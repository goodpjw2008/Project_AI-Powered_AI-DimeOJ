# judge.py

import os
import sys
import uuid
import time
import platform
import subprocess

from models import TestCase, Problem
from config import Config

SANDBOX    = Config.SANDBOX_DIR
PYTHON_BIN = sys.executable

# 기본 체커 코드
DEFAULT_CHECKER = """
import sys

def check(input_file, user_output_file, correct_output_file):
    # 파일에서 입력과 출력 읽기
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    with open(user_output_file, 'r') as f:
        user_output = f.read()
    
    with open(correct_output_file, 'r') as f:
        correct_output = f.read()
    
    # 디버깅을 위한 출력
    print(f"User output (len={len(user_output)}):\\n{repr(user_output)}", file=sys.stderr)
    print(f"Correct output (len={len(correct_output)}):\\n{repr(correct_output)}", file=sys.stderr)
    
    # 줄 단위로 분리하고 각 줄도 공백 제거
    user_lines = [line.strip() for line in user_output.strip().split('\\n')]
    correct_lines = [line.strip() for line in correct_output.strip().split('\\n')]
    
    # 빈 줄 제거
    user_lines = [line for line in user_lines if line]
    correct_lines = [line for line in correct_lines if line]
    
    # 디버깅
    print(f"User lines ({len(user_lines)}): {user_lines}", file=sys.stderr)
    print(f"Correct lines ({len(correct_lines)}): {correct_lines}", file=sys.stderr)
    
    # 줄 수가 다르면 오답
    if len(user_lines) != len(correct_lines):
        print(f"Line count mismatch: {len(user_lines)} vs {len(correct_lines)}", file=sys.stderr)
        return 'WA'
    
    # 각 줄 비교
    for i, (u, c) in enumerate(zip(user_lines, correct_lines)):
        if u != c:
            print(f"Mismatch at line {i+1}: '{u}' vs '{c}'", file=sys.stderr)
            return 'WA'
    
    print("All lines match, returning AC", file=sys.stderr)
    return 'AC'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python checker.py input_file user_output_file correct_output_file", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    user_output_file = sys.argv[2]
    correct_output_file = sys.argv[3]
    
    result = check(input_file, user_output_file, correct_output_file)
    print(result)
"""

try:
    import resource
    HAVE_RESOURCE = True
except ImportError:
    HAVE_RESOURCE = False

def limit_resources(time_limit, memory_limit):
    if not HAVE_RESOURCE:
        return
    try:
        # CPU 시간 제한 설정
        resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit + 1))
        # 메모리 제한 설정 (macOS에서는 RLIMIT_AS 대신 RLIMIT_RSS 사용)
        mem_bytes = memory_limit * 1024 * 1024
        if platform.system() == 'Darwin':  # macOS
            resource.setrlimit(resource.RLIMIT_RSS, (mem_bytes, mem_bytes))
        else:
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    except (ValueError, resource.error) as e:
        print(f"Warning: Could not set resource limits: {e}", file=sys.stderr)
        return

