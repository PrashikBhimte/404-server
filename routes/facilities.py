from fastapi import APIRouter, HTTPException, Depends
from classModels import FacilityApplication, ActionSchema
from supabase_client import supabase
from dependencies import get_user_id
from datetime import datetime
import json

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

@router.get("/applications")
async def get_applications(id : str = Depends(get_user_id)):

    response = supabase.table("FacilitiyApplication").select("*").eq("facultyId", id).execute()
    
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data

@router.post("/action")
async def action_on_application(action: ActionSchema, id: str = Depends(get_user_id)):  # Ensure action is received as a dict
    try:
        action = dict(action)
        action["facultyId"] = id
        action["date"] = str(datetime.now())

        applicationId = action.pop("applicationId", None)
        if not applicationId:
            raise HTTPException(status_code=400, detail="Missing applicationId")

        existing_data = supabase.table("FacilitiyApplication").select("forwardedSchema").eq("id", applicationId).execute()

        if existing_data.data:
            array = existing_data.data[0].get("forwardedSchema", [])
            if not isinstance(array, list):
                array = []

            array.append(action) 
            json_data = json.dumps(array) 

            response = supabase.table("FacilitiyApplication").update({"forwardedSchema": json_data, "status": action['action']}).eq("id", applicationId).execute()

            try :
                if response.error:
                    raise HTTPException(status_code=400, detail=response.error.message)
            except :
                return response.data

        else:
            raise HTTPException(status_code=404, detail="Application not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/status")
async def get_application_status(id : str = Depends(get_user_id)):

    response = supabase.table("FacilitiyApplication").select("*").eq("studentId", id).execute()
    
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data
