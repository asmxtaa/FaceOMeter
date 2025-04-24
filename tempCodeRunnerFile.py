import random
import time
from datetime import datetime

class FaceDetection:
    def detect_faces(self, frame=None):
        print("Detecting faces...")
        time.sleep(1)
        return [(10, 10, 100, 100)]

    def predict_age(self, face, name):
        age = random.randint(18, 45)
        print(f"Predicted age for {name}: {age}")
        return age

    def predict_emotion(self, face):
        emotion = random.choice(["Happy", "Sad", "Neutral", "Angry", "Surprised"])
        print(f"Predicted emotion: {emotion}")
        return emotion

class FaceRecognition:
    def __init__(self):
        self.user_db = {}

    def register_user(self, name, roll_no, face_img):
        if name in self.user_db:
            print(f"User {name} already registered.")
        else:
            self.user_db[name] = roll_no
            print(f"[REGISTERED] Name: {name}, Roll No: {roll_no}")

    def recognize_face(self, face_img):
        if not self.user_db:
            print("No users in database.")
            return "Unknown"
        return random.choice(list(self.user_db.keys()) + ["Unknown"])

    def get_roll_no(self, name):
        return self.user_db.get(name, "N/A")

class UserTable:
    def __init__(self, detector, recognizer):
        self.detector = detector
        self.recognizer = recognizer

    def refresh_table(self):
        print("\n[User Table]")
        if not self.recognizer.user_db:
            print("No users registered.")
        else:
            for name, roll_no in self.recognizer.user_db.items():
                print(f"Name: {name}, Roll No: {roll_no}")
        print("")

class FaceRecognitionUI:
    def __init__(self):
        self.detector = FaceDetection()
        self.recognizer = FaceRecognition()
        self.user_table = UserTable(self.detector, self.recognizer)

    def _log_attendance(self, name):
        print(f"[ATTENDANCE SIMULATED] {name} would be marked present at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def simulate_register(self):
        print("\n--- Register User ---")
        name = input("Enter your name: ").strip()
        roll_no = input("Enter your roll number: ").strip()
        if not name or not roll_no:
            print("Name and Roll No cannot be empty.")
            return
        face_img = None
        self.recognizer.register_user(name, roll_no, face_img)

    def simulate_login(self):
        print("\n--- Face Recognition Login ---")
        print("Simulating webcam input and face scan...")
        time.sleep(1.5)
        face_img = None
        name = self.recognizer.recognize_face(face_img)
        if name == "Unknown":
            print("Face not recognized.")
        else:
            print(f"Face recognized: {name}")
            self.detector.predict_age(face_img, name)
            self.detector.predict_emotion(face_img)
            self._log_attendance(name)

    def menu(self):
        while True:
            print("\n=== Face Recognition System ===")
            print("1. Register New User")
            print("2. Face Recognition Login")
            print("3. Show Registered Users")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.simulate_register()
            elif choice == '2':
                self.simulate_login()
            elif choice == '3':
                self.user_table.refresh_table()
            elif choice == '4':
                print("Exiting system. Goodbye.")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.menu()