def _run_checker(checker_code: str, input_data: str, user_output: str, correct_output: str) -> str:
    """
    커스텀 체커를 실행하여 결과를 반환합니다.
    체커는 다음 세 가지 값을 반환해야 합니다:
    - AC: 정답
    - WA: 오답
    - PE: 출력 형식 오류
    """
    # 기본 체커 사용
    if checker_code == "default":
        checker_code = DEFAULT_CHECKER
        
    # 1) 체커 코드를 임시 파일로 저장
    token = str(uuid.uuid4())
    wd = os.path.abspath(os.path.join(SANDBOX, token))
    os.makedirs(wd, exist_ok=True)
    
    checker_path = os.path.join(wd, 'checker.py')
    with open(checker_path, 'w', encoding='utf-8') as f:
        f.write(checker_code)
    
    # 디버깅용: 입력값과 출력값 확인
    print(f"Running checker with: input_data: {repr(input_data[:100])}...", file=sys.stderr)
    print(f"User output: {repr(user_output[:100])}...", file=sys.stderr)
    print(f"Correct output: {repr(correct_output[:100])}...", file=sys.stderr)
    
    # 2) 체커 실행
    try:
        # 입력 형식 조정: 각 값을 별도의 파일로 저장
        input_path = os.path.join(wd, 'input.txt')
        user_out_path = os.path.join(wd, 'user_output.txt')
        correct_out_path = os.path.join(wd, 'correct_output.txt')
        
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(input_data)
        with open(user_out_path, 'w', encoding='utf-8') as f:
            f.write(user_output)
        with open(correct_out_path, 'w', encoding='utf-8') as f:
            f.write(correct_output)
        
        proc = subprocess.run(
            [PYTHON_BIN, checker_path, input_path, user_out_path, correct_out_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=wd,
            timeout=5  # 체커 실행 시간 제한
        )
        
        # 디버깅용: 체커 결과 출력
        print(f"Checker output: {proc.stdout.decode()}", file=sys.stderr)
        print(f"Checker error: {proc.stderr.decode()}", file=sys.stderr)
        
        if proc.returncode != 0:
            print(f"Checker error: {proc.stderr.decode()}", file=sys.stderr)
            return 'WA'
            
        verdict = proc.stdout.decode().strip().upper()
        if verdict not in ('AC', 'WA', 'PE'):
            print(f"Invalid checker output: {verdict}", file=sys.stderr)
            return 'WA'
            
        return verdict
        
    except subprocess.TimeoutExpired:
        print("Checker timeout", file=sys.stderr)
        return 'WA'
    except Exception as e:
        print(f"Checker exception: {e}", file=sys.stderr)
        return 'WA'
    finally:
        # 임시 파일 정리
        try:
            import shutil
            shutil.rmtree(wd)
        except:
            pass

def run_code(code: str, language: str, problem: Problem):
    """
    C, C++, Python 코드에 대해
    - TC별 최대 CPU 시간
    - TC별 최대 메모리
    를 기록해 반환합니다.
    반환: (verdict, time_used, memory_used)
    """
    # 1) 작업 디렉터리 준비
    token = str(uuid.uuid4())
    wd = os.path.abspath(os.path.join(SANDBOX, token))
    os.makedirs(wd, exist_ok=True)

    # 2) 소스 파일 쓰기
    if language == 'c':
        src = os.path.join(wd, 'Main.c')
    elif language == 'cpp':
        src = os.path.join(wd, 'Main.cpp')
    else:  # python
        src = os.path.join(wd, 'solution.py')

    # Python 문법 검증
    if language == 'py':
        try:
            compile(code, '<string>', 'exec')
        except Exception:
            return 'CE', None, None

    with open(src, 'w', encoding='utf-8') as f:
        f.write(code)

    # 3) 컴파일 (C/C++)
    exec_path = None
    if language in ('c','cpp'):
        compiler = 'gcc' if language=='c' else 'g++'
        flags    = ['-O2','-std=c11'] if language=='c' else ['-O2','-std=c++17']
        out = os.path.join(wd, 'Main')
        ret = subprocess.run(
            [compiler] + flags + ['-o', out, src],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=wd
        )
        if ret.returncode != 0:
            print(f"Compilation error: {ret.stderr.decode()}", file=sys.stderr)
            return 'CE', None, None
        exec_path = out
    else:
        exec_path = PYTHON_BIN

    # 4) 실행 명령어
    if language in ('c','cpp'):
        run_cmd = [exec_path]
    else:
        run_cmd = [exec_path, '-u', src]

    # 5) 리소스 제한 (C/C++만)
    preexec = None
    if language in ('c','cpp') and HAVE_RESOURCE and platform.system() != 'Windows':
        preexec = lambda: limit_resources(problem.time_limit, problem.memory_limit)

    # 6) TC별 실행, 최대값만 남기기
    max_time = 0.0
    max_mem  = 0

    for tc in problem.testcases.order_by(TestCase.id):
        inp = tc.input_data.encode()
        try:
            start = time.process_time()
            proc = subprocess.run(
                run_cmd,
                input=inp,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=wd,
                timeout=problem.time_limit,
                preexec_fn=preexec if preexec else None
            )
            elapsed = time.process_time() - start
        except subprocess.TimeoutExpired:
            return 'TLE', None, None
        if elapsed > max_time:
            max_time = elapsed

        if proc.returncode != 0:
            print(f"Runtime error: {proc.stderr.decode()}", file=sys.stderr)
            return 'RE', max_time, None

        if HAVE_RESOURCE and platform.system() != 'Windows':
            try:
                usage = resource.getrusage(resource.RUSAGE_CHILDREN)
                mem_mb = usage.ru_maxrss / 1024
                if mem_mb > max_mem:
                    max_mem = int(mem_mb)
            except (ValueError, resource.error) as e:
                print(f"Warning: Could not get resource usage: {e}", file=sys.stderr)

        user_out = proc.stdout.decode()
        correct = tc.output_data

        # 체커 사용 결정
        checker_code = problem.checker if problem.checker else "default"
        verdict = _run_checker(checker_code, tc.input_data, user_out, correct)
        verdict = verdict.strip().upper()
        if verdict != 'AC':
            return verdict, max_time, max_mem

    return 'AC', max_time, max_mem
