import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from config import CONFIG
import json
from deepface import DeepFace
import csv
from datetime import datetime

class UserTable:
    def __init__(self, parent_frame, detector, recognizer):
        self.parent = parent_frame
        self.detector = detector
        self.recognizer = recognizer
        self.create_table()

    def create_table(self):
        self.table_container = tk.Frame(self.parent)
        self.table_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.table_container, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.canvas.yview)

        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.table_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content_frame = tk.Frame(self.table_frame)
        self.content_frame.pack(expand=True, pady=10)

        headers = ["Registered Users", "Image", "Roll No.", "Gender", "Attendance", "Predicted Age"]
        for col, header in enumerate(headers):
            tk.Label(self.content_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=19).grid(row=0, column=col, padx=4, pady=4)

        self.display_users()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def display_users(self):
        if not os.path.exists(CONFIG["images_dir"]):
            return

        image_files = [f for f in os.listdir(CONFIG["images_dir"]) if f.endswith('.jpg')]

        for i in range(6):
            self.content_frame.grid_columnconfigure(i, weight=1)

        for row, image_file in enumerate(image_files, start=1):
            name = os.path.splitext(image_file)[0]
            roll_no = self.recognizer.get_roll_no(name)

            tk.Label(self.content_frame, text=name, font=("Arial", 10), borderwidth=1, relief="solid", padx=1, pady=5).grid(row=row, column=0, sticky="nsew")

            try:
                img_path = os.path.join(CONFIG["images_dir"], image_file)
                img = Image.open(img_path)
                img.thumbnail((60, 60))
                photo = ImageTk.PhotoImage(img)

                img_frame = tk.Frame(self.content_frame, borderwidth=1, relief="solid", padx=1, pady=5)
                img_frame.grid(row=row, column=1, sticky="nsew")
                img_label = tk.Label(img_frame, image=photo)
                img_label.image = photo
                img_label.pack(padx=5, pady=5)

                gender = self.predict_gender(img_path)
            except Exception as e:
                print(f"Error loading image {image_file}: {e}")
                img_frame = tk.Frame(self.content_frame, borderwidth=1, relief="solid", padx=1, pady=5)
                img_frame.grid(row=row, column=1, sticky="nsew")
                tk.Label(img_frame, text="Image not found").pack(padx=5, pady=5)
                gender = "Unknown"

            tk.Label(self.content_frame, text=roll_no, borderwidth=1, relief="solid", padx=1, pady=5).grid(row=row, column=2, sticky="nsew")
            tk.Label(self.content_frame, text=gender, borderwidth=1, relief="solid", padx=1, pady=5).grid(row=row, column=3, sticky="nsew")

            attendance_status = self._check_attendance(name, roll_no)
            color = "green" if "Present" in attendance_status else "red"
            tk.Label(self.content_frame, text=attendance_status, fg=color, borderwidth=1, relief="solid", padx=1, pady=5).grid(row=row, column=4, sticky="nsew")

            age_text = "Not yet predicted"
            try:
                age_file = os.path.join(CONFIG["age_dir"], f"{name}.json")
                if os.path.exists(age_file):
                    with open(age_file, 'r') as f:
                        age_data = json.load(f)
                    if "median_age" in age_data:
                        age_text = f"{age_data['median_age']} years"
            except Exception as e:
                print(f"Error loading age data for {name}: {e}")

            tk.Label(self.content_frame, text=age_text, borderwidth=1, relief="solid", padx=10, pady=5).grid(row=row, column=5, sticky="nsew")

    def _check_attendance(self, name, roll_no):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            attendance_path = os.path.join(os.path.dirname(__file__), "attendance.csv")

            if not os.path.exists(attendance_path):
                return "Absent ✖"

            with open(attendance_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 3:
                        if (row[0].strip() == name.strip() and 
                            row[1].strip() == roll_no.strip() and 
                            row[2].strip() == today):
                            return "Present ✔"
            return "Absent ✖"
        except Exception as e:
            print(f"Error reading attendance: {e}")
            return "Error"

    def predict_gender(self, image_path):
        try:
            analysis = DeepFace.analyze(image_path, actions=['gender'], enforce_detection=False)
            gender_data = analysis[0]['gender']
            predicted_gender = max(gender_data, key=gender_data.get)
            return predicted_gender
        except Exception as e:
            print(f"Error predicting gender for {image_path}: {e}")
            return "Unknown"

    def refresh_table(self):
        try:
            if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                headers = ["Registered Users", "Image", "Roll No.", "Gender", "Attendance", "Predicted Age"]
                for col, header in enumerate(headers):
                    tk.Label(self.content_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=19).grid(row=0, column=col, padx=4, pady=4)
                self.display_users()
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            print(f"Error in refresh_table: {e}")
