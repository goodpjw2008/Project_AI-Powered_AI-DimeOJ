#!/usr/bin/env python
"""
Gunicorn을 사용하여 Flask 서버 실행 스크립트
"""
import subprocess
import sys


def main():
    cmd = [
        'gunicorn',
        '-b', '0.0.0.0:5001',
        '--reload',
        'app:app'
    ]

    print(f"Starting Gunicorn: {' '.join(cmd)}")
    process = subprocess.Popen(cmd)

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        process.terminate()
        process.wait()
        sys.exit(0)


if __name__ == '__main__':
    main()
