from fastapi import APIRouter, Depends
from dependencies import get_user_id
from supabase_client import supabase
from classModels import Application, ApplicationAction, ApplicationId
from datetime import datetime

router = APIRouter()

@router.get('/titles')
def get_all_titles():

    response = supabase.table('ApplicationsTitles').select("title").execute()

    if len(response.data) == 0:
        return {"message": "No titles found"}

    return {"titles": response.data}

@router.post('/apply')
def submit_application(application : Application, id: str = Depends(get_user_id)):

    title_response = supabase.table('ApplicationsTitles').select("*").eq("title", application.title).execute()

    response = supabase.table('Applications').insert([{
        "title": application.title,
        "description": application.description,
        "type": application.type,
        "status": "pending",
        "lastUpdated": None,
        "studentId": id,
        "facultyId": title_response.data[0]['facultyId']
    }]).execute()

    return {"message": "Application submitted successfully"}

@router.get('/applications')
def get_applications(id: str = Depends(get_user_id)):

    response = supabase.table('Applications').select("*").eq("facultyId", id).eq('status', 'pending').execute()

    forwarded_response = supabase.table('ApplicationLogs').select("*").eq("to", id).eq('action', 'forwarded').execute()

    for i in forwarded_response.data:
        response.data.append(supabase.table('Applications').select("*").eq("id", i['applicationId']).eq('status', "forwarded").execute().data[0])

    if len(response.data) == 0:
        return {"message": "No applications found"}

    return {"applications": response.data}

@router.post('/action')
def take_action(applicationAction : ApplicationAction, id: str = Depends(get_user_id)):

    response = supabase.table('Applications').update({
        "status": applicationAction.action,
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }).eq("id", applicationAction.applicationId).execute()

    logs_response = supabase.table('ApplicationLogs').insert({
        "applicationId": applicationAction.applicationId,
        "action": applicationAction.action,
        "from": id,
        "to": applicationAction.forwardedTo
    }).execute()

    return {"message": "Action taken successfully", "response" : response }

@router.get('/my-applications')
def get_my_applications(id: str = Depends(get_user_id)):

    response = supabase.table('Applications').select("*").eq("studentId", id).execute()

    if len(response.data) == 0:
        return {"message": "No applications found"}

    return {"applications": response.data}

@router.post('/application-details')
def get_application_details(applicationId: ApplicationId):

    response = supabase.table('Applications').select("*").eq("id", applicationId.applicationId).execute()

    logs_response = supabase.table('ApplicationLogs').select("*").eq("applicationId", applicationId.applicationId).execute()

    if len(response.data) == 0:
        return {"message": "No application found"}

    return {"application": response.data[0], "logs": logs_response.data}