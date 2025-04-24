
# 👤 Face Recognition Attendance System

A real-time face recognition system using **DeepFace**, **OpenCV**, and **Tkinter**. It detects faces, recognizes known individuals, predicts age and emotion, and automatically logs attendance to a CSV file — all through a simple graphical interface.

## ✨ Features

- 🧠 **Face Recognition** using DeepFace
- 😀 **Emotion & Age Prediction**
- 🕒 **Automated Attendance Logging** with timestamp
- 📋 **CSV File Output** for records
- 🖼️ **User-Friendly GUI** built with Tkinter
- 📁 **Photo-based Registration**

---

## ⚙️ Tech Stack

| Technology     | Usage                             |
|----------------|-----------------------------------|
| **Python**     | Core programming language         |
| **DeepFace**   | Face recognition and analysis     |
| **OpenCV**     | Face detection and image capture  |
| **Tkinter**    | GUI development                   |
| **Pandas**     | Data handling and CSV logging     |

---

## 🧑‍💻 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/asmxtaa/Face-Recognition-Attendance.git
   cd Face-Recognition-Attendance
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add registered user images:**
   - Place face images (e.g., `Asmita.jpg`) into the `registered_faces/` folder.

5. **Run the app:**
   ```bash
   python ss.pyw
   ```

6. **View attendance table:**
   ```bash
   python tables.py
   ```

---

## 📁 Project Structure

```
├── ss.pyw               # Main GUI launcher
├── recognition.py       # Handles recognition logic
├── detection.py         # Face preprocessing
├── tables.py            # Attendance table viewer
├── registered_faces/    # Store images of known users
├── attendance_log.csv   # Auto-generated attendance log
```

---

## 📋 Output Format

Attendance logs are stored in `attendance_log.csv` in the following format:

```
Name, Date, Time, Emotion, Age
```

---

## 🧑‍🎨 Built By

**Asmita Mandal 🌸**  
[GitHub](https://github.com/asmxtaa) • [LinkedIn](https://linkedin.com/in/asmxtaa)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
