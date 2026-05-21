from flask import Flask, render_template, redirect, url_for, request, session, flash, abort, Response, stream_with_context
from sqlalchemy import func, and_
from models import db, User, Problem, Submission, Post, TestCase
from judge import run_code
from config import Config
from utils import fetch_cf_tier, fetch_ac_tier, decrypt_id, validate_password
from markupsafe import Markup
from flask_migrate import Migrate
import json
from openai import OpenAI
import time
import openai
from collections import defaultdict

import threading

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

# Security middleware to block malicious requests
@app.before_request
def check_for_malicious_requests():
    # Check for suspicious patterns in the request URL or arguments
    suspicious_patterns = [
        'cmd=', 'wget', 'chmod', 'tftp', 'sh+', '.sh', 
        'device.rsp', 'uname', 'history+-c', 'rm+-rf'
    ]
    
    full_url = request.url
    if any(pattern in full_url for pattern in suspicious_patterns):
        # Log and block suspicious requests
        print(f"Blocked suspicious request on main app: {request.remote_addr} - {full_url}")
        abort(403)  # Forbidden

# Security exception handler
@app.errorhandler(403)
def main_app_forbidden(e):
    try:
        return render_template('error.html', error="Forbidden: Access Denied", code=403), 403
    except:
        # Fallback if error.html doesn't exist
        return "403 Forbidden: Access Denied", 403

# 앱 시작 시 DB 테이블 생성
with app.app_context():
    db.create_all()

# ─── 회원가입 ───────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('모든 필드를 입력해주세요.', 'warning')
        else:
            # 비밀번호 규칙 검증
            is_valid, error_message = validate_password(password)
            if not is_valid:
                flash(error_message, 'danger')
                return render_template('register.html')
                
            # 사용자명 중복 확인을 위해 모든 사용자를 가져와서 복호화하여 비교
            users = User.query.all()
            for user in users:
                if user.get_username() == username:
                    flash('이미 존재하는 사용자명입니다.', 'danger')
                    return render_template('register.html')
                    
            user = User()
            user.set_password(password)
            user.set_username(username)  # Encrypt username
            db.session.add(user)
            db.session.commit()
            flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# ─── 로그인 ───────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 모든 사용자를 가져와서 복호화된 사용자명으로 비교
        users = User.query.all()
        user = None
        for u in users:
            if u.get_username() == username:
                user = u
                break
                
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.get_username()
            # Store encrypted username in session for additional security
            session['encrypted_username'] = user.get_encrypted_username()
            flash(f'{user.get_username()}님 환영합니다!', 'success')
            return redirect(url_for('index'))
        flash('아이디 또는 비밀번호가 틀렸습니다.', 'danger')
    return render_template('login.html')

# ─── 로그아웃 ─────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('encrypted_username', None)
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('login'))

# ─── 메인 화면 ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─── 문제 목록 (페이징 + 상태별 색상) ────────────────────────────────────────
@app.route('/problems')
def problems():
    page     = request.args.get('page', 1, type=int)
    per_page = 14
    pagination = Problem.query.order_by(Problem.id) \
                     .paginate(page=page, per_page=per_page, error_out=False)
    problems = pagination.items
    user_id  = session.get('user_id')

    stats = []
    # 미리 읽어두면 효율적
    if user_id:
        ac_ids    = {r.problem_id for r in Submission.query.filter_by(user_id=user_id, result='AC')}
        tried_ids = {r.problem_id for r in Submission.query.filter_by(user_id=user_id)}
    else:
        ac_ids = tried_ids = set()

    for p in problems:
        total = Submission.query.filter_by(problem_id=p.id).count()
        ac    = Submission.query.filter_by(problem_id=p.id, result='AC').count()
        rate  = f"{ac/total*100:.1f}%" if total else '0%'

        if user_id:
            if p.id in ac_ids:
                st = 'solved'
            elif p.id in tried_ids:
                st = 'wrong'
            else:
                st = 'none'
        else:
            st = 'none'

        stats.append({
            'problem': p,
            'total':   total,
            'ac':      ac,
            'rate':    rate,
            'status':  st
        })

    return render_template('problems.html',
                           stats=stats,
                           pagination=pagination)

