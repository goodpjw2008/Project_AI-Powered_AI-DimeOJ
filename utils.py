import requests
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import secrets
import hashlib
import re
from config import Config

CF_API = "https://codeforces.com/api/user.info"
AC_API = "https://atcoder.jp/users/{handle}/history/json"

# 암호화에 사용할 키와 IV를 Config에서 가져옵니다
ENCRYPTION_KEY = Config.ENCRYPTION_KEY
IV = Config.ENCRYPTION_IV

def validate_password(password):
    """
    비밀번호 규칙을 검증합니다.
    - 최소 8자 이상
    - 영문, 숫자, 특수문자 조합
    
    Returns:
        tuple: (유효성 여부, 오류 메시지)
    """
    if len(password) < 8:
        return False, "비밀번호는 8자 이상이어야 합니다."
    
    if not re.search(r'[A-Za-z]', password):
        return False, "비밀번호는 영문을 포함해야 합니다."
    
    if not re.search(r'\d', password):
        return False, "비밀번호는 숫자를 포함해야 합니다."
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False, "비밀번호는 특수문자를 포함해야 합니다."
    
    return True, "유효한 비밀번호입니다."

def encrypt_id(id_str):
    """AES-256-CBC 방식으로 ID를 암호화합니다."""
    if not id_str:
        return None
    
    # 키와 IV를 바이트로 변환
    key_bytes = bytes.fromhex(ENCRYPTION_KEY) if len(ENCRYPTION_KEY) == 32 else ENCRYPTION_KEY.encode()[:32]
    iv_bytes = bytes.fromhex(IV) if len(IV) == 16 else IV.encode()[:16]
    
    # IV 길이 보정 (16바이트/128비트로 맞춤)
    if len(iv_bytes) < 16:
        iv_bytes = iv_bytes + b'\0' * (16 - len(iv_bytes))
    
    # 16바이트 블록에 맞게 패딩
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    data = padder.update(id_str.encode()) + padder.finalize()
    
    # AES 암호화
    cipher = Cipher(algorithms.AES(key_bytes), 
                   modes.CBC(iv_bytes), 
                   backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    
    # Base64로 인코딩하여 반환
    return base64.b64encode(encrypted_data).decode()

def decrypt_id(encrypted_id):
    """암호화된 ID를 복호화합니다."""
    if not encrypted_id:
        return None
    
    # 키와 IV를 바이트로 변환
    key_bytes = bytes.fromhex(ENCRYPTION_KEY) if len(ENCRYPTION_KEY) == 32 else ENCRYPTION_KEY.encode()[:32]
    iv_bytes = bytes.fromhex(IV) if len(IV) == 16 else IV.encode()[:16]
    
    # IV 길이 보정 (16바이트/128비트로 맞춤)
    if len(iv_bytes) < 16:
        iv_bytes = iv_bytes + b'\0' * (16 - len(iv_bytes))
    
    try:
        # Base64 디코딩
        encrypted_data = base64.b64decode(encrypted_id)
        
        # AES 복호화
        cipher = Cipher(algorithms.AES(key_bytes), 
                       modes.CBC(iv_bytes), 
                       backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # 패딩 제거
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        
        return decrypted_data.decode()
    except Exception as e:
        print(f"복호화 오류: {str(e)}")
        return None

def hash_password(password):
    """PBKDF2 알고리즘과 솔트를 사용해 비밀번호를 해싱합니다."""
    # 32바이트(256비트) 솔트 생성
    salt = secrets.token_bytes(32)
    
    # PBKDF2 해싱 (10만번 반복)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    hash_bytes = kdf.derive(password.encode())
    
    # 솔트와 해시를 합쳐서 저장 (솔트 + 해시)
    storage = salt + hash_bytes
    
    # Base64로 인코딩하여 반환
    return base64.b64encode(storage).decode()

def verify_password(stored_password, provided_password):
    """저장된 해시와 제공된 비밀번호가 일치하는지 확인합니다."""
    # Base64 디코딩
    storage = base64.b64decode(stored_password)
    
    # 솔트 추출 (첫 32바이트)
    salt = storage[:32]
    stored_hash = storage[32:]
    
    # 제공된 비밀번호 해싱
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    try:
        # 검증 시도
        kdf.verify(provided_password.encode(), stored_hash)
        return True
    except:
        return False

def fetch_cf_tier(handle: str) -> str:
    resp = requests.get(CF_API, params={'handles': handle})
    data = resp.json()
    if data.get('status') == 'OK':
        rank = data['result'][0].get('rank','').replace(' ','_').lower()
        return rank
    return ''

def fetch_ac_tier(handle: str) -> str:
    # AtCoder rating history JSON
    url = AC_API.format(handle=handle)
    resp = requests.get(url)
    history = resp.json()
    if isinstance(history, list) and history:
        last = history[-1].get('NewRating',0)
        if last < 400:     return 'beginner'
        if last < 800:     return 'brown'
        if last < 1200:     return 'green'
        if last < 1600:     return 'cyan'
        if last < 2000:     return 'blue'
        if last < 2400:     return 'yellow'
        if last < 2800:     return 'orange'
        return 'red'
    return ''
