import os
import secrets
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))


class Config:
    # 기본 설정
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dimeoj.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 암호화 설정
    ENCRYPTION_KEY = '418951dc9b262d40c78743d2d4cebe75'
    ENCRYPTION_IV = 'a757a58c3015e718'

    # 파이썬 및 샌드박스 설정
    PYTHON_BIN = os.environ.get('PYTHON_BIN', '/usr/bin/python3')
    SANDBOX_DIR = os.environ.get('SANDBOX_DIR', './sandbox')

    # 보안 설정
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
