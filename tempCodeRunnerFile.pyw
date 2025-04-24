import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from deepface import DeepFace

# Configuration
CONFIG = {
    "images_dir": os.path.join(os.path.expanduser("~"), "Desktop", "Face_Recog", "Face", "images"),
    "haar_cascade": cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
    "recognition_threshold": 0.6,
    "model_name": "Facenet"
}

class FaceRecognitionSystem:
    def __init__(self):
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(CONFIG["haar_cascade"])
        
        # Create images directory if not exists
        os.makedirs(CONFIG["images_dir"], exist_ok=True)
        
        # Initialize video capture
        self.video_cap = cv2.VideoCapture(0)
        
        # Initialize Tkinter root
        self.root = tk.Tk()
        self.root.withdraw()
        
    def predict_emotion(self, face_img):
        try:
            analysis = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
            return analysis[0]['dominant_emotion']
        except Exception as e:
            print(f"Emotion prediction error: {e}")
            return "Unknown"

    def predict_age(self, face_img):
        try:
            analysis = DeepFace.analyze(face_img, actions=['age'], enforce_detection=False)
            return int(analysis[0]['age'])
        except Exception as e:
            print(f"Age prediction error: {e}")
            return "Unknown"

    def register_user(self, name, face_img):
        """Save face image and generate encoding"""
        img_path = os.path.join(CONFIG["images_dir"], f"{name}.jpg")
        cv2.imwrite(img_path, face_img)
        return True

    def recognize_face(self, face_img):
        """Compare face with registered users"""
        try:
            # Convert to RGB (DeepFace requirement)
            face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            
            # Find matches in database
            matches = DeepFace.find(
                img_path=face_rgb,
                db_path=CONFIG["images_dir"],
                model_name=CONFIG["model_name"],
                enforce_detection=False,
                silent=True
            )
            
            if matches and not matches[0].empty:
                best_match = matches[0].iloc[0]
                
                # Handle different DeepFace versions
                distance_metric = "distance" if "distance" in matches[0].columns else "Facenet_cosine"
                
                if best_match[distance_metric] < CONFIG["recognition_threshold"]:
                    return os.path.splitext(os.path.basename(best_match["identity"]))[0]
            
            return None
        except Exception as e:
            print(f"Recognition error: {e}")
            return None

    def show_login_popup(self):
        """Display login/registration options"""
        popup = tk.Toplevel()
        popup.title("Face Recognition System")
        popup.geometry("300x200")
        
        tk.Label(popup, text="Welcome", font=("Arial", 14)).pack(pady=20)
        
        def on_register():
            name = simpledialog.askstring("Register", "Enter your name:")
            if name:
                popup.destroy()
                self.register_new_user(name)

        def on_login():
            popup.destroy()
            self.show_camera()

        tk.Button(popup, text="Register", command=on_register, bg="green", fg="white").pack(pady=10)
        tk.Button(popup, text="Login", command=on_login, bg="blue", fg="white").pack(pady=10)
        
        popup.mainloop()

    def register_new_user(self, name):
        """Capture and register new user face"""
        while True:
            ret, frame = self.video_cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

            if len(faces) == 0:
                cv2.putText(frame, "Align face and press SPACE", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                (x, y, w, h) = faces[0]
                face_img = frame[y:y+h, x:x+w]
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE to capture", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            cv2.imshow("Register Face", frame)
            
            key = cv2.waitKey(1)
            if key == ord(' '):  # SPACE to capture
                if len(faces) > 0:
                    self.register_user(name, face_img)
                    messagebox.showinfo("Success", f"{name} registered successfully!")
                    break
            elif key == ord('E'):  # E to quit
                break

        cv2.destroyAllWindows()
        self.show_camera(name)

    def show_camera(self, known_name=None):
        """Live face recognition with emotion/age detection"""
        while True:
            ret, frame = self.video_cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                
                # Recognize face if not already known
                current_name = known_name
                if current_name is None:
                    current_name = self.recognize_face(face_img) or "Unknown"
                
                # Get predictions
                emotion = self.predict_emotion(face_img)
                age = self.predict_age(face_img)
                
                # Display info
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{current_name}, {age}, {emotion}", (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            cv2.imshow("Face Recognition", frame)
            
            if cv2.waitKey(1) == ord('E'):
                break

        self.cleanup()

    def cleanup(self):
        """Release resources"""
        self.video_cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

    def run(self):
        """Start the application"""
        self.show_login_popup()
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRecognitionSystem()
    app.run()