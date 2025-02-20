from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_user_id, get_faculty_details
from classModels import DoctorAdvice
from supabase_client import supabase

router = APIRouter()

def send_email(email):
    print(email)

router.post('/advice')
def register_doctor_advice(doctor_advice : DoctorAdvice, id : str = Depends(get_user_id)):
    user_details = get_faculty_details(id)

    if user_details['desgination'] == "doctor":

        student_details = dict(supabase.table('Student').select("*").eq("collegeRegNo", doctor_advice.collegeRegNo).execute().data[0])

        class_coordinator_id  = dict(supabase.table('ClassCoordinators').select("*").eq("branch", student_details['branch']).eq("year", student_details['year']).execute().data[0])['coordinatorId']
        class_coordinator_email = get_faculty_details(class_coordinator_id)['email']

        send_email(class_coordinator_email)

        doctor_advice = dict(doctor_advice)
        doctor_advice['doctor_id'] = id
        response = supabase.table('DoctorAdvice').insert(doctor_advice).execute()

        if response:
            return dict(response.data[0])
    else :
        raise HTTPException(status_code=401, detail="You are not the authorised Doctor")
