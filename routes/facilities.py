from fastapi import APIRouter, HTTPException, Depends
from classModels import FacilityApplication, ActionSchema
from supabase_client import supabase
from dependencies import get_user_id

router = APIRouter()

@router.get("/all")
async def get_all_facilities():
    response = supabase.table("Facilities").select("*").execute()
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data

@router.post("/apply")
async def apply_for_facility(application: FacilityApplication, id : str = Depends(get_user_id)):
    # try :
    #     application 
    response = supabase.table("Facilities").insert(application.dict()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Application submitted successfully"}

@router.post("/action/{application_id}")
async def action_on_application(application_id: str, action: ActionSchema):
    response = supabase.table("Facilities").update({
        "forwardedSchema": supabase.func.array_append("forwardedSchema", action.dict())
    }).eq("id", application_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Action recorded successfully"}

@router.get("/status/{application_id}")
async def get_application_status(application_id: str):
    response = supabase.table("Facilities").select("status, forwardedSchema").eq("id", application_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="Application not found")
    return response.data[0]
