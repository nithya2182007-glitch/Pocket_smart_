from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router=APIRouter()
templates=Jinja2Templates(directory="app/templates")
@router.get("/",response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse(request=request,name="index.html")
@router.get("/login",response_class=HTMLResponse)
def login(request:Request): return templates.TemplateResponse(request=request,name="login.html")
@router.get("/register",response_class=HTMLResponse)
def register(request:Request): return templates.TemplateResponse(request=request,name="register.html")
@router.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request): return templates.TemplateResponse(request=request,name="dashboard.html")
