from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
dummy_password = "password123"
dummy_hashed_password = password_hash.hash(dummy_password)

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)