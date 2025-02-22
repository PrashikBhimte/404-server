from fastapi import Header, HTTPException, UploadFile, File
from supabase_client import supabase

import google.generativeai as genai
from os import getenv
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

# import face_recognition
# import pickle
# import os

load_dotenv()

GEMINI_API_KEY = getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_PASSWORD = getenv("SENDER_PASSWORD")  
# RECEIVER_EMAIL = "prashikbhimte29@gmail.com"


def is_valguare(content : str):
    try:
        query = (
                "Respond ONLY with an integer: 1 (True) if the content is vulgar, "
                "or 0 (False) if it is clean. Check sure that content is good enough to show all students. Do NOT include any other text. "
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
    

def send_email(email : str, sendingFor : str, details = None):

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    emailContents = {
        "to_parent_as_student_goes_out" : {
            "subject" : "Student is going out",
            "body" : f"Hello, your child is going out of college at {date_time}. Please be aware of it."
        },
        "to_parent_as_student_comes_in" : {
            "subject" : "Student is coming in",
            "body" : f"Hello, your child is coming in college at {date_time}. Please be aware of it."
        },
        "to_class_coordinator" : {
            "subject" : "Doctor's Advice",
            "body" : f"Hello, Doctor has given advice to the student. Please take necessary actions. Details : {details}"
        },
        "to_all_students_regarding_election" : {
            "subject" : "New Election",
            "body" : f"Hello, there is an election going to be held. Please visit site for more information. Details : {details}"
        },
        "regarding_vote_done_to_candidate" : {
            "subject" : "Vote Done",
            "body" : f"Hello, you have got a vote. Please visit site for election live information. Deatils : {details}"
        }
    }
    
    subject = emailContents[sendingFor]["subject"]
    body = emailContents[sendingFor]["body"]

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        server.sendmail(SENDER_EMAIL, email, message.as_string())
        
        server.quit()
        return True

    except Exception as e:
        return False
    

# def register_user_face(id, image : UploadFile = File(...)):

#     face_encodings = face_recognition.face_encodings(face_recognition.load_image_file(image.file))

#     if face_encodings:

#         encoding = face_encodings[0]
#         filename = f"{id}.pkl"

#         with open(filename, "wb") as f:
#             pickle.dump(encoding, f)
        
#         BUCKET_NAME = "pkl-files"
        
#         with open(filename, "rb") as f:
#             print("Uploading file")
#             supabase.storage.from_(BUCKET_NAME).upload(filename, f, {"content-type": "application/octet-stream"})
        
#         os.remove(filename)
        
#         return True
#     else:
#         return False