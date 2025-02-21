from fastapi import APIRouter, HTTPException, Depends
from classModels import FacilityApplication, ActionSchema
from supabase_client import supabase
from dependencies import get_user_id
from datetime import datetime

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
    application = application.dict()
    application["studentId"] = id
    application["status"] = "pending"
    application['facultyId'] = dict(supabase.table('Facilities').select('*').eq('facilitiy', application['facilitiy']).execute().data[0])['facultyId']
    application['forwardedSchema'] = []
    response = supabase.table("FacilitiyApplication").insert(application).execute()
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data

@router.post("/action")
async def action_on_application(action: ActionSchema, id : str = Depends(get_user_id)):

    action = action.dict()
    applicationId = action['applicationId']
    action.pop('applicationId')
    action['facultyId'] = id
    action['date'] = str(datetime.now())

    response = supabase.table("FacilitiyApplication").update({
        "forwardedSchema": supabase.func.array_append("forwardedSchema", action)
    }).eq("id", applicationId).execute()

    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data

@router.get("/status")
async def get_application_status(id : str = Depends(get_user_id)):

    response = supabase.table("FacilitiyApplication").select("*").eq("studentId", id).execute()
    
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data
