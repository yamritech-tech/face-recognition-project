from flask import Flask, request, jsonify
import numpy as np
import pymysql
from imgbeddings import imgbeddings
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection function
def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="system",
        database="reconnaissance_faciale",
        #charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch known faces from the database
def fetch_known_faces():
    known_faces = []
    known_names = []
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, face_embedding FROM faces")
    rows = cursor.fetchall()
    for row in rows:
        name = row['name']
        embedding = np.frombuffer(row['face_embedding'], dtype=np.float32)
        print(f"Fetched embedding length for {name}: {len(embedding)}")
        known_faces.append(embedding)
        known_names.append(name)
    cursor.close()
    db.close()
    return known_faces, known_names

# Route for recognizing faces
@app.route('/recognize', methods=['POST'])
def recognize_face():
    try:
        # Check if the image is in the request
        if 'image' not in request.files:
            return jsonify({"result": "No image part"}), 400
        image_file = request.files['image']
        print("Image received")

        # Read and process the image
        img_bytes = image_file.read()
        img = Image.open(io.BytesIO(img_bytes))
        print("Image processed")

        # Generate embeddings for the received image
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(img)
        embedding = np.array(embedding[0], dtype=np.float32)
        print(f"Generated embedding length: {len(embedding)}")
        print(f"Generated embedding: {embedding}")

        # Fetch known faces from the database
        known_faces, known_names = fetch_known_faces()

        if len(known_faces) == 0:
            return jsonify({"result": "No known faces in the database"}), 400

        # Compare the received face embedding with the known faces
        matches = []
        for idx, known_embedding in enumerate(known_faces):
            distance = np.linalg.norm(embedding - known_embedding)
            print(f"Distance to {known_names[idx]}: {distance}")
            matches.append(distance)

        # Find the best match
        best_match_idx = np.argmin(matches)
        print(f"Best match index: {best_match_idx}, Distance: {matches[best_match_idx]}")

        # Adjust threshold for recognizing faces
        threshold = 12

        if matches[best_match_idx] < threshold:
            recognized_name = known_names[best_match_idx]
            print(f"Recognized: {recognized_name}")
            return jsonify({"result": f"Recognized face: {recognized_name}"}), 200
        else:
            print("Face not recognized")
            return jsonify({"result": "Face not recognized"}), 200

    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        print(f"Error: {str(e)}")
        return jsonify({"result": f"Error: {str(e)}"}), 500

# Route to upload new face for recognition
@app.route('/upload', methods=['POST'])
def upload_face():
    try:
        # Ensure that both image and name are provided in the request
        if 'image' not in request.files or 'name' not in request.form:
            return jsonify({"result": "No image or name provided"}), 400
        image_file = request.files['image']
        name = request.form['name']
        img_bytes = image_file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # Generate embeddings for the uploaded image
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(img)
        embedding = np.array(embedding[0], dtype=np.float32)
        print(f"Generated embedding length for {name}: {len(embedding)}")
        print(f"Generated embedding: {embedding}")

        # Save the embedding and name to the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO faces (name, face_embedding) VALUES (%s, %s)",
                       (name, embedding.tobytes()))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"result": f"Face of {name} uploaded successfully"}), 200

    except Exception as e:
        app.logger.error(f"Error uploading face: {str(e)}")
        print(f"Error: {str(e)}")
        return jsonify({"result": f"Error: {str(e)}"}), 500

# Main entry point for the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
