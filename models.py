from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from utils import encrypt_id, decrypt_id, hash_password, verify_password

db = SQLAlchemy()

class User(db.Model):
    id                     = db.Column(db.Integer, primary_key=True)
    encrypted_username     = db.Column(db.Text, nullable=False, unique=True)  # AES로 암호화된 사용자명
    password_hash          = db.Column(db.String(256), nullable=False)  # 솔트를 포함한 해시 길이 증가
    codeforces_handle      = db.Column(db.String(64), nullable=True)
    atcoder_handle         = db.Column(db.String(64), nullable=True)
    cf_tier                = db.Column(db.String(32), nullable=True)
    ac_tier                = db.Column(db.String(32), nullable=True)
    # ← 새 컬럼: 선호 사이트 (색상 소스)
    preferred_site         = db.Column(db.String(10), nullable=False, default='none')
    submissions            = db.relationship('Submission', backref='user', lazy='dynamic')
    posts                  = db.relationship('Post', backref='user', lazy='dynamic')

    def set_password(self, pw):
        """솔트를 사용한 PBKDF2 해시로 비밀번호를 저장합니다."""
        self.password_hash = hash_password(pw)

    def check_password(self, pw):
        """제공된 비밀번호가 저장된 해시와 일치하는지 확인합니다."""
        return verify_password(self.password_hash, pw)

    def set_username(self, username):
        """사용자명을 암호화하여 저장합니다."""
        self.encrypted_username = encrypt_id(username)

    def get_username(self):
        """암호화된 사용자명을 복호화하여 반환합니다."""
        if not self.encrypted_username:
            return None
        return decrypt_id(self.encrypted_username)

    def get_encrypted_username(self):
        """암호화된 사용자명을 반환합니다."""
        return self.encrypted_username

    def submission_stats(self):
        q = Submission.query.filter_by(user_id=self.id)
        total = q.count()
        counts = { res: q.filter_by(result=res).count()
                   for res in ('AC','WA','CE','RE','TLE') }
        solved = db.session.query(
                     func.count(func.distinct(Submission.problem_id))
                 ).filter_by(user_id=self.id, result='AC').scalar() or 0
        return {'total': total, 'solved': solved, **counts}


class Problem(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(120), nullable=False)
    # 지문
    description   = db.Column(db.Text, nullable=False)
    # 입력/출력 명세
    input_spec    = db.Column(db.Text, nullable=True)
    output_spec   = db.Column(db.Text, nullable=True)
    time_limit    = db.Column(db.Integer, default=1)    # seconds
    memory_limit  = db.Column(db.Integer, default=128)  # MB
    # Python checker 코드 (optional)
    checker       = db.Column(db.Text, nullable=True)
    # 예제 입출력
    sample_input  = db.Column(db.Text, nullable=True)
    sample_output = db.Column(db.Text, nullable=True)

    submissions = db.relationship('Submission', backref='problem', lazy='dynamic', cascade="all, delete-orphan")
    testcases   = db.relationship('TestCase', backref='problem', lazy='dynamic', cascade="all, delete-orphan")


class Submission(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    problem_id   = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    code         = db.Column(db.Text, nullable=False)
    language     = db.Column(db.String(10), nullable=False)
    result       = db.Column(db.String(20), nullable=False)
    time_used    = db.Column(db.Float, nullable=True)    # seconds
    memory_used  = db.Column(db.Integer, nullable=True)  # MB
    code_length  = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Post(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class TestCase(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    problem_id  = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    input_data  = db.Column(db.Text, nullable=False)
    output_data = db.Column(db.Text, nullable=False)
