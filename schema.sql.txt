CREATE DATABASE reconnaissance_faciale;
USE reconnaissance_faciale;

CREATE TABLE faces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    face_embedding BLOB NOT NULL
);
