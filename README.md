🎭 Face Recognition Project

A real-time facial recognition system built with Flask, Python, OpenCV, and ESP32-CAM, connected to a MySQL database for storing and verifying users.

This project demonstrates how AI and IoT can work together for secure authentication and real-time video streaming.

🚀 Features

📷 ESP32-CAM Integration → live camera feed to Flask server.

🧠 Face Detection & Recognition using OpenCV.

🗄️ Database Integration (MySQL) → stores user details & embeddings.

🌐 Web Dashboard (Flask) → real-time video & recognition results.

🔒 Secure Authentication → only recognized users are granted access.

📂 Project Structure
face-recognition-project/
│── app.py              # Flask server
│── esp32/              # ESP32-CAM Arduino code
│── models/             # Trained face recognition models
│── static/             # CSS/JS files for Flask app
│── templates/          # HTML pages (Flask Jinja2)
│── database/           # MySQL setup scripts
│── README.md           # Project documentation

⚙️ Setup & Installation
🔧 Requirements

Python 3.8+

OpenCV

Flask

MySQL

ESP32-CAM + Arduino IDE

🖥️ Steps

Clone the repository:

git clone https://github.com/yamritech-tech/face-recognition-project.git
cd face-recognition-project


Install dependencies:

pip install -r requirements.txt


Configure database in app.py with your MySQL credentials.

Upload ESP32 code from esp32/ to your ESP32-CAM.

Run Flask app:

python app.py


Open browser at http://127.0.0.1:5000

🎥 Demo
 <img width="1776" height="895" alt="image" src="https://github.com/user-attachments/assets/f6daebf6-c251-4499-8258-6709ce837323" />

📌 Future Improvements

🔑 Add JWT-based user authentication

☁️ Cloud deployment with Docker

📱 Mobile client for real-time alerts

👤 Author

Yamritech
