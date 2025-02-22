import cv2
import face_recognition
import pickle
import os

KNOWN_FACES_DIR = "known_faces"

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

def register_user(name):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Press 's' to save face", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_encodings = face_recognition.face_encodings(frame)
            if face_encodings:
                with open(f"{KNOWN_FACES_DIR}/{name}.pkl", "wb") as f:
                    pickle.dump(face_encodings[0], f)
                print(f"Face data for {name} saved!")
                break
            else:
                print("No face detected, try again!")

    cap.release()
    cv2.destroyAllWindows()

# Example: Register a user
# register_user("yash")


def verify_user():
    known_faces = {}
    
    # Load stored face encodings
    for filename in os.listdir(KNOWN_FACES_DIR):
        with open(f"{KNOWN_FACES_DIR}/{filename}", "rb") as f:
            known_faces[filename.split(".")[0]] = pickle.load(f)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        face_encodings = face_recognition.face_encodings(frame)

        if face_encodings:
            for name, stored_encoding in known_faces.items():
                matches = face_recognition.compare_faces([stored_encoding], face_encodings[0])
                if matches[0]:
                    print(f"User Verified: {name}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return name

        cv2.imshow("Face Verification - Press 'q' to exit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# Example: Check user
verified_user = verify_user()
if verified_user:
    print(f"Access Granted to {verified_user}")
else:
    print("Access Denied!")
