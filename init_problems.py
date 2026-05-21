from app import app, db
from models import Problem

def init_problems():
    with app.app_context():
        # 기존 문제가 있는지 확인하고 모두 삭제
        existing_problems = Problem.query.all()
        if existing_problems:
            for problem in existing_problems:
                db.session.delete(problem)
            db.session.commit()
            print("기존 문제가 모두 삭제되었습니다.")
            
        # 1단계: Hello World 문제 생성
        problem1 = Problem(
            title="[1단계] Hello World",
            description="'Hello, World!'를 출력하는 프로그램을 작성하세요.",
            input_spec="입력은 없습니다.",
            output_spec="'Hello, World!'를 출력하세요.",
            time_limit=1,  # 1초
            memory_limit=128,  # 128MB
            checker="default",  # 기본 체커
            sample_input="",  # 입력 없음
            sample_output="Hello, World!"  # 예시 출력
        )
        
        # 1단계: A+B 문제 생성
        problem2 = Problem(
            title="[1단계] A+B",
            description="두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 A와 B가 주어집니다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A+B를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="1 2",
            sample_output="3"
        )
        
        # 1단계: A-B 문제 생성
        problem3 = Problem(
            title="[1단계] A-B",
            description="두 정수 A와 B를 입력받은 다음, A-B를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 A와 B가 주어집니다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A-B를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3 2",
            sample_output="1"
        )
        
        # 1단계: A*B 문제 생성
        problem4 = Problem(
            title="[1단계] A*B",
            description="두 정수 A와 B를 입력받은 다음, A×B를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 A와 B가 주어집니다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A×B를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3 4",
            sample_output="12"
        )
        
        # 1단계: A/B 문제 생성
        problem5 = Problem(
            title="[1단계] A/B",
            description="두 정수 A와 B를 입력받은 다음, A/B를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 A와 B가 주어집니다. (0 < A, B < 10)",
            output_spec="첫째 줄에 A/B를 출력하세요. 실제 정답과 출력값의 절대오차 또는 상대오차가 10^-9 이하이면 정답입니다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="4 5",
            sample_output="0.8"
        )
        
        # 1단계: 사칙연산 문제 생성
        problem6 = Problem(
            title="[1단계] 사칙연산",
            description="두 자연수 A와 B가 주어진다. 이때, A+B, A-B, A*B, A/B(몫)을 출력하는 프로그램을 작성하세요.",
            input_spec="두 자연수 A와 B가 주어집니다. (1 ≤ A, B ≤ 10,000)",
            output_spec="첫째 줄에 A+B, 둘째 줄에 A-B, 셋째 줄에 A*B, 넷째 줄에 A/B(몫)을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="7 3",
            sample_output="10\n4\n21\n2"
        )
        
        # 2단계: 두 수 비교하기 문제 생성
        problem7 = Problem(
            title="[2단계] 두 수 비교하기",
            description="두 정수 A와 B가 주어졌을 때, A와 B를 비교하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 A와 B가 주어집니다. (-10,000 ≤ A, B ≤ 10,000)",
            output_spec="첫째 줄에 다음 세 가지 중 하나를 출력하세요.\n- A가 B보다 큰 경우에는 '>'를 출력합니다.\n- A가 B보다 작은 경우에는 '<'를 출력합니다.\n- A와 B가 같은 경우에는 '=='를 출력합니다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="1 2",
            sample_output="<"
        )
        
        # 2단계: 시험 성적 문제 생성
        problem8 = Problem(
            title="[2단계] 시험 성적",
            description="시험 점수를 입력받아 90 ~ 100점은 A, 80 ~ 89점은 B, 70 ~ 79점은 C, 60 ~ 69점은 D, 나머지 점수는 F를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 시험 점수가 주어집니다. 시험 점수는 0보다 크거나 같고, 100보다 작거나 같은 정수입니다.",
            output_spec="시험 성적을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="85",
            sample_output="B"
        )
        
        # 2단계: 윤년 문제 생성
        problem9 = Problem(
            title="[2단계] 윤년",
            description="연도가 주어졌을 때, 윤년이면 1, 아니면 0을 출력하는 프로그램을 작성하세요.\n\n윤년은 연도가 4의 배수이면서, 100의 배수가 아닐 때 또는 400의 배수일 때입니다.",
            input_spec="첫째 줄에 연도가 주어집니다. 연도는 1보다 크거나 같고, 4000보다 작거나 같은 자연수입니다.",
            output_spec="첫째 줄에 윤년이면 1, 아니면 0을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="2000",
            sample_output="1"
        )
        
        # 2단계: 사분면 고르기 문제 생성
        problem10 = Problem(
            title="[2단계] 사분면 고르기",
            description="점의 좌표를 입력받아 그 점이 어느 사분면에 속하는지 알아내는 프로그램을 작성하세요.\n\n사분면은 아래와 같이 1부터 4까지 번호를 갖습니다.\n- 제1사분면: x좌표와 y좌표가 모두 양수\n- 제2사분면: x좌표가 음수, y좌표가 양수\n- 제3사분면: x좌표와 y좌표가 모두 음수\n- 제4사분면: x좌표가 양수, y좌표가 음수",
            input_spec="첫 줄에는 정수 x가 주어집니다. 다음 줄에는 정수 y가 주어집니다. (-1000 ≤ x, y ≤ 1000; x, y ≠ 0)",
            output_spec="점 (x, y)의 사분면 번호(1, 2, 3, 4 중 하나)를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="12\n5",
            sample_output="1"
        )
        
        # 2단계: 알람 시계 문제 생성
        problem11 = Problem(
            title="[2단계] 알람 시계",
            description="상근이는 매일 아침 알람을 듣고 일어납니다. 알람을 설정할 때, 시간을 설정하면 알람이 울리는 시간을 계산하는 프로그램을 작성하세요.\n\n현재 상근이가 설정한 알람 시각이 주어질 때, 45분 일찍 알람을 설정하면 알람이 울리는 시각을 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 두 정수 H와 M이 주어집니다. (0 ≤ H ≤ 23, 0 ≤ M ≤ 59) 그리고 이것은 현재 설정한 알람 시간 H시 M분을 의미합니다.",
            output_spec="첫째 줄에 상근이가 설정해야 하는 알람 시간을 출력하세요. (입력과 같은 형태로 출력하면 됩니다.)",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10 10",
            sample_output="9 25"
        )
        
        # 3단계: 구구단 문제 생성
        problem12 = Problem(
            title="[3단계] 구구단",
            description="N을 입력받은 뒤, 구구단 N단을 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 N이 주어집니다. N은 1보다 크거나 같고, 9보다 작거나 같습니다.",
            output_spec="출력형식과 같게 N*1부터 N*9까지 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="2",
            sample_output="2 * 1 = 2\n2 * 2 = 4\n2 * 3 = 6\n2 * 4 = 8\n2 * 5 = 10\n2 * 6 = 12\n2 * 7 = 14\n2 * 8 = 16\n2 * 9 = 18"
        )
        
        # 3단계: A+B - 3 문제 생성
        problem13 = Problem(
            title="[3단계] A+B - 3",
            description="두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 테스트 케이스의 개수 T가 주어집니다.\n\n각 테스트 케이스는 한 줄로 이루어져 있으며, 각 줄에 A와 B가 주어집니다. (0 < A, B < 10)",
            output_spec="각 테스트 케이스마다 A+B를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n1 1\n2 3\n3 4\n9 8\n5 2",
            sample_output="2\n5\n7\n17\n7"
        )
        
        # 3단계: 합 문제 생성
        problem14 = Problem(
            title="[3단계] 합",
            description="n이 주어졌을 때, 1부터 n까지 합을 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 n (1 ≤ n ≤ 10,000)이 주어집니다.",
            output_spec="1부터 n까지 합을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3",
            sample_output="6"
        )
        
        # 3단계: 별찍기 문제 생성
        problem15 = Problem(
            title="[3단계] 별찍기",
            description="첫째 줄에는 별 1개, 둘째 줄에는 별 2개, N번째 줄에는 별 N개를 찍는 문제",
            input_spec="첫째 줄에 N(1 ≤ N ≤ 100)이 주어집니다.",
            output_spec="첫째 줄부터 N번째 줄까지 차례대로 별을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5",
            sample_output="*\n**\n***\n****\n*****"
        )
        
        # 4단계: 개수 세기 문제 생성
        problem16 = Problem(
            title="[4단계] 개수 세기",
            description="총 N개의 정수가 주어졌을 때, 정수 v가 몇 개인지 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 정수의 개수 N(1 ≤ N ≤ 100)이 주어집니다.\n둘째 줄에는 정수가 공백으로 구분되어져있습니다.\n셋째 줄에는 찾으려고 하는 정수 v가 주어집니다.\n입력으로 주어지는 정수와 v는 -100보다 크거나 같으며, 100보다 작거나 같습니다.",
            output_spec="첫째 줄에 입력으로 주어진 N개의 정수 중에 v가 몇 개인지 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="11\n1 4 1 2 4 2 4 2 3 4 4\n4",
            sample_output="5"
        )
        
        # 4단계: 최소, 최대 문제 생성
        problem17 = Problem(
            title="[4단계] 최소, 최대",
            description="N개의 정수가 주어진다. 이때, 최솟값과 최댓값을 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 정수의 개수 N (1 ≤ N ≤ 1,000,000)이 주어집니다.\n둘째 줄에는 N개의 정수를 공백으로 구분해서 주어집니다.\n모든 정수는 -1,000,000보다 크거나 같고, 1,000,000보다 작거나 같은 정수입니다.",
            output_spec="첫째 줄에 주어진 정수 N개의 최솟값과 최댓값을 공백으로 구분해 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n20 10 35 30 7",
            sample_output="7 35"
        )
        
        # 4단계: 최대값 문제 생성
        problem18 = Problem(
            title="[4단계] 최대값",
            description="9개의 서로 다른 자연수가 주어질 때, 이들 중 최댓값을 찾고 그 최댓값이 몇 번째 수인지를 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄부터 아홉 번째 줄까지 한 줄에 하나의 자연수가 주어집니다. 주어지는 자연수는 100보다 작은 자연수입니다.",
            output_spec="첫째 줄에 최댓값을 출력하고, 둘째 줄에 최댓값이 몇 번째 수인지를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3\n29\n38\n12\n57\n74\n40\n85\n61",
            sample_output="85\n8"
        )
        
        # 4단계: 공 넣기 문제 생성
        problem19 = Problem(
            title="[4단계] 공 넣기",
            description="도현이는 바구니를 총 N개 가지고 있다. 각각의 바구니에는 1번부터 N번까지 번호가 매겨져 있다. 또, 1번부터 N번까지 번호가 적혀있는 공을 매우 많이 가지고 있다. 가장 처음에는 바구니에 공이 들어있지 않으며, 바구니에는 공을 1개만 넣을 수 있다.\n\n도현이는 앞으로 M번 공을 넣으려고 한다. 도현이는 한 번 공을 넣을 때, 공을 넣을 바구니 범위를 정하고, 정한 바구니에 모두 같은 번호가 적혀있는 공을 넣는다. 이때, 공을 넣을 바구니는 연속되어 있어야 한다.\n\n공을 어떻게 넣을지가 주어졌을 때, M번 공을 넣은 이후에 각 바구니에 어떤 공이 들어 있는지 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 N (1 ≤ N ≤ 100)과 M (1 ≤ M ≤ 100)이 주어집니다.\n\n둘째 줄부터 M개의 줄에 걸쳐서 공을 넣는 방법이 주어집니다. 각 방법은 세 정수 i j k로 이루어져 있으며, i번 바구니부터 j번 바구니까지에 k번 번호가 적혀있는 공을 넣는다는 뜻입니다. (1 ≤ i ≤ j ≤ N, 1 ≤ k ≤ N)",
            output_spec="1번 바구니부터 N번 바구니에 들어있는 공의 번호를 공백으로 구분해 출력하세요. 공이 들어있지 않은 바구니는 0을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 4\n1 2 3\n3 4 4\n1 4 1\n2 2 2",
            sample_output="1 2 1 4 0"
        )
        
        # 4단계: 공 바꾸기 문제 생성
        problem20 = Problem(
            title="[4단계] 공 바꾸기",
            description="도현이는 바구니를 총 N개 가지고 있고, 각각의 바구니에는 1번부터 N번까지 번호가 매겨져 있다. 바구니에는 공이 1개씩 들어있고, 처음에는 바구니에 적혀있는 번호와 같은 번호가 적힌 공이 들어있다.\n\n도현이는 앞으로 M번 공을 바꾸려고 한다. 도현이는 공을 바꿀 바구니 2개를 선택하고, 두 바구니에 들어있는 공을 서로 교환한다.\n\n공을 어떻게 바꿀지가 주어졌을 때, M번 공을 바꾼 이후에 각 바구니에 어떤 공이 들어있는지 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 N (1 ≤ N ≤ 100)과 M (1 ≤ M ≤ 100)이 주어집니다.\n\n둘째 줄부터 M개의 줄에 걸쳐서 공을 교환할 방법이 주어집니다. 각 방법은 두 정수 i j로 이루어져 있으며, i번 바구니와 j번 바구니에 들어있는 공을 교환한다는 뜻입니다. (1 ≤ i ≤ j ≤ N)",
            output_spec="1번 바구니부터 N번 바구니에 들어있는 공의 번호를 공백으로 구분해 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 4\n1 2\n3 4\n1 4\n2 2",
            sample_output="3 1 4 2 5"
        )
        
        # 5단계: 행렬 덧셈 문제 생성
        problem21 = Problem(
            title="[5단계] 행렬 덧셈",
            description="N*M 크기의 두 행렬 A와 B가 주어졌을 때, 두 행렬을 더하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 행렬의 크기 N과 M이 주어집니다. 둘째 줄부터 N개의 줄에 행렬 A의 원소 M개가 차례대로 주어지고, 이어서 N개의 줄에 행렬 B의 원소 M개가 차례대로 주어집니다. N과 M은 100보다 작거나 같고, 행렬의 원소는 절댓값이 100보다 작거나 같은 정수입니다.",
            output_spec="첫째 줄부터 N개의 줄에 행렬 A와 B를 더한 행렬을 출력하세요. 행렬의 각 원소는 공백으로 구분합니다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3 3\n1 1 1\n2 2 2\n0 1 0\n3 3 3\n4 4 4\n5 5 100",
            sample_output="4 4 4\n6 6 6\n5 6 100"
        )
        
        # 5단계: 최댓값 문제 생성
        problem22 = Problem(
            title="[5단계] 최댓값",
            description="9×9 격자판에 쓰여진 81개의 자연수가 주어질 때, 이들 중 최댓값을 찾고 그 최댓값이 몇 행 몇 열에 위치한 수인지를 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄부터 아홉 번째 줄까지 한 줄에 아홉 개씩 수가 주어집니다. 주어지는 수는 100보다 작은 자연수입니다.",
            output_spec="첫째 줄에 최댓값을 출력하고, 둘째 줄에 최댓값이 위치한 행 번호와 열 번호를 공백으로 구분해 출력하세요. 행과 열의 번호는 1부터 시작합니다. 최댓값이 여러 개인 경우 그 중 한 곳의 위치를 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="3 23 85 34 17 74 25 52 65\n10 7 39 42 88 52 14 72 63\n87 42 18 78 53 45 18 84 53\n34 28 64 85 12 16 75 36 55\n21 77 45 35 28 75 90 76 1\n25 87 65 15 28 11 37 28 74\n65 27 75 41 7 89 78 64 39\n47 47 70 45 23 65 3 41 44\n87 13 82 38 31 12 29 29 80",
            sample_output="90\n5 7"
        )
        
        # 5단계: 세로읽기 문제 생성
        problem23 = Problem(
            title="[5단계] 세로읽기",
            description="아직 최백준은 아름다운 세계의 세로읽기를 해보지 못했다. 창영이가 세로로 써놓은 글자를 읽어보자.\n\n총 다섯줄의 입력이 주어진다. 각 줄에는 최소 1개, 최대 15개의 글자들이 빈칸 없이 연속으로 주어진다. 주어지는 글자는 영어 대소문자, 숫자, 기호로만 이루어져 있다.\n\n이 글자들을 세로로 읽으려 한다. 이를 위해서는 각 줄의 길이가 같아야 하는데, 글자가 부족한 경우는 빈칸으로 생각한다.",
            input_spec="총 다섯 줄의 입력이 주어진다. 각 줄에는 최소 1개, 최대 15개의 글자들이 빈칸 없이 연속으로 주어진다. 주어지는 글자는 영어 대소문자, 숫자, 기호로만 이루어져 있다.",
            output_spec="영어 대소문자, 숫자, 기호로 이루어진 세로읽기한 문자열을 출력한다. 단, 글자가 없는 자리는 읽지 않는다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="ABCDE\nabcde\n01234\nFGHIJ\nfghij",
            sample_output="Aa0Ff\nBb1Gg\nCc2Hh\nDd3Ii\nEe4Jj"
        )
        
        # 6단계: 수 정렬하기 문제 생성
        problem24 = Problem(
            title="[6단계] 수 정렬하기",
            description="N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 수의 개수 N(1 ≤ N ≤ 1,000)이 주어집니다. 둘째 줄부터 N개의 줄에는 수가 주어집니다. 이 수는 절댓값이 1,000보다 작거나 같은 정수입니다. 수는 중복되지 않습니다.",
            output_spec="첫째 줄부터 N개의 줄에 오름차순으로 정렬한 결과를 한 줄에 하나씩 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5\n5\n2\n3\n4\n1",
            sample_output="1\n2\n3\n4\n5"
        )
        
        # 6단계: 대표값 문제 생성
        problem25 = Problem(
            title="[6단계] 대표값",
            description="중앙값은 어떤 주어진 값들을 크기 순서대로 정렬했을 때 가장 중앙에 위치하는 값을 의미합니다. 예를 들어 1, 2, 7, 10, 11의 중앙값은 7입니다. 정렬했을 때 중앙값의 위치에 있는 값을 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄부터 다섯 개의 줄에 각 줄마다 자연수가 한 개씩 주어집니다. 주어지는 자연수는 100 이하입니다.",
            output_spec="첫째 줄에는 평균을 출력하고, 둘째 줄에는 중앙값을 출력하세요. 평균과 중앙값은 모두 자연수이며, 평균은 소수점 이하를 버림하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10\n40\n30\n60\n30",
            sample_output="34\n30"
        )
        
        # 6단계: 커트라인 문제 생성
        problem26 = Problem(
            title="[6단계] 커트라인",
            description="2022 연세대학교 미래캠퍼스 슬기로운 코딩생활에 N명의 학생들이 응시했다.\n\n이들 중 점수가 가장 높은 k명은 상을 받을 것이다. 이 때, 상을 받는 커트라인이 몇 점인지 구하라.\n\n커트라인이란 상을 받는 사람들 중 점수가 가장 낮은 사람의 점수를 말한다.",
            input_spec="첫째 줄에는 응시자의 수 N과 상을 받는 사람의 수 k가 공백을 사이에 두고 주어진다.\n\n둘째 줄에는 각 학생의 점수 x가 공백을 사이에 두고 주어진다.\n\n1 ≤ N ≤ 1,000\n1 ≤ k ≤ N\n0 ≤ x ≤ 10,000",
            output_spec="상을 받는 커트라인을 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 2\n100 76 85 93 98",
            sample_output="98"
        )
        
        # 6단계: 단어 정렬 문제 생성
        problem27 = Problem(
            title="[6단계] 단어 정렬",
            description="알파벳 소문자로 이루어진 N개의 단어가 들어오면 아래와 같은 조건에 따라 정렬하는 프로그램을 작성하세요.\n\n1. 길이가 짧은 것부터\n2. 길이가 같으면 사전 순으로\n\n단, 중복된 단어는 하나만 남기고 제거해야 합니다.",
            input_spec="첫째 줄에 단어의 개수 N이 주어진다. (1 ≤ N ≤ 20,000) 둘째 줄부터 N개의 줄에 걸쳐 알파벳 소문자로 이루어진 단어가 한 줄에 하나씩 주어진다. 주어지는 문자열의 길이는 50을 넘지 않는다.",
            output_spec="조건에 따라 정렬하여 단어들을 출력하세요. 단, 중복된 단어는 한 번만 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="13\nbut\ni\nwont\nhesitate\nno\nmore\nno\nmore\nit\ncannot\nwait\nim\nyours",
            sample_output="i\nim\nit\nno\nbut\nwont\nwait\nmore\nyours\ncannot\nhesitate"
        )
        
        # 7단계: 스택 문제 생성
        problem28 = Problem(
            title="[7단계] 스택",
            description="스택은 자료를 넣는 (push) 입구와 자료를 뽑는 (pop) 입구가 같아 제일 나중에 들어간 자료가 제일 먼저 나오는 (LIFO, Last in First out) 특성을 가지는 자료구조입니다.\n\n1부터 n까지의 수를 스택에 넣었다가 뽑아 늘어놓음으로써, 하나의 수열을 만들 수 있습니다. 이때, 스택에 push하는 순서는 반드시 오름차순을 지키도록 합니다. 임의의 수열이 주어졌을 때 스택을 이용해 그 수열을 만들 수 있는지 없는지, 있다면 어떤 순서로 push와 pop 연산을 수행해야 하는지를 알아낼 수 있습니다. 이를 계산하는 프로그램을 작성하세요.",
            input_spec="첫 줄에 n (1 ≤ n ≤ 100,000)이 주어집니다.\n둘째 줄부터 n개의 줄에는 수열을 이루는 1이상 n이하의 정수가 하나씩 순서대로 주어집니다. 물론 같은 정수가 두 번 나오는 일은 없습니다.",
            output_spec="입력된 수열을 만들기 위해 필요한 연산을 한 줄에 한 개씩 출력합니다. push연산은 +로, pop 연산은 -로 표현합니다. 불가능한 경우 NO를 출력합니다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="8\n4\n3\n6\n8\n7\n5\n2\n1",
            sample_output="+\n+\n+\n+\n-\n-\n+\n+\n-\n+\n+\n-\n-\n-\n-\n-"
        )
        
        # 7단계: 큐 문제 생성
        problem29 = Problem(
            title="[7단계] 큐",
            description="큐(queue)는 컴퓨터의 기본적인 자료구조 중 하나로, 먼저 집어넣은 데이터가 먼저 나오는 FIFO(First In First Out) 구조를 가집니다.\n\n이 문제에서는 큐를 구현하고 다음 명령을 처리하는 프로그램을 작성하세요:\n- push X: 정수 X를 큐에 넣는 연산입니다.\n- pop: 큐에서 가장 앞에 있는 정수를 빼고, 그 수를 출력합니다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력합니다.\n- size: 큐에 들어있는 정수의 개수를 출력합니다.\n- empty: 큐가 비어있으면 1, 아니면 0을 출력합니다.\n- front: 큐의 가장 앞에 있는 정수를 출력합니다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력합니다.\n- back: 큐의 가장 뒤에 있는 정수를 출력합니다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력합니다.",
            input_spec="첫째 줄에 주어지는 명령의 수 N (1 ≤ N ≤ 10,000)이 주어집니다. 둘째 줄부터 N개의 줄에는 명령이 하나씩 주어집니다. 주어지는 정수는 1보다 크거나 같고, 100,000보다 작거나 같습니다. 문제에 나와있지 않은 명령이 주어지는 경우는 없습니다.",
            output_spec="출력해야하는 명령이 주어질 때마다, 한 줄에 하나씩 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="15\npush 1\npush 2\nfront\nback\nsize\nempty\npop\npop\npop\nsize\nempty\npush 3\nempty\nfront\npop",
            sample_output="1\n2\n2\n0\n1\n2\n-1\n0\n1\n0\n3\n3"
        )
        
        # 7단계: 트리 문제 생성
        problem30 = Problem(
            title="[7단계] 트리",
            description="트리는 사이클이 없는 연결 그래프입니다. 트리에서는 어떤 두 노드를 선택해도 둘 사이에 경로가 항상 하나만 존재하게 됩니다.\n\n트리의 루트가 1번 노드인 루트 트리가 주어집니다. 각 노드의 부모 노드를 구하는 프로그램을 작성하세요.",
            input_spec="첫째 줄에 노드의 개수 N (2 ≤ N ≤ 100,000)이 주어집니다. 둘째 줄부터 N-1개의 줄에 트리 상에서 연결된 두 정점이 주어집니다. 주어지는 트리는 항상 올바른 트리입니다.",
            output_spec="첫째 줄부터 N-1개의 줄에 각 노드의 부모 노드 번호를 2번 노드부터 순서대로 출력하세요.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="7\n1 6\n6 3\n3 5\n4 1\n2 4\n4 7",
            sample_output="4\n6\n1\n3\n1\n4"
        )
        
        # 8단계: 그리디 알고리즘 문제 생성
        problem31 = Problem(
            title="[8단계] 그리디 알고리즘",
            description="준규가 가지고 있는 동전은 총 N종류이고, 각각의 동전을 매우 많이 가지고 있다.\n\n동전을 적절히 사용해서 그 가치의 합을 K로 만들려고 한다. 이때 필요한 동전 개수의 최솟값을 구하는 프로그램을 작성하시오.",
            input_spec="첫째 줄에 N과 K가 주어진다. (1 ≤ N ≤ 10, 1 ≤ K ≤ 100,000,000)\n\n둘째 줄부터 N개의 줄에 동전의 가치 Ai가 오름차순으로 주어진다. (1 ≤ Ai ≤ 1,000,000, A1 = 1, i ≥ 2인 경우에 Ai는 Ai-1의 배수)",
            output_spec="첫째 줄에 K원을 만드는데 필요한 동전 개수의 최솟값을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="10 4200\n1\n5\n10\n50\n100\n500\n1000\n5000\n10000\n50000",
            sample_output="6"
        )
        
        # 8단계: 브루트 포스 문제 생성
        problem32 = Problem(
            title="[8단계] 브루트 포스",
            description="블랙잭은 카지노에서 제일 인기 있는 게임이다. 블랙잭의 규칙은 상당히 쉽다. 카드의 합이 21을 넘지 않는 한도 내에서, 카드의 합을 최대한 크게 만드는 게임이다. 블랙잭은 카지노마다 다양한 규정이 있다.\n\n한국 최고의 블랙잭 고수 김정인은 새로운 블랙잭 규칙을 만들어 학생들과 게임하려고 한다.\n\n김정인 버전의 블랙잭에서 각 카드에는 양의 정수가 쓰여 있다. 그 다음, 딜러는 N장의 카드를 모두 숫자가 보이도록 바닥에 놓는다. 그런 후에 딜러는 숫자 M을 크게 외친다.\n\n이제 플레이어는 제한된 시간 안에 N장의 카드 중에서 3장의 카드를 골라야 한다. 블랙잭 변형 게임이기 때문에, 플레이어가 고른 카드의 합은 M을 넘지 않으면서 M과 최대한 가깝게 만들어야 한다.\n\nN장의 카드에 써져 있는 숫자가 주어졌을 때, M을 넘지 않으면서 M에 최대한 가까운 카드 3장의 합을 구해 출력하시오.",
            input_spec="첫째 줄에 카드의 개수 N(3 ≤ N ≤ 100)과 M(10 ≤ M ≤ 300,000)이 주어진다. 둘째 줄에는 카드에 쓰여 있는 수가 주어지며, 이 값은 100,000을 넘지 않는 양의 정수이다.\n\n합이 M을 넘지 않는 카드 3장을 찾을 수 있는 경우만 입력으로 주어진다.",
            output_spec="첫째 줄에 M을 넘지 않으면서 M에 최대한 가까운 카드 3장의 합을 출력한다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 21\n5 6 7 8 9",
            sample_output="21"
        )
        
        # 8단계: 이분 탐색 문제 생성
        problem33 = Problem(
            title="[8단계] 이분 탐색",
            description="수열 A가 주어졌을 때, 세 값 ai, aj, ak의 합이 M이 되는 경우의 수를 구하는 프로그램을 작성하시오. (1 ≤ i < j < k ≤ N)\n\n이 문제는 이분 탐색을 활용하여 해결할 수 있습니다.",
            input_spec="첫째 줄에 수열의 크기 N(3 ≤ N ≤ 5,000), 찾고자 하는 합 M(1 ≤ M ≤ 1,000,000,000)이 주어집니다.\n\n둘째 줄에는 N개의 정수로 된 수열이 주어집니다. 수열의 각 원소는 절댓값이 30,000을 넘지 않는 정수입니다.",
            output_spec="첫째 줄에 경우의 수를 출력합니다. 만약 경우의 수가 없으면 0을 출력합니다.",
            time_limit=1,
            memory_limit=128,
            checker="default",
            sample_input="5 21\n1 4 7 9 10",
            sample_output="2"
        )
        
        # 데이터베이스에 저장
        db.session.add(problem1)
        db.session.add(problem2)
        db.session.add(problem3)
        db.session.add(problem4)
        db.session.add(problem5)
        db.session.add(problem6)
        db.session.add(problem7)
        db.session.add(problem8)
        db.session.add(problem9)
        db.session.add(problem10)
        db.session.add(problem11)
        db.session.add(problem12)
        db.session.add(problem13)
        db.session.add(problem14)
        db.session.add(problem15)
        db.session.add(problem16)
        db.session.add(problem17)
        db.session.add(problem18)
        db.session.add(problem19)
        db.session.add(problem20)
        db.session.add(problem21)
        db.session.add(problem22)
        db.session.add(problem23)
        db.session.add(problem24)
        db.session.add(problem25)
        db.session.add(problem26)
        db.session.add(problem27)
        db.session.add(problem28)
        db.session.add(problem29)
        db.session.add(problem30)
        db.session.add(problem31)
        db.session.add(problem32)
        db.session.add(problem33)
        db.session.commit()
        print("문제가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    init_problems() 