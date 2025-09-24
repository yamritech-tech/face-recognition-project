import pymysql
import cv2
import numpy as np
import requests
from imgbeddings import imgbeddings
from PIL import Image
import io

def capture_and_insert_image():
    name = input("Entrez le nom de l'individu : ")

    # URL of the ESP32-CAM
    url = "http://10.99.130.168/capture"

    try:
        # Send a GET request to capture an image from the ESP32-CAM
        response = requests.get(url)
        if response.status_code == 200:
            # Convert the image bytes to a numpy array
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                print("Erreur : Impossible de décoder l'image.")
                return

            cv2.imshow("Image Capturée", img)
            print("Appuyez sur une touche pour continuer...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Convert image to RGB for imgbeddings
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            ibed = imgbeddings()
            embedding = ibed.to_embeddings(pil_img)
            embedding = np.array(embedding[0], dtype=np.float32)
            print(f"Generated embedding length for {name}: {len(embedding)}")

            # Connect to MySQL database
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='system',
                database='reconnaissance_faciale'
            )

            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO faces (name, face_embedding) VALUES (%s, %s)"
                    cursor.execute(sql, (name, embedding.tobytes()))

                connection.commit()
                print("Image capturée et insérée avec succès pour l'individu :", name)

            except Exception as e:
                print(f"Erreur lors de l'insertion de l'image : {e}")
                connection.rollback()

            finally:
                connection.close()

        else:
            print("Erreur : Impossible de récupérer l'image depuis l'ESP32-CAM.")

    except Exception as e:
        print(f"Erreur générale : {e}")

capture_and_insert_image()
