from typing import Annotated
from fastapi import Header, HTTPException
from supabase_client import supabase

def get_user_id(access_token: str = Header(..., alias="access_token")):
    try :
        response = supabase.auth.get_user(access_token)
    except :
        raise HTTPException(status_code=401, detail="Token is expired")
    else :
        if response.user:
            return response.user.id

        raise HTTPException(status_code=401, detail="Invalid tokens")


def get_student_details(id : str):
    response = supabase.table('Student').select("*").eq("id", id).execute()

    if response.count != 0:
        return dict(response.data[0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.") 

def get_faculty_details(id : str):
    response = supabase.table('Faculty').select("*").eq("id", id).execute()

    if response.count != 0:
        return dict(response.data[0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.") 
    

def get_user_role(access_token):
    try :
        response = supabase.auth.get_user(access_token)
    except :
        raise HTTPException(status_code=401, detail="Token is expired")
    else :
        if response.user:
            id = response.user.id

            details = get_student_details(id)
            if details:
                return "student"
            else :
                details = get_faculty_details(id)
                if details:
                    return "faculty"
                else :
                    return ""

        raise HTTPException(status_code=401, detail="Invalid tokens")