# ─── 문제 상세 및 제출 ────────────────────────────────────────────────────
@app.route('/problems/<int:problem_id>', methods=['GET', 'POST'])
def problem_detail(problem_id):
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))

    problem = Problem.query.get_or_404(problem_id)

    if request.method == 'POST':
        code     = request.form['code']
        language = request.form['language']
        result, time_used, memory_used = run_code(code, language, problem)

        sub = Submission(
            user_id      = session['user_id'],
            problem_id   = problem_id,
            code         = code,
            language     = language,
            result       = result,
            time_used    = time_used,
            memory_used  = memory_used,
            code_length  = len(code)
        )
        db.session.add(sub)
        db.session.commit()
        flash(f'채점 결과: {result}', 'info')
        return redirect(url_for('problem_detail', problem_id=problem_id))

    total = Submission.query.filter_by(problem_id=problem_id).count()
    ac    = Submission.query.filter_by(problem_id=problem_id, result='AC').count()
    solve_rate = f"{ac/total*100:.1f}%" if total else '0%'

    user_subs = Submission.query \
        .filter_by(problem_id=problem_id, user_id=session['user_id']) \
        .order_by(Submission.submitted_at.desc()) \
        .all()

    return render_template('problem_detail.html',
                           problem=problem,
                           total_submissions=total,
                           ac_submissions=ac,
                           solve_rate=solve_rate,
                           user_submissions=user_subs)

# ─── 문제 생성 ────────────────────────────────────────────────────────────
@app.route('/create', methods=['GET', 'POST'])
def create_problem():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        f = request.form
        prob = Problem(
            title         = f['title'],
            description   = f['description'],
            input_spec    = f.get('input_spec', ''),
            output_spec   = f.get('output_spec',''),
            time_limit    = int(f['time_limit']),
            memory_limit  = int(f['memory_limit']),
            checker       = f['checker'],
            sample_input  = f.get('sample_input',''),
            sample_output = f.get('sample_output','')
        )
        db.session.add(prob)
        db.session.commit()
        flash('문제가 생성되었습니다. 이제 테스트케이스를 추가하세요.', 'success')
        return redirect(url_for('manage_testcases', problem_id=prob.id))
    return render_template('create_problem.html')

# ─── 문제 수정 ────────────────────────────────────────────────────────────
@app.route('/problems/<int:problem_id>/edit', methods=['GET', 'POST'])
def edit_problem(problem_id):
    prob = Problem.query.get_or_404(problem_id)
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        f = request.form
        prob.title         = f['title']
        prob.description   = f['description']
        prob.input_spec    = f.get('input_spec', '')
        prob.output_spec   = f.get('output_spec','')
        prob.time_limit    = int(f['time_limit'])
        prob.memory_limit  = int(f['memory_limit'])
        prob.checker       = f['checker']
        prob.sample_input  = f.get('sample_input','')
        prob.sample_output = f.get('sample_output','')
        db.session.commit()
        flash('문제가 수정되었습니다.', 'success')
        return redirect(url_for('problem_detail', problem_id=prob.id))

    return render_template('edit_problem.html', problem=prob)

# ─── 테스트케이스 관리 ──────────────────────────────────────────────────────
@app.route('/problems/<int:problem_id>/testcases', methods=['GET', 'POST'])
def manage_testcases(problem_id):
    prob = Problem.query.get_or_404(problem_id)
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        inp = request.form['input_data'].strip()
        out = request.form['output_data'].strip()
        if inp and out:
            tc = TestCase(problem_id=prob.id, input_data=inp, output_data=out)
            db.session.add(tc)
            db.session.commit()
            flash('테스트케이스가 추가되었습니다.', 'success')
        else:
            flash('입력/출력을 모두 입력해주세요.', 'warning')
        return redirect(url_for('manage_testcases', problem_id=prob.id))

    cases = prob.testcases.order_by(TestCase.id).all()
    return render_template('testcases.html', problem=prob, cases=cases)

