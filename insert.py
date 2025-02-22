from supabase_client import supabase


application_titles = [
    "Ground Booking for Sports Event",
    "Classroom Reservation for Study Group",
    "Auditorium Booking for Seminar",
    "Library Hall Reservation for Workshop",
    "Lab Booking for Practical Sessions",
    "Conference Room Reservation for Meeting",
    "Cafeteria Booking for Student Gathering",
    "Gymnasium Reservation for Fitness Event",
    "Parking Lot Booking for Event",
    "Hostel Common Room Reservation",
    "Open Air Theatre Booking for Cultural Event",
    "Computer Lab Reservation for Coding Session",
    "Music Room Booking for Band Practice",
    "Dance Room Reservation for Rehearsal",
    "Art Room Booking for Painting Session",
    "Photography Studio Reservation",
    "Media Room Booking for Recording",
    "Sports Complex Reservation for Tournament",
    "Swimming Pool Booking for Training",
    "Tennis Court Reservation for Match",
    "Basketball Court Booking for Practice",
    "Volleyball Court Reservation for Game",
    "Badminton Court Booking for Tournament",
    "Cricket Ground Reservation for Match",
    "Football Ground Booking for Practice",
    "Rugby Field Reservation for Game",
    "Hockey Field Booking for Training",
    "Table Tennis Room Reservation for Match",
    "Chess Room Booking for Tournament",
    "Yoga Room Reservation for Session",
    "Meditation Room Booking for Class"
]

for i in application_titles:
    supabase.table('ApplicationsTitles').insert({"title": i, "facultyId" : "faee5d21-873d-4d59-9815-ce9aca1c0b8d"}).execute()

print("Done")