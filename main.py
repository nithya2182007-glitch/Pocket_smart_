from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .services.store import init_db
from .routes import pages,auth,planners
s=get_settings()
@asynccontextmanager
async def lifespan(app):
    init_db()
    yield
app=FastAPI(title=s.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[s.frontend_origin],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(pages.router); app.include_router(auth.router); app.include_router(planners.router)
@app.get("/health")
def health(): return {"status":"ok","app":s.app_name}
@app.get("/startup")
def startup(): return {"status":"initialized","mock_ai":s.mock_ai,"model":s.gemini_model}
