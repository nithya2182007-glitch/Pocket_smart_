from fastapi import APIRouter,HTTPException,Response,Request
from ..models.schemas import RegisterRequest,LoginRequest
from ..auth import hash_password,verify_password,create_token,current_user
from ..services.store import create_user,get_user
router=APIRouter()

@router.post("/register")
def register(x:RegisterRequest):
    if get_user(x.username): raise HTTPException(409,"Username already exists")
    create_user(x.username,hash_password(x.password)); return {"message":"Registration successful"}

@router.post("/login")
def login(x:LoginRequest,response:Response):
    u=get_user(x.username)
    if not u or not verify_password(x.password,u["password_hash"]): raise HTTPException(401,"Invalid username or password")
    t=create_token(x.username); response.set_cookie("access_token",t,httponly=True,samesite="lax",max_age=86400)
    return {"message":"Login successful","access_token":t}

@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token"); return {"message":"Logged out"}

@router.post("/token")
def token(x:LoginRequest):
    u=get_user(x.username)
    if not u or not verify_password(x.password,u["password_hash"]): raise HTTPException(401,"Invalid username or password")
    return {"access_token":create_token(x.username),"token_type":"bearer"}

@router.get("/session-info")
def session_info(request:Request):
    try: return {"logged_in":True,"username":current_user(request)}
    except HTTPException: return {"logged_in":False}

@router.get("/session-data")
def session_data(request:Request): return {"username":current_user(request),"preferences":{}}
