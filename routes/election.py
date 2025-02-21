from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_user_id, get_faculty_details, get_student_details
from classModels import ElectionDetails, Candidate, Vote, ElectionId
from supabase_client import supabase

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

    election_details = dict(supabase.table('Elections').select("*").eq("electionId", candidate['electionId']).execute().data[0])
    candidate_details = get_student_details(id)

    if candidate_details['year'] in election_details['year_eligible']['years'] and candidate_details['branch'] in election_details['branch_eligible']['branch']:
        try :

            response = supabase.table('Candidates').insert(candidate).execute()
            vote_details = {
                "candidateId" : id,
                "electionId" : candidate['electionId'],
                "votes" : 0
            }
            vote_response = supabase.table('Votes').insert(vote_details).execute()

            return response
        except :
            raise HTTPException(status_code=400, detail="Unabale to register as candidate.")

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
        return { "status" : "Your vote is counted successfully!" }
    except :
        raise HTTPException(status_code=400, detail="Your Vote is not count due to some issue. Please try again!")