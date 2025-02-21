from typing import Annotated
from fastapi import Header, HTTPException
from supabase_client import supabase

import google.generativeai as genai
from os import getenv
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def is_valguare(content : str):
    try:
        query = (
                "Respond ONLY with an integer: 1 (True) if the content is vulgar, "
                "or 0 (False) if it is clean. Do NOT include any other text. "
                f"Content: {content}"
            )
        response = model.generate_content(query)

        result = response.text.strip()

        return int(result) == 1
    except Exception as e:
        return False 

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

    if len(response.data) != 0:
        return dict(response.data[0])
    else :
        return None

def get_faculty_details(id : str):
    response = supabase.table('Faculty').select("*").eq("id", id).execute()

    if len(response.data) != 0:
        return dict(response.data[0])
    else :
        return None


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
    
