from app import app, db
from models import Problem, TestCase

def init_problems_with_testcases():
    with app.app_context():
        # 기존 문제가 있는지 확인하고 모두 삭제
        existing_problems = Problem.query.all()
        if existing_problems:
            for problem in existing_problems:
                db.session.delete(problem)
            db.session.commit()
            print("기존 문제가 모두 삭제되었습니다.")
            
        # A+B 문제 생성
        apb_problem = Problem(
            title="(입출력과 사칙연산)A+B",
            description="두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A+B를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="1 2",
            sample_output="3"
        )
        
        # A-B 문제 생성
        amb_problem = Problem(
            title="(입출력과 사칙연산)A-B",
            description="두 정수 A와 B를 입력받은 다음, A-B를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A-B를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3 2",
            sample_output="1"
        )
        
        # A×B 문제 생성
        amul_problem = Problem(
            title="(입출력과 사칙연산)A×B",
            description="두 정수 A와 B를 입력받은 다음, A×B를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A×B를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="1 2",
            sample_output="2"
        )
        
        # A/B 문제 생성
        adiv_problem = Problem(
            title="(입출력과 사칙연산)A/B",
            description="두 정수 A와 B를 입력받은 다음, A/B를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A/B를 출력한다. 실제 정답과 출력값의 절대오차 또는 상대오차가 10-9 이하이면 정답이다.",
            time_limit=1,
            memory_limit=128,
            checker="""
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
    
    # 공백을 제거하고 유저 출력과 정답 출력을 부동소수점 숫자로 변환
    try:
        user_value = float(user_output.strip())
        correct_value = float(correct_output.strip())
        
        # 절대 오차 또는 상대 오차 계산
        abs_error = abs(user_value - correct_value)
        rel_error = abs_error / max(1e-9, abs(correct_value))  # 0으로 나누는 것 방지
        
        # 디버깅을 위한 출력
        print(f"User value: {user_value}", file=sys.stderr)
        print(f"Correct value: {correct_value}", file=sys.stderr)
        print(f"Absolute error: {abs_error}", file=sys.stderr)
        print(f"Relative error: {rel_error}", file=sys.stderr)
        
        # 절대 오차 또는 상대 오차가 10^-9 이하면 정답
        if abs_error <= 1e-9 or rel_error <= 1e-9:
            print("Error within tolerance, returning AC", file=sys.stderr)
            return 'AC'
        else:
            print("Error outside tolerance, returning WA", file=sys.stderr)
            return 'WA'
    except ValueError as e:
        # 숫자로 변환할 수 없는 경우
        print(f"Conversion error: {e}", file=sys.stderr)
        return 'WA'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python checker.py input_file user_output_file correct_output_file", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    user_output_file = sys.argv[2]
    correct_output_file = sys.argv[3]
    
    result = check(input_file, user_output_file, correct_output_file)
    print(result)
""",
            sample_input="1 3",
            sample_output="0.33333333333333333333333333333333"
        )
        
        # 사칙연산 문제 생성
        arithmetic_problem = Problem(
            title="사칙연산",
            description="두 자연수 A와 B가 주어진다. 이때, A+B, A-B, A*B, A/B(몫), A%B(나머지)를 출력하는 프로그램을 작성하시오.",
            input_spec="두 자연수 A와 B가 주어진다. (1 ≤ A, B ≤ 10,000)",
            output_spec="첫째 줄에 A+B, 둘째 줄에 A-B, 셋째 줄에 A*B, 넷째 줄에 A/B, 다섯째 줄에 A%B를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="7 3",
            sample_output="10\n4\n21\n2\n1"
        )
        
        # 두 수 비교하기 문제 생성
        compare_problem = Problem(
            title="(조건문)두 수 비교하기",
            description="두 정수 A와 B가 주어졌을 때, A와 B를 비교하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 A와 B가 주어진다. A와 B는 공백 한 칸으로 구분되어져 있다.\n\n제한\n-10,000 ≤ A, B ≤ 10,000",
            output_spec="첫째 줄에 다음 세 가지 중 하나를 출력한다.\n\nA가 B보다 큰 경우에는 '>'를 출력한다.\nA가 B보다 작은 경우에는 '<'를 출력한다.\nA와 B가 같은 경우에는 '=='를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="1 2",
            sample_output="<"
        )
        
        # 시험 성적 문제 생성
        grade_problem = Problem(
            title="(조건문)시험 성적",
            description="시험 점수를 입력받아 90 ~ 100점은 A, 80 ~ 89점은 B, 70 ~ 79점은 C, 60 ~ 69점은 D, 나머지 점수는 F를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 시험 점수가 주어진다. 시험 점수는 0보다 크거나 같고, 100보다 작거나 같은 정수이다.",
            output_spec="시험 성적을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="100",
            sample_output="A"
        )
        
        # 윤년 문제 생성
        leap_year_problem = Problem(
            title="(조건문)윤년",
            description="연도가 주어졌을 때, 윤년이면 1, 아니면 0을 출력하는 프로그램을 작성하시오.\n\n윤년은 연도가 4의 배수이면서, 100의 배수가 아닐 때 또는 400의 배수일 때이다.\n\n예를 들어, 2012년은 4의 배수이면서 100의 배수가 아니라서 윤년이다. 1900년은 100의 배수이고 400의 배수는 아니기 때문에 윤년이 아니다. 하지만, 2000년은 400의 배수이기 때문에 윤년이다.",
            input_spec="첫째 줄에 연도가 주어진다. 연도는 1보다 크거나 같고, 4000보다 작거나 같은 자연수이다.",
            output_spec="첫째 줄에 윤년이면 1, 아니면 0을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="2000",
            sample_output="1"
        )
        
        # 구구단 문제 생성
        gugudan_problem = Problem(
            title="(반복문)구구단",
            description="N을 입력받은 뒤, 구구단 N단을 출력하는 프로그램을 작성하시오. 출력 형식에 맞춰서 출력하면 된다.",
            input_spec="첫째 줄에 N이 주어진다. N은 1보다 크거나 같고, 9보다 작거나 같다.",
            output_spec="출력형식과 같게 N*1부터 N*9까지 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="2",
            sample_output="2 * 1 = 2\n2 * 2 = 4\n2 * 3 = 6\n2 * 4 = 8\n2 * 5 = 10\n2 * 6 = 12\n2 * 7 = 14\n2 * 8 = 16\n2 * 9 = 18"
        )
        
        # 합 문제 생성
        sum_problem = Problem(
            title="(반복문)합",
            description="n이 주어졌을 때, 1부터 n까지 합을 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 n (1 ≤ n ≤ 10,000)이 주어진다.",
            output_spec="1부터 n까지 합을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3",
            sample_output="6"
        )
        
        # 영수증 문제 생성
        receipt_problem = Problem(
            title="(반복문)영수증",
            description="준원이는 저번 주에 살면서 처음으로 코스트코를 가 봤다. 정말 멋졌다. 그런데, 몇 개 담지도 않았는데 수상하게 높은 금액이 나오는 것이다! 준원이는 영수증을 보면서 정확하게 계산된 것이 맞는지 확인해보려 한다.\n\n영수증에 적힌,\n\n구매한 각 물건의 가격과 개수\n구매한 물건들의 총 금액\n을 보고, 구매한 물건의 가격과 개수로 계산한 총 금액이 영수증에 적힌 총 금액과 일치하는지 검사해보자.",
            input_spec="첫째 줄에는 영수증에 적힌 총 금액 X가 주어진다.\n\n둘째 줄에는 영수증에 적힌 구매한 물건의 종류의 수 N이 주어진다.\n\n이후 N개의 줄에는 각 물건의 가격 a와 개수 b가 공백을 사이에 두고 주어진다.\n\n제한\n1 ≤ X ≤ 1,000,000,000\n1 ≤ N ≤ 100\n1 ≤ a ≤ 1,000,000\n1 ≤ b ≤ 10",
            output_spec="구매한 물건의 가격과 개수로 계산한 총 금액이 영수증에 적힌 총 금액과 일치하면 Yes를 출력한다. 일치하지 않는다면 No를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="260000\n4\n20000 5\n30000 2\n10000 6\n5000 8",
            sample_output="Yes"
        )
        
        # 별 찍기 문제 생성
        star_problem = Problem(
            title="(반복문)별 찍기",
            description="첫째 줄에는 별 1개, 둘째 줄에는 별 2개, N번째 줄에는 별 N개를 찍는 문제",
            input_spec="첫째 줄에 N(1 ≤ N ≤ 100)이 주어진다.",
            output_spec="첫째 줄부터 N번째 줄까지 차례대로 별을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5",
            sample_output="*\n**\n***\n****\n*****"
        )
        
        # (배열)개수 세기 문제 생성
        count_problem = Problem(
            title="(배열)개수 세기",
            description="총 N개의 정수가 주어졌을 때, 정수 v가 몇 개인지 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 정수의 개수 N(1 ≤ N ≤ 100)이 주어진다. 둘째 줄에는 정수가 공백으로 구분되어져있다. 셋째 줄에는 찾으려고 하는 정수 v가 주어진다. 입력으로 주어지는 정수와 v는 -100보다 크거나 같으며, 100보다 작거나 같다.",
            output_spec="첫째 줄에 입력으로 주어진 N개의 정수 중에 v가 몇 개인지 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="11\n1 4 1 2 4 2 4 2 3 4 4\n2",
            sample_output="3"
        )
        
        # (배열)X보다 작은 수 문제 생성
        less_than_x_problem = Problem(
            title="(배열)X보다 작은 수",
            description="정수 N개로 이루어진 수열 A와 정수 X가 주어진다. 이때, A에서 X보다 작은 수를 모두 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N과 X가 주어진다. (1 ≤ N, X ≤ 10,000)\n\n둘째 줄에 수열 A를 이루는 정수 N개가 주어진다. 주어지는 정수는 모두 1보다 크거나 같고, 10,000보다 작거나 같은 정수이다.",
            output_spec="X보다 작은 수를 입력받은 순서대로 공백으로 구분해 출력한다. X보다 작은 수는 적어도 하나 존재한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10 5\n1 10 4 9 2 3 8 5 7 6",
            sample_output="1 4 2 3"
        )
        
        # (배열)공 넣기 문제 생성
        put_ball_problem = Problem(
            title="(배열)공 넣기",
            description="도현이는 바구니를 총 N개 가지고 있고, 각각의 바구니에는 1번부터 N번까지 번호가 매겨져 있다. 또, 1번부터 N번까지 번호가 적혀있는 공을 매우 많이 가지고 있다. 가장 처음 바구니에는 공이 들어있지 않으며, 바구니에는 공을 1개만 넣을 수 있다.\n\n도현이는 앞으로 M번 공을 넣으려고 한다. 도현이는 한 번 공을 넣을 때, 공을 넣을 바구니 범위를 정하고, 정한 바구니에 모두 같은 번호가 적혀있는 공을 넣는다. 만약, 바구니에 공이 이미 있는 경우에는 들어있는 공을 빼고, 새로 공을 넣는다. 공을 넣을 바구니는 연속되어 있어야 한다.\n\n공을 어떻게 넣을지가 주어졌을 때, M번 공을 넣은 이후에 각 바구니에 어떤 공이 들어 있는지 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N (1 ≤ N ≤ 100)과 M (1 ≤ M ≤ 100)이 주어진다.\n\n둘째 줄부터 M개의 줄에 걸쳐서 공을 넣는 방법이 주어진다. 각 방법은 세 정수 i j k로 이루어져 있으며, i번 바구니부터 j번 바구니까지에 k번 번호가 적혀져 있는 공을 넣는다는 뜻이다. 예를 들어, 2 5 6은 2번 바구니부터 5번 바구니까지에 6번 공을 넣는다는 뜻이다. (1 ≤ i ≤ j ≤ N, 1 ≤ k ≤ N)\n\n도현이는 입력으로 주어진 순서대로 공을 넣는다.",
            output_spec="1번 바구니부터 N번 바구니에 들어있는 공의 번호를 공백으로 구분해 출력한다. 공이 들어있지 않은 바구니는 0을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 4\n1 2 3\n3 4 4\n1 4 1\n2 2 2",
            sample_output="1 2 1 1 0"
        )
        
        # (배열)공 바꾸기 문제 생성
        swap_ball_problem = Problem(
            title="(배열)공 바꾸기",
            description="도현이는 바구니를 총 N개 가지고 있고, 각각의 바구니에는 1번부터 N번까지 번호가 매겨져 있다. 바구니에는 공이 1개씩 들어있고, 처음에는 바구니에 적혀있는 번호와 같은 번호가 적힌 공이 들어있다.\n\n도현이는 앞으로 M번 공을 바꾸려고 한다. 도현이는 공을 바꿀 바구니 2개를 선택하고, 두 바구니에 들어있는 공을 서로 교환한다.\n\n공을 어떻게 바꿀지가 주어졌을 때, M번 공을 바꾼 이후에 각 바구니에 어떤 공이 들어있는지 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N (1 ≤ N ≤ 100)과 M (1 ≤ M ≤ 100)이 주어진다.\n\n둘째 줄부터 M개의 줄에 걸쳐서 공을 교환할 방법이 주어진다. 각 방법은 두 정수 i j로 이루어져 있으며, i번 바구니와 j번 바구니에 들어있는 공을 교환한다는 뜻이다. (1 ≤ i ≤ j ≤ N)\n\n도현이는 입력으로 주어진 순서대로 공을 교환한다.",
            output_spec="1번 바구니부터 N번 바구니에 들어있는 공의 번호를 공백으로 구분해 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 4\n1 2\n3 4\n1 4\n2 2",
            sample_output="3 1 4 2 5"
        )
        
        # (배열)평균  문제 생성
        avg_problem = Problem(
            title="(배열)평균",
            description="세준이는 기말고사를 망쳤다. 세준이는 점수를 조작해서 집에 가져가기로 했다. 일단 세준이는 자기 점수 중에 최댓값을 골랐다. 이 값을 M이라고 한다. 그리고 나서 모든 점수를 점수/M*100으로 고쳤다.\n\n예를 들어, 세준이의 최고점이 70이고, 수학점수가 50이었으면 수학점수는 50/70*100이 되어 71.43점이 된다.\n\n세준이의 성적을 위의 방법대로 새로 계산했을 때, 새로운 평균을 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 시험 본 과목의 개수 N이 주어진다. 이 값은 1000보다 작거나 같다. 둘째 줄에 세준이의 현재 성적이 주어진다. 이 값은 100보다 작거나 같은 음이 아닌 정수이고, 적어도 하나의 값은 0보다 크다.",
            output_spec="첫째 줄에 새로운 평균을 출력한다. 실제 정답과 출력값의 절대오차 또는 상대오차가 10-2 이하이면 정답이다.",
            time_limit=1,
            memory_limit=128,
            checker="""
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
    
    # 공백을 제거하고 유저 출력과 정답 출력을 부동소수점 숫자로 변환
    try:
        user_value = float(user_output.strip())
        correct_value = float(correct_output.strip())
        
        # 절대 오차 또는 상대 오차 계산
        abs_error = abs(user_value - correct_value)
        rel_error = abs_error / max(1e-9, abs(correct_value))  # 0으로 나누는 것 방지
        
        # 디버깅을 위한 출력
        print(f"User value: {user_value}", file=sys.stderr)
        print(f"Correct value: {correct_value}", file=sys.stderr)
        print(f"Absolute error: {abs_error}", file=sys.stderr)
        print(f"Relative error: {rel_error}", file=sys.stderr)
        
        # 절대 오차 또는 상대 오차가 10^-2 이하면 정답
        if abs_error <= 1e-2 or rel_error <= 1e-2:
            print("Error within tolerance, returning AC", file=sys.stderr)
            return 'AC'
        else:
            print("Error outside tolerance, returning WA", file=sys.stderr)
            return 'WA'
    except ValueError as e:
        # 숫자로 변환할 수 없는 경우
        print(f"Conversion error: {e}", file=sys.stderr)
        return 'WA'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python checker.py input_file user_output_file correct_output_file", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    user_output_file = sys.argv[2]
    correct_output_file = sys.argv[3]
    
    result = check(input_file, user_output_file, correct_output_file)
    print(result)
""",
            sample_input="3\n40 80 60",
            sample_output="75.0"
        )
        
        # (문자열)문자와 문자열 문제 생성
        char_in_string_problem = Problem(
            title="(문자열)문자와 문자열",
            description="단어 S와 정수 i가 주어졌을 때, S의 i번째 글자를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 영어 소문자와 대문자로만 이루어진 단어 S가 주어진다. 단어의 길이는 최대 1,000이다.\n\n둘째 줄에 정수 i가 주어진다. (1 ≤ i ≤ |S|)",
            output_spec="S의 i번째 글자를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="Sprout\n3",
            sample_output="r"
        )
        
        # (문자열)단어 길이 재기 문제 생성
        word_length_problem = Problem(
            title="(문자열)단어 길이 재기",
            description="알파벳으로만 이루어진 단어를 입력받아, 그 길이를 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 영어 소문자와 대문자로만 이루어진 단어가 주어진다. 단어의 길이는 최대 100이다.",
            output_spec="첫째 줄에 입력으로 주어진 단어의 길이를 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="pulljima",
            sample_output="8"
        )
        
        # (문자열)문자열 문제 생성
        first_last_problem = Problem(
            title="(문자열)문자열",
            description="문자열을 입력으로 주면 문자열의 첫 글자와 마지막 글자를 출력하는 프로그램을 작성하시오.",
            input_spec="입력의 첫 줄에는 테스트 케이스의 개수 T(1 ≤ T ≤ 10)가 주어진다. 각 테스트 케이스는 한 줄에 하나의 문자열이 주어진다. 문자열은 알파벳 A~Z 대문자로 이루어지며 알파벳 사이에 공백은 없으며 문자열의 길이는 1000보다 작다.",
            output_spec="각 테스트 케이스에 대해서 주어진 문자열의 첫 글자와 마지막 글자를 연속하여 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3\nACDKJFOWIEGHE\nO\nAB",
            sample_output="AE\nOO\nAB"
        )
        
        # (문자열)숫자의 합 문제 생성
        sum_of_digits_problem = Problem(
            title="(문자열)숫자의 합",
            description="N개의 숫자가 공백 없이 쓰여있다. 이 숫자를 모두 합해서 출력하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 숫자의 개수 N (1 ≤ N ≤ 100)이 주어진다. 둘째 줄에 숫자 N개가 공백없이 주어진다.",
            output_spec="입력으로 주어진 숫자 N개의 합을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n54321",
            sample_output="15"
        )
        
        # (브루트 포스)블랙잭 문제 생성
        blackjack_problem = Problem(
            title="(브루트 포스)블랙잭",
            description="카지노에서 제일 인기 있는 게임 블랙잭의 규칙은 상당히 쉽다. 카드의 합이 21을 넘지 않는 한도 내에서, 카드의 합을 최대한 크게 만드는 게임이다. 블랙잭은 카지노마다 다양한 규정이 있다.\n\n한국 최고의 블랙잭 고수 김정인은 새로운 블랙잭 규칙을 만들어 상근, 창영이와 게임하려고 한다.\n\n김정인 버전의 블랙잭에서 각 카드에는 양의 정수가 쓰여 있다. 그 다음, 딜러는 N장의 카드를 모두 숫자가 보이도록 바닥에 놓는다. 그런 후에 딜러는 숫자 M을 크게 외친다.\n\n이제 플레이어는 제한된 시간 안에 N장의 카드 중에서 3장의 카드를 골라야 한다. 블랙잭 변형 게임이기 때문에, 플레이어가 고른 카드의 합은 M을 넘지 않으면서 M과 최대한 가깝게 만들어야 한다.\n\nN장의 카드에 써져 있는 숫자가 주어졌을 때, M을 넘지 않으면서 M에 최대한 가까운 카드 3장의 합을 구해 출력하시오.",
            input_spec="첫째 줄에 카드의 개수 N(3 ≤ N ≤ 100)과 M(10 ≤ M ≤ 300,000)이 주어진다. 둘째 줄에는 카드에 쓰여 있는 숫자가 주어지며, 이 값은 100,000을 넘지 않는 양의 정수이다.\n\n합이 M을 넘지 않는 카드 3장을 찾을 수 있는 경우만 입력으로 주어진다.",
            output_spec="첫째 줄에 M을 넘지 않으면서 M에 최대한 가까운 카드 3장의 합을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 21\n5 6 7 8 9",
            sample_output="21"
        )
        
        # (브루트 포스)분해합 문제 생성
        decompose_problem = Problem(
            title="(브루트 포스)분해합",
            description="어떤 자연수 N이 있을 때, 그 자연수 N의 분해합은 N과 N을 이루는 각 자리수의 합을 의미한다. 어떤 자연수 M의 분해합이 N인 경우, M을 N의 생성자라 한다. 예를 들어, 245의 분해합은 256(=245+2+4+5)이 된다. 따라서 245는 256의 생성자가 된다. 물론, 어떤 자연수의 경우에는 생성자가 없을 수도 있다. 반대로, 생성자가 여러 개인 자연수도 있을 수 있다.\n\n자연수 N이 주어졌을 때, N의 가장 작은 생성자를 구해내는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 자연수 N(1 ≤ N ≤ 1,000,000)이 주어진다.",
            output_spec="첫째 줄에 답을 출력한다. 생성자가 없는 경우에는 0을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="216",
            sample_output="198"
        )
        
        # (브루트 포스)체스판 다시 칠하기 문제 생성
        chess_repaint_problem = Problem(
            title="(브루트 포스)체스판 다시 칠하기",
            description="지민이는 자신의 저택에서 MN개의 단위 정사각형으로 나누어져 있는 M×N 크기의 보드를 찾았다. 어떤 정사각형은 검은색으로 칠해져 있고, 나머지는 흰색으로 칠해져 있다. 지민이는 이 보드를 잘라서 8×8 크기의 체스판으로 만들려고 한다.\n\n체스판은 검은색과 흰색이 번갈아서 칠해져 있어야 한다. 구체적으로, 각 칸이 검은색과 흰색 중 하나로 색칠되어 있고, 변을 공유하는 두 개의 사각형은 다른 색으로 칠해져 있어야 한다. 따라서 이 정의를 따르면 체스판을 색칠하는 경우는 두 가지뿐이다. 하나는 맨 왼쪽 위 칸이 흰색인 경우, 하나는 검은색인 경우이다.\n\n보드가 체스판처럼 칠해져 있다는 보장이 없어서, 지민이는 8×8 크기의 체스판으로 잘라낸 후에 몇 개의 정사각형을 다시 칠해야겠다고 생각했다. 당연히 8*8 크기는 아무데서나 골라도 된다. 지민이가 다시 칠해야 하는 정사각형의 최소 개수를 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N과 M이 주어진다. N과 M은 8보다 크거나 같고, 50보다 작거나 같은 자연수이다. 둘째 줄부터 N개의 줄에는 보드의 각 행의 상태가 주어진다. B는 검은색이며, W는 흰색이다.",
            output_spec="첫째 줄에 지민이가 다시 칠해야 하는 정사각형 개수의 최솟값을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="8 8\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBBBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBWBWBW",
            sample_output="1"
        )
        
        # (정렬)수 정렬하기 문제 생성
        sort_numbers_problem = Problem(
            title="(정렬)수 정렬하기",
            description="N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 수의 개수 N(1 ≤ N ≤ 1,000)이 주어진다. 둘째 줄부터 N개의 줄에는 수가 주어진다. 이 수는 절댓값이 1,000보다 작거나 같은 정수이다. 수는 중복되지 않는다.",
            output_spec="첫째 줄부터 N개의 줄에 오름차순으로 정렬한 결과를 한 줄에 하나씩 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n5\n2\n3\n4\n1",
            sample_output="1\n2\n3\n4\n5"
        )
        
        # (정렬)대표값 문제 생성
        representative_value_problem = Problem(
            title="(정렬)대표값",
            description="어떤 수들이 있을 때, 그 수들을 대표하는 값으로 가장 흔하게 쓰이는 것은 평균이다. 평균은 주어진 모든 수의 합을 수의 개수로 나눈 것이다. 예를 들어 10, 40, 30, 60, 30의 평균은 (10 + 40 + 30 + 60 + 30) / 5 = 170 / 5 = 34가 된다.\n\n평균 이외의 또 다른 대표값으로 중앙값이라는 것이 있다. 중앙값은 주어진 수를 크기 순서대로 늘어 놓았을 때 가장 중앙에 놓인 값이다. 예를 들어 10, 40, 30, 60, 30의 경우, 크기 순서대로 늘어 놓으면\n\n10 30 30 40 60\n\n이 되고 따라서 중앙값은 30이 된다.\n\n다섯 개의 자연수가 주어질 때 이들의 평균과 중앙값을 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄부터 다섯 번째 줄까지 한 줄에 하나씩 자연수가 주어진다. 주어지는 자연수는 100 보다 작은 10의 배수이다.",
            output_spec="첫째 줄에는 평균을 출력하고, 둘째 줄에는 중앙값을 출력한다. 평균과 중앙값은 모두 자연수이다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10\n40\n30\n60\n30",
            sample_output="34\n30"
        )
        
        # (정렬)단어 정렬 문제 생성
        word_sort_problem = Problem(
            title="(정렬)단어 정렬",
            description="알파벳 소문자로 이루어진 N개의 단어가 들어오면 아래와 같은 조건에 따라 정렬하는 프로그램을 작성하시오.\n\n1. 길이가 짧은 것부터\n2. 길이가 같으면 사전 순으로\n\n단, 중복된 단어는 하나만 남기고 제거해야 한다.",
            input_spec="첫째 줄에 단어의 개수 N이 주어진다. (1 ≤ N ≤ 20,000) 둘째 줄부터 N개의 줄에 걸쳐 알파벳 소문자로 이루어진 단어가 한 줄에 하나씩 주어진다. 주어지는 문자열의 길이는 50을 넘지 않는다.",
            output_spec="조건에 따라 정렬하여 단어들을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="13\nbut\ni\nwont\nhesitate\nno\nmore\nno\nmore\nit\ncannot\nwait\nim\nyours",
            sample_output="i\nim\nit\nno\nbut\nmore\nwait\nwont\nyours\ncannot\nhesitate"
        )
        
        # (자료구조)스택 문제 생성
        stack_problem = Problem(
            title="(자료구조)스택",
            description="정수를 저장하는 스택을 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.\n\n명령은 총 다섯 가지이다.\n\n1 X: 정수 X를 스택에 넣는다. (1 ≤ X ≤ 100,000)\n2: 스택에 정수가 있다면 맨 위의 정수를 빼고 출력한다. 없다면 -1을 대신 출력한다.\n3: 스택에 들어있는 정수의 개수를 출력한다.\n4: 스택이 비어있으면 1, 아니면 0을 출력한다.\n5: 스택에 정수가 있다면 맨 위의 정수를 출력한다. 없다면 -1을 대신 출력한다.",
            input_spec="첫째 줄에 명령의 수 N이 주어진다. (1 ≤ N ≤ 1,000,000)\n\n둘째 줄부터 N개 줄에 명령이 하나씩 주어진다.\n\n출력을 요구하는 명령은 하나 이상 주어진다.",
            output_spec="출력을 요구하는 명령이 주어질 때마다 명령의 결과를 한 줄에 하나씩 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="9\n4\n1 3\n1 5\n3\n2\n5\n2\n2\n5",
            sample_output="1\n2\n5\n3\n3\n-1\n-1"
        )
        
        # (자료구조)큐 문제 생성
        queue_problem = Problem(
            title="(자료구조)큐",
            description="정수를 저장하는 큐를 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.\n\n명령은 총 여섯 가지이다.\n\npush X: 정수 X를 큐에 넣는 연산이다.\npop: 큐에서 가장 앞에 있는 정수를 빼고, 그 수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.\nsize: 큐에 들어있는 정수의 개수를 출력한다.\nempty: 큐가 비어있으면 1, 아니면 0을 출력한다.\nfront: 큐의 가장 앞에 있는 정수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.\nback: 큐의 가장 뒤에 있는 정수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.",
            input_spec="첫째 줄에 주어지는 명령의 수 N (1 ≤ N ≤ 2,000,000)이 주어진다. 둘째 줄부터 N개의 줄에는 명령이 하나씩 주어진다. 주어지는 정수는 1보다 크거나 같고, 100,000보다 작거나 같다. 문제에 나와있지 않은 명령이 주어지는 경우는 없다.",
            output_spec="출력해야하는 명령이 주어질 때마다, 한 줄에 하나씩 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="15\npush 1\npush 2\nfront\nback\nsize\nempty\npop\npop\npop\nsize\nempty\npop\npush 3\nempty\nfront",
            sample_output="1\n2\n2\n0\n1\n2\n-1\n0\n1\n-1\n0\n3"
        )
        
        # (그리디 알고리즘)동전 문제 생성
        coin_problem = Problem(
            title="(그리디 알고리즘)동전",
            description="준규가 가지고 있는 동전은 총 N종류이고, 각각의 동전을 매우 많이 가지고 있다.\n\n동전을 적절히 사용해서 그 가치의 합을 K로 만들려고 한다. 이때 필요한 동전 개수의 최솟값을 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N과 K가 주어진다. (1 ≤ N ≤ 10, 1 ≤ K ≤ 100,000,000)\n\n둘째 줄부터 N개의 줄에 동전의 가치 Ai가 오름차순으로 주어진다. (1 ≤ Ai ≤ 1,000,000, A1 = 1, i ≥ 2인 경우에 Ai는 Ai-1의 배수)",
            output_spec="첫째 줄에 K원을 만드는데 필요한 동전 개수의 최솟값을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10 4200\n1\n5\n10\n50\n100\n500\n1000\n5000\n10000\n50000",
            sample_output="6"
        )
        
        # (이분 탐색)수 찾기 문제 생성
        binary_search_problem = Problem(
            title="(이분 탐색)수 찾기",
            description="N개의 정수 A[1], A[2], …, A[N]이 주어져 있을 때, 이 안에 X라는 정수가 존재하는지 알아내는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 자연수 N(1 ≤ N ≤ 100,000)이 주어진다. 다음 줄에는 N개의 정수 A[1], A[2], …, A[N]이 주어진다. 다음 줄에는 M(1 ≤ M ≤ 100,000)이 주어진다. 다음 줄에는 M개의 수들이 주어지는데, 이 수들이 A안에 존재하는지 알아내면 된다. 모든 정수의 범위는 -231 보다 크거나 같고 231보다 작다.",
            output_spec="M개의 줄에 답을 출력한다. 존재하면 1을, 존재하지 않으면 0을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n4 1 5 2 3\n5\n1 3 7 9 5",
            sample_output="1\n1\n0\n0\n1"
        )
        
        # (자료구조)트리의 부모 찾기 문제 생성
        tree_parent_problem = Problem(
            title="(자료구조)트리의 부모 찾기",
            description="루트 없는 트리가 주어진다. 이때, 트리의 루트를 1이라고 정했을 때, 각 노드의 부모를 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 노드의 개수 N (2 ≤ N ≤ 100,000)이 주어진다. 둘째 줄부터 N-1개의 줄에 트리 상에서 연결된 두 정점이 주어진다.",
            output_spec="첫째 줄부터 N-1개의 줄에 각 노드의 부모 노드 번호를 2번 노드부터 순서대로 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="7\n1 6\n6 3\n3 5\n4 1\n2 4\n4 7",
            sample_output="4\n6\n1\n3\n1\n4"
        )
        
        # 데이터베이스에 문제 저장
        db.session.add(apb_problem)
        db.session.add(amb_problem)
        db.session.add(amul_problem)
        db.session.add(adiv_problem)
        db.session.add(arithmetic_problem)
        db.session.add(compare_problem)
        db.session.add(grade_problem)
        db.session.add(leap_year_problem)
        db.session.add(gugudan_problem)
        db.session.add(sum_problem)
        db.session.add(receipt_problem)
        db.session.add(star_problem)
        db.session.add(count_problem)
        db.session.add(less_than_x_problem)
        db.session.add(put_ball_problem)
        db.session.add(swap_ball_problem)
        db.session.add(avg_problem)
        db.session.add(char_in_string_problem)
        db.session.add(word_length_problem)
        db.session.add(first_last_problem)
        db.session.add(sum_of_digits_problem)
        db.session.add(blackjack_problem)
        db.session.add(decompose_problem)
        db.session.add(chess_repaint_problem)
        db.session.add(sort_numbers_problem)
        db.session.add(representative_value_problem)
        db.session.add(word_sort_problem)
        db.session.add(stack_problem)
        db.session.add(queue_problem)
        db.session.add(coin_problem)
        db.session.add(binary_search_problem)
        db.session.add(tree_parent_problem)
        db.session.commit()
        
        # A+B 문제에 대한 테스트 케이스 추가
        test_case1 = TestCase(
            problem_id=apb_problem.id,
            input_data="1 2",
            output_data="3"
        )
        
        test_case2 = TestCase(
            problem_id=apb_problem.id,
            input_data="3 4",
            output_data="7"
        )
        
        test_case3 = TestCase(
            problem_id=apb_problem.id,
            input_data="9 8",
            output_data="17"
        )
        
        # A-B 문제에 대한 테스트 케이스 추가
        test_case4 = TestCase(
            problem_id=amb_problem.id,
            input_data="3 2",
            output_data="1"
        )
        
        test_case5 = TestCase(
            problem_id=amb_problem.id,
            input_data="5 2",
            output_data="3"
        )
        
        test_case6 = TestCase(
            problem_id=amb_problem.id,
            input_data="9 1",
            output_data="8"
        )
        
        # A×B 문제에 대한 테스트 케이스 추가
        test_case7 = TestCase(
            problem_id=amul_problem.id,
            input_data="1 2",
            output_data="2"
        )
        
        test_case8 = TestCase(
            problem_id=amul_problem.id,
            input_data="3 4",
            output_data="12"
        )
        
        test_case9 = TestCase(
            problem_id=amul_problem.id,
            input_data="9 9",
            output_data="81"
        )
        
        # A/B 문제에 대한 테스트 케이스 추가
        test_case10 = TestCase(
            problem_id=adiv_problem.id,
            input_data="1 3",
            output_data="0.33333333333333333333333333333333"
        )
        
        test_case11 = TestCase(
            problem_id=adiv_problem.id,
            input_data="4 5",
            output_data="0.8"
        )
        
        test_case12 = TestCase(
            problem_id=adiv_problem.id,
            input_data="3 2",
            output_data="1.5"
        )
        
        # 사칙연산 문제에 대한 테스트 케이스 추가
        test_case13 = TestCase(
            problem_id=arithmetic_problem.id,
            input_data="7 3",
            output_data="10\n4\n21\n2\n1"
        )
        
        test_case14 = TestCase(
            problem_id=arithmetic_problem.id,
            input_data="5 2",
            output_data="7\n3\n10\n2\n1"
        )
        
        test_case15 = TestCase(
            problem_id=arithmetic_problem.id,
            input_data="10 3",
            output_data="13\n7\n30\n3\n1"
        )
        
        # 두 수 비교하기 문제에 대한 테스트 케이스 추가
        test_case16 = TestCase(
            problem_id=compare_problem.id,
            input_data="1 2",
            output_data="<"
        )
        
        test_case17 = TestCase(
            problem_id=compare_problem.id,
            input_data="10 2",
            output_data=">"
        )
        
        test_case18 = TestCase(
            problem_id=compare_problem.id,
            input_data="5 5",
            output_data="=="
        )
        
        # 시험 성적 문제에 대한 테스트 케이스 추가
        test_case19 = TestCase(
            problem_id=grade_problem.id,
            input_data="100",
            output_data="A"
        )
        
        test_case20 = TestCase(
            problem_id=grade_problem.id,
            input_data="85",
            output_data="B"
        )
        
        test_case21 = TestCase(
            problem_id=grade_problem.id,
            input_data="73",
            output_data="C"
        )
        
        test_case22 = TestCase(
            problem_id=grade_problem.id,
            input_data="65",
            output_data="D"
        )
        
        test_case23 = TestCase(
            problem_id=grade_problem.id,
            input_data="59",
            output_data="F"
        )
        
        # 윤년 문제에 대한 테스트 케이스 추가
        test_case24 = TestCase(
            problem_id=leap_year_problem.id,
            input_data="2000",
            output_data="1"
        )
        
        test_case25 = TestCase(
            problem_id=leap_year_problem.id,
            input_data="1999",
            output_data="0"
        )
        
        test_case26 = TestCase(
            problem_id=leap_year_problem.id,
            input_data="2012",
            output_data="1"
        )
        
        test_case27 = TestCase(
            problem_id=leap_year_problem.id,
            input_data="1900",
            output_data="0"
        )
        
        # 구구단 문제에 대한 테스트 케이스 추가
        test_case28 = TestCase(
            problem_id=gugudan_problem.id,
            input_data="2",
            output_data="2 * 1 = 2\n2 * 2 = 4\n2 * 3 = 6\n2 * 4 = 8\n2 * 5 = 10\n2 * 6 = 12\n2 * 7 = 14\n2 * 8 = 16\n2 * 9 = 18"
        )
        
        test_case29 = TestCase(
            problem_id=gugudan_problem.id,
            input_data="3",
            output_data="3 * 1 = 3\n3 * 2 = 6\n3 * 3 = 9\n3 * 4 = 12\n3 * 5 = 15\n3 * 6 = 18\n3 * 7 = 21\n3 * 8 = 24\n3 * 9 = 27"
        )
        
        test_case30 = TestCase(
            problem_id=gugudan_problem.id,
            input_data="9",
            output_data="9 * 1 = 9\n9 * 2 = 18\n9 * 3 = 27\n9 * 4 = 36\n9 * 5 = 45\n9 * 6 = 54\n9 * 7 = 63\n9 * 8 = 72\n9 * 9 = 81"
        )
        
        # 합 문제에 대한 테스트 케이스 추가
        test_case31 = TestCase(
            problem_id=sum_problem.id,
            input_data="3",
            output_data="6"
        )
        
        test_case32 = TestCase(
            problem_id=sum_problem.id,
            input_data="10",
            output_data="55"
        )
        
        test_case33 = TestCase(
            problem_id=sum_problem.id,
            input_data="100",
            output_data="5050"
        )
        
        # 영수증 문제에 대한 테스트 케이스 추가
        test_case34 = TestCase(
            problem_id=receipt_problem.id,
            input_data="260000\n4\n20000 5\n30000 2\n10000 6\n5000 8",
            output_data="Yes"
        )
        
        test_case35 = TestCase(
            problem_id=receipt_problem.id,
            input_data="250000\n4\n20000 5\n30000 2\n10000 6\n5000 8",
            output_data="No"
        )
        
        test_case36 = TestCase(
            problem_id=receipt_problem.id,
            input_data="1000000\n2\n500000 1\n500000 1",
            output_data="Yes"
        )
        
        # 별 찍기 문제에 대한 테스트 케이스 추가
        test_case37 = TestCase(
            problem_id=star_problem.id,
            input_data="5",
            output_data="*\n**\n***\n****\n*****"
        )
        
        test_case38 = TestCase(
            problem_id=star_problem.id,
            input_data="3",
            output_data="*\n**\n***"
        )
        
        test_case39 = TestCase(
            problem_id=star_problem.id,
            input_data="1",
            output_data="*"
        )
        
        # (배열)개수 세기 문제에 대한 테스트 케이스 추가
        test_case40 = TestCase(
            problem_id=count_problem.id,
            input_data="11\n1 4 1 2 4 2 4 2 3 4 4\n2",
            output_data="3"
        )
        
        test_case41 = TestCase(
            problem_id=count_problem.id,
            input_data="11\n1 4 1 2 4 2 4 2 3 4 4\n5",
            output_data="0"
        )
        
        test_case42 = TestCase(
            problem_id=count_problem.id,
            input_data="5\n1 2 3 4 5\n1",
            output_data="1"
        )
        
        # (배열)X보다 작은 수 문제에 대한 테스트 케이스 추가
        test_case43 = TestCase(
            problem_id=less_than_x_problem.id,
            input_data="10 5\n1 10 4 9 2 3 8 5 7 6",
            output_data="1 4 2 3"
        )
        
        test_case44 = TestCase(
            problem_id=less_than_x_problem.id,
            input_data="5 3\n1 2 3 4 5",
            output_data="1 2"
        )
        
        test_case45 = TestCase(
            problem_id=less_than_x_problem.id,
            input_data="8 10\n1 5 2 8 9 3 7 6",
            output_data="1 5 2 8 9 3 7 6"
        )
        
        # (배열)공 넣기 문제에 대한 테스트 케이스 추가
        test_case46 = TestCase(
            problem_id=put_ball_problem.id,
            input_data="5 4\n1 2 3\n3 4 4\n1 4 1\n2 2 2",
            output_data="1 2 1 1 0"
        )
        
        test_case47 = TestCase(
            problem_id=put_ball_problem.id,
            input_data="3 3\n1 2 5\n2 3 7\n1 1 9",
            output_data="9 7 7"
        )
        
        test_case48 = TestCase(
            problem_id=put_ball_problem.id,
            input_data="4 2\n1 4 3\n2 3 1",
            output_data="3 1 1 3"
        )
        
        # (배열)공 바꾸기 문제에 대한 테스트 케이스 추가
        test_case49 = TestCase(
            problem_id=swap_ball_problem.id,
            input_data="5 4\n1 2\n3 4\n1 4\n2 2",
            output_data="3 1 4 2 5"
        )
        
        test_case50 = TestCase(
            problem_id=swap_ball_problem.id,
            input_data="3 2\n1 2\n2 3",
            output_data="2 3 1"
        )
        
        test_case51 = TestCase(
            problem_id=swap_ball_problem.id,
            input_data="4 4\n1 4\n2 3\n1 2\n3 4",
            output_data="3 4 1 2"
        )
        
        # (배열)평균 문제에 대한 테스트 케이스 추가
        test_case52 = TestCase(
            problem_id=avg_problem.id,
            input_data="3\n40 80 60",
            output_data="75.0"
        )
        
        test_case53 = TestCase(
            problem_id=avg_problem.id,
            input_data="3\n10 20 30",
            output_data="66.666667"
        )
        
        test_case54 = TestCase(
            problem_id=avg_problem.id,
            input_data="4\n1 100 100 100",
            output_data="75.25"
        )
        
        test_case55 = TestCase(
            problem_id=avg_problem.id,
            input_data="5\n1 2 4 8 16",
            output_data="38.75"
        )
        
        test_case56 = TestCase(
            problem_id=avg_problem.id,
            input_data="2\n3 10",
            output_data="65.0"
        )
        
        test_case57 = TestCase(
            problem_id=avg_problem.id,
            input_data="4\n10 20 0 100",
            output_data="32.5"
        )
        
        test_case58 = TestCase(
            problem_id=avg_problem.id,
            input_data="1\n50",
            output_data="100.0"
        )
        
        test_case59 = TestCase(
            problem_id=avg_problem.id,
            input_data="9\n10 20 30 40 50 60 70 80 90",
            output_data="55.55555555555556"
        )
        
        # (문자열)문자와 문자열 문제에 대한 테스트 케이스 추가
        test_case60 = TestCase(
            problem_id=char_in_string_problem.id,
            input_data="Sprout\n3",
            output_data="r"
        )
        
        test_case61 = TestCase(
            problem_id=char_in_string_problem.id,
            input_data="shiftpsh\n6",
            output_data="p"
        )
        
        test_case62 = TestCase(
            problem_id=char_in_string_problem.id,
            input_data="Baekjoon\n4",
            output_data="k"
        )
        
        # (문자열)단어 길이 재기 문제에 대한 테스트 케이스 추가
        test_case63 = TestCase(
            problem_id=word_length_problem.id,
            input_data="pulljima",
            output_data="8"
        )
        
        test_case64 = TestCase(
            problem_id=word_length_problem.id,
            input_data="Sprout",
            output_data="6"
        )
        
        test_case65 = TestCase(
            problem_id=word_length_problem.id,
            input_data="abcdefghijklmnopqrstuvwxyz",
            output_data="26"
        )
        
        # (문자열)문자열 문제에 대한 테스트 케이스 추가
        test_case66 = TestCase(
            problem_id=first_last_problem.id,
            input_data="3\nACDKJFOWIEGHE\nO\nAB",
            output_data="AE\nOO\nAB"
        )
        
        test_case67 = TestCase(
            problem_id=first_last_problem.id,
            input_data="2\nHELLO\nZ",
            output_data="HO\nZZ"
        )
        
        test_case68 = TestCase(
            problem_id=first_last_problem.id,
            input_data="1\nXYZ",
            output_data="XZ"
        )
        
        # (문자열)숫자의 합 문제에 대한 테스트 케이스 추가
        test_case69 = TestCase(
            problem_id=sum_of_digits_problem.id,
            input_data="1\n1",
            output_data="1"
        )
        
        test_case70 = TestCase(
            problem_id=sum_of_digits_problem.id,
            input_data="5\n54321",
            output_data="15"
        )
        
        test_case71 = TestCase(
            problem_id=sum_of_digits_problem.id,
            input_data="25\n7000000000000000000000000",
            output_data="7"
        )
        
        test_case72 = TestCase(
            problem_id=sum_of_digits_problem.id,
            input_data="11\n10987654321",
            output_data="46"
        )
        
        # (브루트 포스)블랙잭 문제에 대한 테스트 케이스 추가
        test_case73 = TestCase(
            problem_id=blackjack_problem.id,
            input_data="5 21\n5 6 7 8 9",
            output_data="21"
        )
        
        test_case74 = TestCase(
            problem_id=blackjack_problem.id,
            input_data="10 500\n93 181 245 214 315 36 185 138 216 295",
            output_data="497"
        )
        
        test_case75 = TestCase(
            problem_id=blackjack_problem.id,
            input_data="5 100\n5 10 15 20 25",
            output_data="60"
        )
        
        # (브루트 포스)분해합 문제에 대한 테스트 케이스 추가
        test_case76 = TestCase(
            problem_id=decompose_problem.id,
            input_data="216",
            output_data="198"
        )
        
        test_case77 = TestCase(
            problem_id=decompose_problem.id,
            input_data="101",
            output_data="91"
        )
        
        test_case78 = TestCase(
            problem_id=decompose_problem.id,
            input_data="1",
            output_data="0"
        )
        
        # (브루트 포스)체스판 다시 칠하기 문제에 대한 테스트 케이스 추가
        test_case80 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="8 8\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBBBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBWBWBW",
            output_data="1"
        )
        
        test_case81 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="10 13\nBBBBBBBBWBWBW\nBBBBBBBBBWBWB\nBBBBBBBBWBWBW\nBBBBBBBBBWBWB\nBBBBBBBBWBWBW\nBBBBBBBBBWBWB\nBBBBBBBBWBWBW\nBBBBBBBBBWBWB\nWWWWWWWWWWBWB\nWWWWWWWWWWBWB",
            output_data="12"
        )
        
        test_case82 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="8 8\nBWBWBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB",
            output_data="0"
        )
        
        test_case83 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="9 23\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBB\nBBBBBBBBBBBBBBBBBBBBBBW",
            output_data="31"
        )
        
        test_case84 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="10 10\nBBBBBBBBBB\nBBWBWBWBWB\nBWBWBWBWBB\nBBWBWBWBWB\nBWBWBWBWBB\nBBWBWBWBWB\nBWBWBWBWBB\nBBWBWBWBWB\nBWBWBWBWBB\nBBBBBBBBBB",
            output_data="0"
        )
        
        test_case85 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="8 8\nWBWBWBWB\nBWBWBWBW\nWBWBWBWB\nBWBBBWBW\nWBWBWBWB\nBWBWBWBW\nWBWBWWWB\nBWBWBWBW",
            output_data="2"
        )
        
        test_case86 = TestCase(
            problem_id=chess_repaint_problem.id,
            input_data="11 12\nBWWBWWBWWBWW\nBWWBWBBWWBWW\nWBWWBWBBWWBW\nBWWBWBBWWBWW\nWBWWBWBBWWBW\nBWWBWBBWWBWW\nWBWWBWBBWWBW\nBWWBWBWWWBWW\nWBWWBWBBWWBW\nBWWBWBBWWBWW\nWBWWBWBBWWBW",
            output_data="15"
        )
        
        # (정렬)대표값 문제의 테스트 케이스
        test_case94 = TestCase(
            problem_id=representative_value_problem.id,
            input_data="10\n40\n30\n60\n30",
            output_data="34\n30"
        )
        db.session.add(test_case94)

        test_case95 = TestCase(
            problem_id=representative_value_problem.id,
            input_data="10\n20\n30\n40\n50",
            output_data="30\n30"
        )
        db.session.add(test_case95)

        test_case96 = TestCase(
            problem_id=representative_value_problem.id,
            input_data="40\n40\n40\n40\n40",
            output_data="40\n40"
        )
        db.session.add(test_case96)

        # (정렬)단어 정렬 문제의 테스트 케이스
        test_case97 = TestCase(
            problem_id=word_sort_problem.id,
            input_data="13\nbut\ni\nwont\nhesitate\nno\nmore\nno\nmore\nit\ncannot\nwait\nim\nyours",
            output_data="i\nim\nit\nno\nbut\nmore\nwait\nwont\nyours\ncannot\nhesitate"
        )
        db.session.add(test_case97)

        test_case98 = TestCase(
            problem_id=word_sort_problem.id,
            input_data="5\naa\nbb\ncc\naa\nbb",
            output_data="aa\nbb\ncc"
        )
        db.session.add(test_case98)

        test_case99 = TestCase(
            problem_id=word_sort_problem.id,
            input_data="5\nword\nwords\nwordsmith\nwordsmithery\nw",
            output_data="w\nword\nwords\nwordsmith\nwordsmithery"
        )
        db.session.add(test_case99)

        # (자료구조)스택 문제의 테스트 케이스
        test_case100 = TestCase(
            problem_id=stack_problem.id,
            input_data="9\n4\n1 3\n1 5\n3\n2\n5\n2\n2\n5",
            output_data="1\n2\n5\n3\n3\n-1\n-1"
        )
        db.session.add(test_case100)


        # (자료구조)큐 문제의 테스트 케이스
        test_case103 = TestCase(
            problem_id=queue_problem.id,
            input_data="15\npush 1\npush 2\nfront\nback\nsize\nempty\npop\npop\npop\nsize\nempty\npop\npush 3\nempty\nfront",
            output_data="1\n2\n2\n0\n1\n2\n-1\n0\n1\n-1\n0\n3"
        )
        db.session.add(test_case103)

        test_case104 = TestCase(
            problem_id=queue_problem.id,
            input_data="8\npush 1\npush 2\npush 3\nfront\nback\nsize\npop\nsize",
            output_data="1\n3\n3\n1\n2"
        )
        db.session.add(test_case104)

        test_case105 = TestCase(
            problem_id=queue_problem.id,
            input_data="10\nsize\nempty\nfront\nback\npop\npush 3\nfront\nback\nsize\npop",
            output_data="0\n1\n-1\n-1\n-1\n3\n3\n1\n3"
        )
        db.session.add(test_case105)

        # (그리디 알고리즘)동전 문제의 테스트 케이스
        test_case106 = TestCase(
            problem_id=coin_problem.id,
            input_data="10 4200\n1\n5\n10\n50\n100\n500\n1000\n5000\n10000\n50000",
            output_data="6"
        )
        db.session.add(test_case106)

        test_case107 = TestCase(
            problem_id=coin_problem.id,
            input_data="10 4790\n1\n5\n10\n50\n100\n500\n1000\n5000\n10000\n50000",
            output_data="12"
        )
        db.session.add(test_case107)

        test_case108 = TestCase(
            problem_id=coin_problem.id,
            input_data="2 1000\n1\n5",
            output_data="200"
        )
        db.session.add(test_case108)

        # (이분 탐색)수 찾기 문제의 테스트 케이스
        test_case109 = TestCase(
            problem_id=binary_search_problem.id,
            input_data="5\n4 1 5 2 3\n5\n1 3 7 9 5",
            output_data="1\n1\n0\n0\n1"
        )
        db.session.add(test_case109)

        test_case110 = TestCase(
            problem_id=binary_search_problem.id,
            input_data="10\n6 3 2 10 10 10 -10 -10 7 3\n8\n10 9 -5 2 3 4 5 -10",
            output_data="1\n0\n0\n1\n1\n0\n0\n1"
        )
        db.session.add(test_case110)

        test_case111 = TestCase(
            problem_id=binary_search_problem.id,
            input_data="3\n1 2 3\n3\n1 2 4",
            output_data="1\n1\n0"
        )
        db.session.add(test_case111)

        # (자료구조)트리의 부모 찾기 문제의 테스트 케이스
        test_case112 = TestCase(
            problem_id=tree_parent_problem.id,
            input_data="7\n1 6\n6 3\n3 5\n4 1\n2 4\n4 7",
            output_data="4\n6\n1\n3\n1\n4"
        )
        db.session.add(test_case112)

        test_case113 = TestCase(
            problem_id=tree_parent_problem.id,
            input_data="12\n1 2\n1 3\n2 4\n3 5\n3 6\n4 7\n4 8\n5 9\n5 10\n6 11\n6 12",
            output_data="1\n1\n2\n3\n3\n4\n4\n5\n5\n6\n6"
        )
        db.session.add(test_case113)

        test_case114 = TestCase(
            problem_id=tree_parent_problem.id,
            input_data="5\n1 2\n2 3\n3 4\n4 5",
            output_data="1\n2\n3\n4"
        )
        db.session.add(test_case114)

        # 데이터베이스에 테스트 케이스 저장
        db.session.add(test_case1)
        db.session.add(test_case2)
        db.session.add(test_case3)
        db.session.add(test_case4)
        db.session.add(test_case5)
        db.session.add(test_case6)
        db.session.add(test_case7)
        db.session.add(test_case8)
        db.session.add(test_case9)
        db.session.add(test_case10)
        db.session.add(test_case11)
        db.session.add(test_case12)
        db.session.add(test_case13)
        db.session.add(test_case14)
        db.session.add(test_case15)
        db.session.add(test_case16)
        db.session.add(test_case17)
        db.session.add(test_case18)
        db.session.add(test_case19)
        db.session.add(test_case20)
        db.session.add(test_case21)
        db.session.add(test_case22)
        db.session.add(test_case23)
        db.session.add(test_case24)
        db.session.add(test_case25)
        db.session.add(test_case26)
        db.session.add(test_case27)
        db.session.add(test_case28)
        db.session.add(test_case29)
        db.session.add(test_case30)
        db.session.add(test_case31)
        db.session.add(test_case32)
        db.session.add(test_case33)
        db.session.add(test_case34)
        db.session.add(test_case35)
        db.session.add(test_case36)
        db.session.add(test_case37)
        db.session.add(test_case38)
        db.session.add(test_case39)
        db.session.add(test_case40)
        db.session.add(test_case41)
        db.session.add(test_case42)
        db.session.add(test_case43)
        db.session.add(test_case44)
        db.session.add(test_case45)
        db.session.add(test_case46)
        db.session.add(test_case47)
        db.session.add(test_case48)
        db.session.add(test_case49)
        db.session.add(test_case50)
        db.session.add(test_case51)
        db.session.add(test_case52)
        db.session.add(test_case53)
        db.session.add(test_case54)
        db.session.add(test_case55)
        db.session.add(test_case56)
        db.session.add(test_case57)
        db.session.add(test_case58)
        db.session.add(test_case59)
        db.session.add(test_case60)
        db.session.add(test_case61)
        db.session.add(test_case62)
        db.session.add(test_case63)
        db.session.add(test_case64)
        db.session.add(test_case65)
        db.session.add(test_case66)
        db.session.add(test_case67)
        db.session.add(test_case68)
        db.session.add(test_case69)
        db.session.add(test_case70)
        db.session.add(test_case71)
        db.session.add(test_case72)
        db.session.add(test_case73)
        db.session.add(test_case74)
        db.session.add(test_case75)
        db.session.add(test_case76)
        db.session.add(test_case77)
        db.session.add(test_case78)
        db.session.add(test_case80)
        db.session.add(test_case81)
        db.session.add(test_case82)
        db.session.add(test_case83)
        db.session.add(test_case84)
        db.session.add(test_case85)
        db.session.add(test_case86)
        db.session.add(test_case94)
        db.session.add(test_case95)
        db.session.add(test_case96)
        db.session.add(test_case97)
        db.session.add(test_case98)
        db.session.add(test_case99)
        db.session.add(test_case100)
        db.session.add(test_case103)
        db.session.add(test_case104)
        db.session.add(test_case105)
        db.session.add(test_case106)
        db.session.add(test_case107)
        db.session.add(test_case108)
        db.session.add(test_case109)
        db.session.add(test_case110)
        db.session.add(test_case111)
        db.session.add(test_case112)
        db.session.add(test_case113)
        db.session.add(test_case114)
        db.session.commit()
        
        print("문제와 테스트 케이스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    init_problems_with_testcases() 