# ─── 테스트케이스 삭제 ──────────────────────────────────────────────────────
@app.route('/problems/<int:problem_id>/testcases/<int:tc_id>/delete', methods=['POST'])
def delete_testcase(problem_id, tc_id):
    tc = TestCase.query.get_or_404(tc_id)
    db.session.delete(tc)
    db.session.commit()
    flash('테스트케이스가 삭제되었습니다.', 'info')
    return redirect(url_for('manage_testcases', problem_id=problem_id))

# ─── 문제 삭제 ────────────────────────────────────────────────────────────
@app.route('/problems/<int:problem_id>/delete', methods=['POST'])
def delete_problem(problem_id):
    if 'user_id' not in session:
        flash('권한이 없습니다. 로그인 해주세요.', 'warning')
        return redirect(url_for('login'))

    prob = Problem.query.get_or_404(problem_id)
    for sub in prob.submissions.all():
        db.session.delete(sub)
    for tc in prob.testcases.all():
        db.session.delete(tc)
    db.session.delete(prob)
    db.session.commit()
    flash(f'문제 "{prob.title}" 가 삭제되었습니다.', 'success')
    return redirect(url_for('problems'))

# ─── 전체 제출 현황 ────────────────────────────────────────────────────────
@app.route('/submissions')
def submissions():
    pid  = request.args.get('problem_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 14

    q = Submission.query.order_by(Submission.submitted_at.desc())
    if pid:
        q = q.filter_by(problem_id=pid)

    # paginate 를 이용해 페이지네이션
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    subs       = pagination.items

    # (기존) 문제 상태 매핑 로직
    user_id = session.get('user_id')
    problem_status = {}
    if user_id:
        ac_ids    = {r.problem_id for r in Submission.query.filter_by(user_id=user_id, result='AC')}
        tried_ids = {r.problem_id for r in Submission.query.filter_by(user_id=user_id)}
        for p_id in tried_ids:
            problem_status[p_id] = 'solved' if p_id in ac_ids else 'wrong'

    return render_template(
        'submissions.html',
        submissions=subs,
        pagination=pagination,      # ← 여기를 추가!
        problem_id=pid,
        problem_status=problem_status
    )

# ─── 내 제출 기록 ─────────────────────────────────────────────────────────
@app.route('/my_submissions')
def my_submissions():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    per_page = 14

    pagination = Submission.query \
        .filter_by(user_id=session['user_id']) \
        .order_by(Submission.submitted_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    subs = pagination.items

    # (기존) 내 제출 문제 상태 매핑
    ac_ids    = {r.problem_id for r in Submission.query.filter_by(user_id=session['user_id'], result='AC')}
    tried_ids = {s.problem_id for s in pagination.items}
    problem_status = {pid: ('solved' if pid in ac_ids else 'wrong') for pid in tried_ids}

    return render_template(
        'my_submissions.html',
        submissions=subs,
        pagination=pagination,      # ← 여기를 추가!
        problem_status=problem_status
    )

# ─── "/profile": 내 프로필로 리다이렉트 ─────────────────────────────────
@app.route('/profile')
def profile_root():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    username = session.get('username')
    if not username:
        # 세션에 username이 없는 경우, 사용자 객체에서 가져오기
        user = User.query.get(session.get('user_id'))
        if user:
            username = user.get_username()
            # 세션에 username 업데이트
            session['username'] = username
        else:
            flash('사용자 정보를 찾을 수 없습니다.', 'danger')
            return redirect(url_for('logout'))
    
    return redirect(url_for('profile', nickname=username))

# ─── "/profile/<nickname>": 모든 유저 프로필 보기 ────────────────────────
@app.route('/profile/<string:nickname>')
def profile(nickname):
    # nickname으로 사용자 찾기
    users = User.query.all()
    user = None
    for u in users:
        if u.get_username() == nickname:
            user = u
            break
    
    if not user:
        abort(404)
        
    stats = user.submission_stats()
    return render_template('profile.html', user=user, stats=stats)

# ─── "/profile/<nickname>/edit": 내 프로필만 수정 ───────────────────────
@app.route('/profile/<string:nickname>/edit', methods=['GET', 'POST'])
def edit_profile(nickname):
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    
    # nickname이 비어있는 경우 처리
    if not nickname:
        return redirect(url_for('profile_root'))
        
    # 내 닉네임이 아니면 403
    if session.get('username') != nickname:
        abort(403)
        
    # 사용자 찾기
    users = User.query.all()
    user = None
    for u in users:
        if u.get_username() == nickname:
            user = u
            break
            
    if not user:
        abort(404)
    
    # preferred_site 값 설정 (GET 요청과 POST 요청 모두에서 필요)
    user.preferred_site = request.form.get('preferred_site', user.preferred_site or 'none')

    if request.method == 'POST':
        cur_pw = request.form['current_password']
        if not user.check_password(cur_pw):
            flash('현재 비밀번호가 틀렸습니다.', 'danger')
            return redirect(url_for('edit_profile', nickname=nickname))

        # handles
        user.codeforces_handle = request.form.get('codeforces_handle') or None
        user.atcoder_handle    = request.form.get('atcoder_handle') or None

        # password change
        new_pw = request.form.get('new_password')
        if new_pw:
            # 비밀번호 규칙 검증
            is_valid, error_message = validate_password(new_pw)
            if not is_valid:
                flash(error_message, 'danger')
                return redirect(url_for('edit_profile', nickname=nickname))
            
            user.set_password(new_pw)

        db.session.commit()
        flash(f'{nickname}님의 정보가 성공적으로 업데이트되었습니다.', 'success')
        return redirect(url_for('profile', nickname=nickname))

    return render_template('edit_profile.html', user=user)

@app.before_request
def update_tiers():
    uid = session.get('user_id')
    if not uid:
        return
    user = User.query.get(uid)
    if not user:
        return

    dirty = False
    if user.codeforces_handle:
        tier = fetch_cf_tier(user.codeforces_handle)
        if tier and tier != user.cf_tier:
            user.cf_tier = tier
            dirty = True
    if user.atcoder_handle:
        at = fetch_ac_tier(user.atcoder_handle)
        if at and at != user.ac_tier:
            user.ac_tier = at
            dirty = True

    if dirty:
        db.session.commit()

# ─── 제출 코드 보기 ───────────────────────────────────────────────────────
@app.route('/submission/<int:submission_id>')
def view_submission(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    # 문제 상태 계산 (내 기준)
    user_id = session.get('user_id')
    status = 'none'
    if user_id:
        ac = Submission.query.filter_by(
            user_id=user_id,
            problem_id=sub.problem_id,
            result='AC'
        ).first()
        if ac:
            status = 'solved'
        else:
            tried = Submission.query.filter_by(
                user_id=user_id,
                problem_id=sub.problem_id
            ).first()
            status = 'wrong' if tried else 'none'
    return render_template(
        'view_submission.html',
        submission=sub,
        problem_status=status
    )

# ─── 게시판: 게시글 목록 ──────────────────────────────────────────────
@app.route('/forum')
def forum():
    page = request.args.get('page', 1, type=int)
    per_page = 14
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    return render_template('forum.html', posts=posts, pagination=pagination)

# ─── 게시판: 글쓰기 폼 ────────────────────────────────────────────────
@app.route('/forum/new', methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title or not content:
            flash('제목과 내용을 모두 입력하세요.', 'danger')
            return render_template('new_post.html')
        post = Post(user_id=session['user_id'], title=title, content=content)
        db.session.add(post)
        db.session.commit()
        flash('게시글이 등록되었습니다.', 'success')
        return redirect(url_for('forum'))
    return render_template('new_post.html')

# ─── 게시판: 게시글 상세 ──────────────────────────────────────────────
@app.route('/forum/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

# ─── 게시글 삭제 ──────────────────────────────────────────────────────
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        flash('권한이 없습니다. 로그인 해주세요.', 'warning')
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    if session['user_id'] != post.user_id:
        flash('삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('forum'))
    db.session.delete(post)
    db.session.commit()
    flash('게시글이 삭제되었습니다.', 'success')
    return redirect(url_for('forum'))

# ─── 게시판: 게시글 수정 ──────────────────────────────────────────────
@app.route('/forum/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if 'user_id' not in session or session['user_id'] != post.user_id:
        flash('수정 권한이 없습니다.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title or not content:
            flash('제목과 내용을 모두 입력하세요.', 'danger')
            return render_template('edit_post.html', post=post)
        post.title = title
        post.content = content
        db.session.commit()
        flash('게시글이 수정되었습니다.', 'success')
        return redirect(url_for('forum'))
    return render_template('edit_post.html', post=post)

# ─── 랭킹 (고유 문제 풀이 개수 기준) ───────────────────────────────────────
@app.route('/ranking')
def ranking():
    # id, username, cf_tier, solved_count를 함께 쿼리
    ranked = db.session.query(
        User.id,
        User.encrypted_username,
        User.cf_tier,
        User.ac_tier,
        User.preferred_site,
        func.count(func.distinct(Submission.problem_id)).label('solved')
    ).join(
        Submission, Submission.user_id == User.id
    ).filter(
        Submission.result == 'AC'
    ).group_by(
        User.id
    ).order_by(
        func.count(func.distinct(Submission.problem_id)).desc(),
        User.encrypted_username
    ).all()
    
    # 복호화된 사용자명 추가
    ranked_with_names = []
    for r in ranked:
        user = User.query.get(r.id)
        username = user.get_username()
        ranked_with_names.append({
            'id': r.id,
            'username': username,
            'cf_tier': r.cf_tier,
            'ac_tier': r.ac_tier,
            'preferred_site': r.preferred_site,
            'solved': r.solved
        })

    return render_template('ranking.html', ranked=ranked_with_names)

@app.template_filter('nl2br')
def nl2br(value):
    return Markup(value.replace('\n', '<br>\n'))

# 템플릿에서 사용자명 복호화 필터
@app.template_filter('decrypt_username')
def decrypt_username(user):
    if hasattr(user, 'get_username'):
        return user.get_username()
    return "Unknown"

@app.route('/ai_chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    message = data.get('message', '')
    problem_id = data.get('problem_id')
    
    # 문제 설명 불러오기
    problem = Problem.query.get(problem_id)
    if not problem:
        return {"reply": "문제를 찾을 수 없습니다."}
    
    # OpenAI API 키 설정 및 클라이언트 생성
    client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
    
    # AI에게 전달할 프롬프트 구성
    prompt = f"""
    [문제 제목]
    {problem.title}
    [문제 설명]
    {problem.description}
    [입력]
    {problem.input_spec or ''}
    [출력]
    {problem.output_spec or ''}
    [예제 입력]
    {problem.sample_input or ''}
    [예제 출력]
    {problem.sample_output or ''}
    ---
    [질문]
    {message}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 친절한 코딩 선생님이야. 문제에 대해 쉽게 설명해줘."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"OpenAI API 오류: {str(e)}"
    return {"reply": reply}

@app.route('/ai_chat_stream', methods=['GET', 'POST'])
def ai_chat_stream():
    is_post = request.method == 'POST'
    if is_post:
        data = request.get_json()
        message = data.get('message')
        problem_id = data.get('problem_id')
        history = data.get('history', [])
    else:
        message = request.args.get('message')
        problem_id = request.args.get('problem_id')
        history = []
    
    def generate():
        try:
            # 문제 정보 가져오기
            problem = Problem.query.get(problem_id)
            if not problem:
                if is_post:
                    yield "Error: 문제를 찾을 수 없습니다."
                else:
                    yield f"data: Error: 문제를 찾을 수 없습니다.\n\n"
                return

            # AI에게 전달할 프롬프트 구성
            prompt = f"""
            [문제 제목]
            {problem.title}
            [문제 설명]
            {problem.description}
            [입력]
            {problem.input_spec or ''}
            [출력]
            {problem.output_spec or ''}
            [예제 입력]
            {problem.sample_input or ''}
            [예제 출력]
            {problem.sample_output or ''}
            ---
            [질문]
            {message}
            """

            # OpenAI API 호출 (스트리밍 모드)
            client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
            # 대화 히스토리 반영
            messages = [
                {"role": "system", "content": """
너는 친절한 코딩 선생님이야. 문제에 대해 쉽게 설명해줘.\n만약 코드 예시를 줄 때는 반드시 아래처럼 해줘:\n[CODE_START]\n(여기에 코드, 예를 들어)\n```python\nprint(\"hello\")\n```\n[CODE_END]\n이렇게 [CODE_START]와 [CODE_END]로 감싸서 보내. 코드가 여러 개면 각각 감싸.\n코드는 반드시 여러 줄로, 각 줄마다 줄바꿈(\\n)이 들어가도록 해."""},
                {"role": "user", "content": prompt}
            ]
            if history:
                messages = [
                    {"role": "system", "content": """
너는 친절한 코딩 선생님이야. 문제에 대해 쉽게 설명해줘.\n만약 코드 예시를 줄 때는 반드시 아래처럼 해줘:\n[CODE_START]\n(여기에 코드, 예를 들어)\n```python\nprint(\"hello\")\n```\n[CODE_END]\n이렇게 [CODE_START]와 [CODE_END]로 감싸서 보내. 코드가 여러 개면 각각 감싸.\n코드는 반드시 여러 줄로, 각 줄마다 줄바꿈(\\n)이 들어가도록 해."""},
                    *history,
                    {"role": "user", "content": prompt}
                ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True
            )
            
            current_code_block = ""
            in_code_block = False
            
            for chunk in response:
                if chunk and chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # 코드 블록 시작/끝 감지
                    if "[CODE_START]" in content:
                        in_code_block = True
                        content = content.replace("[CODE_START]", "")
                        if is_post:
                            yield "[CODE_START]"
                        else:
                            yield f"data: [CODE_START]\n\n"
                    if "[CODE_END]" in content:
                        in_code_block = False
                        idx = content.index("[CODE_END]")
                        code_part = content[:idx]
                        rest = content[idx+len("[CODE_END]"):]
                        if is_post:
                            yield code_part
                            yield "[CODE_END]"
                        else:
                            yield f"data: {code_part}\n\n"
                            yield f"data: [CODE_END]\n\n"
                        current_code_block = ""
                        content = rest
                    if in_code_block:
                        if is_post:
                            yield content
                        else:
                            yield f"data: {content}\n\n"
                    else:
                        if is_post:
                            yield content
                        else:
                            yield f"data: {content}\n\n"
        except Exception as e:
            if is_post:
                yield f"Error: {str(e)}"
            else:
                yield f"data: Error: {str(e)}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream' if not is_post else 'text/plain')

# 속도 제한을 위한 상태 저장
request_counts = defaultdict(list)
rate_limit_lock = threading.Lock()  # 스레드 안전성을 위한 락
RATE_LIMIT = 20  # 초당 최대 요청 수
RATE_WINDOW = 10  # 10초 동안의 요청 기록을 유지

# 과도한 메모리 사용 방지를 위한 정리 함수
def cleanup_old_requests():
    current_time = time.time()
    with rate_limit_lock:
        # 일정 시간 이상 요청이 없는 IP는 제거
        ips_to_remove = []
        for ip, times in request_counts.items():
            if not times or times[-1] < current_time - RATE_WINDOW * 2:
                ips_to_remove.append(ip)
            else:
                # 오래된 요청 시간 제거
                while times and times[0] < current_time - RATE_WINDOW:
                    times.pop(0)
        
        # 사용하지 않는 IP 제거
        for ip in ips_to_remove:
            del request_counts[ip]

# 주기적으로 정리 작업 수행 (1분마다)
def periodic_cleanup():
    while True:
        time.sleep(60)
        cleanup_old_requests()

# 백그라운드에서 정리 작업 실행
cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()

@app.before_request
def apply_rate_limit():
    client_ip = request.remote_addr
    current_time = time.time()
    with rate_limit_lock:
        request_times = request_counts[client_ip]
        request_times.append(current_time)

        while request_times and request_times[0] < current_time - RATE_WINDOW:
            request_times.pop(0)

        if len(request_times) > RATE_LIMIT:
            print(f"Rate limit exceeded for {client_ip}")
            return "Too Many Requests", 429

if __name__ == '__main__':
    try:
        print("Starting HTTP server on port 80...")
        app.run(host='0.0.0.0', port=80, threaded=True)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Server shutdown complete.")
