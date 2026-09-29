import hashlib, hmac, secrets, time, jwt
from fastapi import HTTPException, Request
from .config import get_settings

def hash_password(password):
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,120000)
    return salt.hex()+"$"+digest.hex()

def verify_password(password, stored):
    try:
        salt,digest=stored.split("$",1)
        got=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),120000)
        return hmac.compare_digest(got.hex(),digest)
    except Exception:
        return False

def create_token(username):
    now=int(time.time())
    return jwt.encode({"sub":username,"iat":now,"exp":now+86400},get_settings().secret_key,algorithm="HS256")

def decode_token(token):
    try:
        p=jwt.decode(token,get_settings().secret_key,algorithms=["HS256"])
        if not p.get("sub"): raise ValueError
        return p["sub"]
    except Exception:
        raise HTTPException(401,"Invalid or expired token")

def current_user(request: Request):
    token=request.cookies.get("access_token")
    if not token:
        h=request.headers.get("Authorization","")
        if h.startswith("Bearer "): token=h[7:]
    if not token: raise HTTPException(401,"Login required")
    return decode_token(token)
