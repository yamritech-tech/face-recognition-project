# Face Recognition Project (ESP32 + Flask + OpenCV)

## 📌 Overview  
This project implements a real-time facial recognition system using an ESP32 camera module, a Python Flask server, and a simple web interface.  

- **ESP32** captures an image.  
- **Flask server** processes the image and compares it with the stored database using embeddings.  
- **Web page** displays recognition results.  

---

## 🛠️ Features  
- Add new faces to the database via camera.  
- Real-time recognition of individuals.  
- Web interface for capturing and testing.  
- Modular design for better organization:  
  - `CodePython/` → Python scripts (Flask server, database tools)  
  - `CodeESP32/` → ESP32 Arduino code  
  - `Web/` → HTML, CSS, JS interface  

---

## 📂 Project Structure  

Face Recognition Project/
│── CodePython/
│ ├── AddToDatabase.py
│ ├── Server.py
│
│── CodeESP32/
│ └── ESP32_FaceRecognition.ino
│
│── Web/
│ └── index.html # contains HTML, CSS, and JavaScript together
│
│── requirements.txt
│── schema.sql
│── README.md

yaml
Copy code

---

## ⚙️ Installation & Setup  

### 1. Clone the repository  
```bash
git clone https://github.com/yamritech-tech/face-recognition-project.git
cd face-recognition-project
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Setup the database
Run in MySQL:

sql
Copy code
SOURCE schema.sql;
4. Start the server
bash
Copy code
python CodePython/Server.py
5. Access the web interface
Open in your browser:
👉 http://localhost:5000

💻 Usage
Add new user: Run AddToDatabase.py, enter a name, capture a photo.

Recognition: ESP32 captures an image, server checks against the database.

Results: Web page shows recognized individual or "not recognized".

🚀 Technologies Used
ESP32-CAM

Python (Flask, OpenCV, NumPy, Imgbeddings)

MySQL

HTML, CSS, JavaScript