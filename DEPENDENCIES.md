# 사용된 오픈소스

본 프로젝트(AI-DimiOJ)는 아래 오픈소스 라이브러리·서비스의 도움을 받아 제작되었습니다. 각 라이브러리는 표시된 라이선스를 따르며 모두 MIT 라이선스와 호환됩니다.

## 백엔드 (Python)

| 라이브러리 | 라이선스 | 용도 |
|---|---|---|
| [Flask](https://github.com/pallets/flask) | BSD-3-Clause | 웹 프레임워크 |
| [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy) | BSD-3-Clause | ORM 통합 |
| [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) | MIT | DB 마이그레이션 |
| [Werkzeug](https://github.com/pallets/werkzeug) | BSD-3-Clause | WSGI / HTTP 유틸 |
| [Jinja2](https://github.com/pallets/jinja) | BSD-3-Clause | 템플릿 엔진 |
| [MarkupSafe](https://github.com/pallets/markupsafe) | BSD-3-Clause | 템플릿 안전 처리 |
| [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) | MIT | ORM |
| [Alembic](https://github.com/sqlalchemy/alembic) | MIT | 마이그레이션 엔진 |
| [requests](https://github.com/psf/requests) | Apache-2.0 | 외부 API 호출 |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | BSD-3-Clause | `.env` 파일 로드 |
| [openai](https://github.com/openai/openai-python) | Apache-2.0 | OpenAI 공식 Python SDK |
| [cryptography](https://github.com/pyca/cryptography) | Apache-2.0 / BSD-3-Clause | AES-256 / PBKDF2 |
| [gunicorn](https://github.com/benoitc/gunicorn) | MIT | 프로덕션 WSGI 서버 |

## 프론트엔드

| 라이브러리 | 라이선스 | 용도 |
|---|---|---|
| [highlight.js](https://github.com/highlightjs/highlight.js) 11.9.0 (CDN) | BSD-3-Clause | 코드 신택스 하이라이팅 |

## 외부 서비스 (코드 미포함)

| 서비스 | 사용 형태 |
|---|---|
| [OpenAI API](https://platform.openai.com/) | 사용자 본인 API 키로 호출 (AI 코딩 선생님 기능) |
| [Codeforces API](https://codeforces.com/apiHelp) | 사용자 티어 조회 |
| [AtCoder](https://atcoder.jp/) | 사용자 등급 페이지 스크래핑 |

## 라이선스 호환성

본 프로젝트의 [MIT License](LICENSE) 하에서 위 의존성을 모두 자유롭게 사용·재배포할 수 있습니다.

- **MIT / BSD-2/3-Clause / Apache-2.0** 라이선스: MIT 프로젝트에 포함 가능 (해당 라이브러리의 저작권 표시 보존 의무만 있음)
- GPL/LGPL/AGPL 등 강한 카피레프트 라이선스를 가진 의존성은 **사용하지 않습니다**.
