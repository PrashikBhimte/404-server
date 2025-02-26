from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_user_id, get_faculty_details, send_email
from classModels import InOutReg
from supabase_client import supabase

router = APIRouter()

@router.post('/inoutregister')
def in_out_register(inoutreg : InOutReg, id : str = Depends(get_user_id)):
    user = get_faculty_details(id)

    if user['desgination'] == "HOD":
        response = dict(supabase.table('InOutRegister').insert(dict(inoutreg)).execute().data[0])

        student_email = dict(supabase.table('Student').select("*").eq("collegeRegNo", inoutreg.collegeRegNo).execute().data[0])['parentEmail']
     
        if inoutreg.in_or_out == "out":  
            send_email(student_email, "to_parent_as_student_goes_out")
        elif inoutreg.in_or_out == "in":
            send_email(student_email, "to_parent_as_student_comes_in")

        if response :
            return response
        
    else:
        raise HTTPException(status_code=401, detail="You are not the authorised Guard.")

