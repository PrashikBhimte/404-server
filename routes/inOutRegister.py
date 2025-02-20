from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_user_id, get_faculty_details
from classModels import InOutReg
from supabase_client import supabase

router = APIRouter()

def send_email(email):
    print(email)

router.post('/inoutregister')
def in_out_register(inoutreg : InOutReg, id : str = Depends(get_user_id)):
    user = get_faculty_details(id)
    if user['desgination'] == "guard":
        response = dict(supabase.table('InOutRegister').insert(dict(inoutreg)).execute().data[0])
        
        student_email = dict(supabase.table('Student').select("*").eq("collegeRegNo", inoutreg.collegeRegNo).execute().data[0])['email']

        send_email(student_email)

        if response :
            return response
        
    else:
        raise HTTPException(status_code=401, detail="You are not the authorised Guard.")
