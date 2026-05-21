#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR="./myenv"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"
PID_FILE="./server.pid"
LOG_FILE="./server.log"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5001}"
WORKERS="${WORKERS:-2}"

is_running() {
    [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

start() {
    if is_running; then
        echo "Server already running (PID $(cat "$PID_FILE"))."
        return 0
    fi
    rm -f "$PID_FILE"

    if [ ! -f "$VENV_ACTIVATE" ]; then
        echo "Venv activate script not found at $VENV_ACTIVATE. Setup myenv first." >&2
        exit 1
    fi

    # shellcheck disable=SC1090
    source "$VENV_ACTIVATE"

    if ! python -c "import gunicorn" 2>/dev/null; then
        echo "Gunicorn not installed in venv. Run: pip install gunicorn" >&2
        exit 1
    fi

    echo "Starting server on ${HOST}:${PORT}..."
    nohup python -m gunicorn \
        -b "${HOST}:${PORT}" \
        --workers "$WORKERS" \
        --pid "$PID_FILE" \
        app:app \
        >> "$LOG_FILE" 2>&1 &

    for _ in $(seq 1 20); do
        sleep 0.25
        if is_running; then
            echo "Started (PID $(cat "$PID_FILE")). Logs: $LOG_FILE"
            return 0
        fi
    done

    echo "Failed to start. See $LOG_FILE" >&2
    exit 1
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Not running (no PID file)."
        return 0
    fi
    PID="$(cat "$PID_FILE")"
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "Stale PID file removed (PID $PID not alive)."
        rm -f "$PID_FILE"
        return 0
    fi

    echo "Stopping server (PID $PID)..."
    kill "$PID"
    for _ in $(seq 1 20); do
        kill -0 "$PID" 2>/dev/null || break
        sleep 0.5
    done
    if kill -0 "$PID" 2>/dev/null; then
        echo "Process did not exit, sending SIGKILL..."
        kill -9 "$PID" || true
    fi
    rm -f "$PID_FILE"
    echo "Stopped."
}

restart() {
    stop
    sleep 1
    start
}

status() {
    if is_running; then
        echo "Running (PID $(cat "$PID_FILE")) on ${HOST}:${PORT}."
    else
        echo "Not running."
        if [ -f "$PID_FILE" ]; then
            echo "(stale PID file present: $PID_FILE)"
        fi
    fi
}

case "${1:-}" in
    start)   start ;;
    stop)    stop ;;
    restart) restart ;;
    status)  status ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}" >&2
        echo "Env vars: HOST (default 0.0.0.0), PORT (default 5001), WORKERS (default 2)" >&2
        exit 1
        ;;
esac
