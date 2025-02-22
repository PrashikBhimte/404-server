from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from dependencies import get_user_id, get_faculty_details, get_student_details, send_email
from classModels import ElectionDetails, Candidate, Vote, ElectionId
from supabase_client import supabase
import pickle
import face_recognition
import numpy as np
import cv2

router = APIRouter()

eligible_designations_to_conduct_election = ['HOD']

@router.post('/register')
def register_the_election(election_details : ElectionDetails, id : str = Depends(get_user_id)):
    user_details = get_faculty_details(id)

    if user_details['desgination'] in eligible_designations_to_conduct_election:
        election_details = dict(election_details)
        election_details['conductedBy'] = user_details['fullName']
        election_details['status'] = "Ongoing"
        response = supabase.table('Elections').insert(election_details).execute()

        students = list(supabase.table('Student').select("*").execute().data)
    
        for i in students:
            email = i['email']
            send_email(email, "to_all_students_regarding_election", details = response.data[0])
        
        return response.data[0]
    else :
        raise HTTPException(status_code=401, detail="You are not authorised to conducte an election.")

@router.get('/elections')
def get_ongoing_elections_details():
    response = supabase.table('Elections').select("*").eq("status", "Ongoing").execute()

    if response:
        return response

@router.post('/apply_as_candidate')
def apply_as_candiate(candidate : Candidate, id : str = Depends(get_user_id)):
    
    candidate = dict(candidate)
    candidate['id'] = id

    election_details = dict(supabase.table('Elections').select("*").eq("electionId", int(candidate['electionId'])).execute().data[0])
    candidate_details = get_student_details(id)

    if candidate_details['year'] in election_details['year_eligible']['years'] and candidate_details['branch'] in election_details['branch_eligible']['branch']:
        try :

            response = supabase.table('Candidates').insert(candidate).execute()
    
            vote_details = {
                "candidateId" : id,
                "electionId" : int(candidate['electionId']),
                "votes" : 0
            }
            vote_response = supabase.table('Votes').insert(vote_details).execute()

            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unabale to register as candidate. {e}")

    else: 
        raise HTTPException(status_code=401, detail="you are not eligible for this election.")

    
@router.post('/candidates')
def get_election_candiates(electionId : ElectionId):

    response = supabase.table('Candidates').select("*").eq("electionId", electionId.electionId).execute()
    candidates = []
    for i in response.data:
        details = get_student_details(i['id'])
        if details:
            details.pop('created_at')
            details.pop('club')
            details.pop('parentEmail')
            details.pop('parentPhone')
            details.pop('position')
            details['manifesto'] = i['manifesto']
            details['proposals'] = i['proposals']

            candidates.append(details)

    return { "candidates" : candidates }

@router.post('/vote')
def vote(vote : Vote, id : str = Depends(get_user_id)):

    response = supabase.table('Voted').select("*").eq('voterId', id).eq('electionId', vote.electionId).execute()

    if response.data:
        raise HTTPException(status_code=401, detail="You have alreday voted once.")
    
    try :
        votes = dict(supabase.table('Votes').select('*').eq("candidateId", vote.candidateId).eq("electionId", vote.electionId).execute().data[0])['votes']
        supabase.table('Votes').update({"votes" : votes +  1}).eq("candidateId", vote.candidateId).eq("electionId", vote.electionId).execute()
        supabase.table('Voted').insert({
            "voterId" : id,
            "electionId" : vote.electionId
        }).execute()
        
        send_email(get_student_details(id)['email'], "regarding_vote_done_to_candidate", vote)

        return { "status" : "Your vote is counted successfully!" }
    except :
        raise HTTPException(status_code=400, detail="Your Vote is not count due to some issue. Please try again!")
    


@router.post("/verify-student")
async def verify_user(file: UploadFile = File(...), user_id: str = Depends(get_user_id)):
    try:
        BUCKET_NAME = "pkl-files"
        file_path = f"{user_id}.pkl"
        response = supabase.storage.from_(BUCKET_NAME).download(file_path)

        if not response:
            raise HTTPException(status_code=404, detail="Face data not found")

        stored_encoding = pickle.loads(response)

        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        face_encodings = face_recognition.face_encodings(image)
        if not face_encodings:
            raise HTTPException(status_code=400, detail="No face detected in the uploaded image")

        uploaded_encoding = face_encodings[0]

        results = face_recognition.compare_faces([stored_encoding], uploaded_encoding)

        if results[0]:
            return {"message": "User validated successfully"}
        else:
            raise HTTPException(status_code=401, detail="Face does not match")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))