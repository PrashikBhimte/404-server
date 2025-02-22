from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from classModels import User, Student, Faculty, LoginDetails
from supabase_client import supabase,  supabase_url
from dependencies import get_user_role

router = APIRouter()

@router.post('/signup')
def signup(user: User):

    user.data['id'] = "1a"

    if user.role == "student":
        validated_user = Student(**user.data)
    elif user.role == "faculty":
        validated_user = Faculty(**user.data)
    else:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'student' or 'faculty'.")

    response = supabase.auth.sign_up({
        "email": user.data['email'],
        "password": user.data['password']
    })

    if response and response.user:
        validated_user.id = response.user.id
        try:
            role = user.role.capitalize()
            inserted_data = dict(validated_user)
            password = inserted_data.pop("password")
            inserted_data['profilePhoto'] = ""
            response = supabase.table(role).insert(inserted_data).execute()
            return {"status": "Successfully signed up", "response" : response}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to insert the user data. {e}")
    
    raise HTTPException(status_code=400, detail="Signup failed. Email may already be in use.")

@router.post('/signin')
def signin(user : LoginDetails):
    
    try :
        responce = supabase.auth.sign_in_with_password(dict(user))

        if responce.session :
            role = get_user_role(responce.session.access_token)

            return {
                "access_token" : responce.session.access_token,
                "refresh_token" : responce.session.refresh_token,
                "role" : role
            }
        else :
            raise HTTPException(status_code=400, detail="Signin failed. Email may not be verifed yet.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Credentials. {e}")

@router.post('/signout')
def signout():
    try:
    
        response = supabase.auth.sign_out()
 
        if response and isinstance(response, dict) and response.get("error"):
            raise HTTPException(status_code=400, detail="Signout failed")

        return {"message": "User signout successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/access_token')
def get_new_access_token(refresh_token: str = Header(None, alias="refresh_token")):
    new_tokens = supabase.auth.refresh_session(refresh_token)
    if new_tokens.session:
        return { "access_token" : new_tokens.session.access_token, "refresh_token" : new_tokens.session.refresh_token }
    else :
        raise HTTPException(status_code=401, detail="Invalid tokens")
    

@router.post('/profilephoto')
async def post_profile_photo(file: UploadFile = File(...), id: str = Header(None, alias="id"), role: str = Header(None, alias="role")):
    try:
        file_extension = file.filename.split(".")[-1]
        file_name = f"{id}.{file_extension}"

        file_content = await file.read()

        # register_user_face(id, file)

        response = supabase.storage.from_("profile-images").upload(
            file_name, file_content, {"content-type": file.content_type}
        )

        image_url = f"{supabase_url}/storage/v1/object/public/{file_name}"

        supabase.table(role.capitalize()).update({"profilePhoto": image_url}).eq("id", id).execute()
        
        return {"response": response}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))