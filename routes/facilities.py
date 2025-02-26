from fastapi import APIRouter, HTTPException, Depends
from classModels import FacilityBook, Date
from supabase_client import supabase
from dependencies import get_user_id
from datetime import datetime
import json

router = APIRouter()

@router.get("/all")
async def get_all_facilities():
    response = supabase.table("Facilities").select("*").execute()
    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data

@router.post("/book")
async def apply_for_facility(facility: FacilityBook, id: str = Depends(get_user_id)):  
    bookings = list(supabase.table("FacilityBooked")
                    .select("*")
                    .eq("facility", facility.facility)  # ✅ Ensure same facility
                    .eq("date", facility.date)          # ✅ Ensure same date
                    .execute().data)

    facility_dict = facility.dict()
    facility_dict["studentId"] = id

    for existing_booking in bookings:
        existing_from = existing_booking["fromTime"]
        existing_to = existing_booking["toTime"]

        # Check if new booking overlaps with existing booking
        if not (facility_dict["toTime"] <= existing_from or facility_dict["fromTime"] >= existing_to):
            raise HTTPException(status_code=400, detail="Slot is already booked.")

    response = supabase.table("FacilityBooked").insert(facility_dict).execute()
    try:
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return {"message": "Facility booked successfully!"}


@router.post('/bookings')
def get_all_booking(date : Date):

    response = supabase.table('FacilityBooked').select("*").eq('date', date.date).execute()

    try :
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
    except :
        return response.data
