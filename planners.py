import json
from fastapi import APIRouter,Request,UploadFile,File,Form
from ..auth import current_user
from ..models.schemas import HomeRequest,PartyRequest,TravelRequest,MealRequest,ShoppingRequest
from ..services.gemini_utils import generate_with_gemini
from ..services.store import save_history,get_history,get_recommendation
router=APIRouter()

def save(u,p,req,res): save_history(res["recommendation_id"],u,p,req,res); return res

@router.post("/generate-home")
def home(x:HomeRequest,request:Request):
    return save(current_user(request),"home",x.model_dump(),generate_with_gemini("home",x.model_dump()))

@router.post("/generate-party")
def party(x:PartyRequest,request:Request):
    return save(current_user(request),"party",x.model_dump(),generate_with_gemini("party",x.model_dump()))

@router.post("/generate-travel")
def travel(x:TravelRequest,request:Request):
    return save(current_user(request),"travel",x.model_dump(),generate_with_gemini("travel",x.model_dump()))

@router.post("/generate-meal")
def meal(x:MealRequest,request:Request):
    return save(current_user(request),"meal",x.model_dump(),generate_with_gemini("meal",x.model_dump()))

@router.post("/generate-shopping")
def shopping(x:ShoppingRequest,request:Request):
    return save(current_user(request),"shopping",x.model_dump(),generate_with_gemini("shopping",x.model_dump()))

@router.post("/generate-jewelry")
async def jewelry(request:Request,budget:float=Form(...),occasion:str=Form("Wedding"),style:str=Form("Elegant"),outfit_color:str=Form(""),notes:str=Form(""),outfit_image:UploadFile|None=File(None)):
    u=current_user(request); data={"budget":budget,"occasion":occasion,"style":style,"outfit_color":outfit_color,"notes":notes}
    img=await outfit_image.read() if outfit_image else None
    return save(u,"jewelry",data,generate_with_gemini("jewelry",data,img,outfit_image.content_type if outfit_image else None))

@router.get("/history")
def history(request:Request):
    return [{"id":r["id"],"planner":r["planner"],"created_at":r["created_at"],"summary":json.loads(r["response_json"]).get("summary","")} for r in get_history(current_user(request))]

@router.get("/recommendations-details/{rec_id}")
def details(rec_id:str,request:Request):
    from fastapi import HTTPException
    r=get_recommendation(rec_id,current_user(request))
    if not r: raise HTTPException(404,"Recommendation not found")
    return json.loads(r["response_json"])
