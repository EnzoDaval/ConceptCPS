import cv2
import os
from Face_recognition.face_recognition import face_recognition_cli


class CameraManager:
    def __init__(self):
        # Spécifier les chemins des dossiers d'entrée et de sortie
        self.input_folder = 'Images/Image_to_analyze'
        self.output_folder = 'Images/Image_analyzed'

    """
    On récupère 5 images de la camera, elles sont stockées dans /Images/Images_to_analyze
    /!\ Ne pas oublier d'avoir le VPN activé
    """

    def recuperation_images(self):
        flux_video = cv2.VideoCapture("rtsp://user:2S7c7-cpDs6Y6UqQ_HTD@192.168.215.102")
        # Créer un dossier "Images" s'il n'existe pas déjà
        output_folder = 'Images/Image_to_analyze'
        os.makedirs(output_folder, exist_ok=True)

        # Boucle pour enregistrer 5 images
        for i in range(5):
            # Lire le flux vidéo à chaque itération pour capturer une nouvelle image
            ret, frame = flux_video.read()

            # Vérifier si la lecture est réussie
            if not ret:
                print("La lecture du flux vidéo a échoué.")
                break

            # Enregistrer l'image dans le dossier spécifié avec un nom de fichier unique
            file_path = os.path.join(output_folder, f'Image_{i + 1}.jpg')
            cv2.imwrite(file_path, frame)

            # Afficher le chemin du fichier (facultatif)
            print(f"Image enregistrée à : {file_path}")

            # Attente pour capturer la prochaine image (ajustez selon vos besoins)
            cv2.waitKey(2000)

        flux_video.release()
        cv2.destroyAllWindows()

    """
    On fait de la detection de visage sur les images provenant de la camera, stockés dans /Images/Images_to_analyze
    """

    def detect_and_save_faces(self, image_path, output_folder):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Lire l'image depuis le chemin spécifié
        frame = cv2.imread(image_path)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter les visages dans l'image
        faces = face_cascade.detectMultiScale(gray_img, 1.1, 4)
        print(f"{len(faces)} faces detected in {image_path}.")

        # Dessiner des rectangles autour des visages détectés
        for x, y, width, height in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), color=(0, 255, 0), thickness=2)

        # Enregistrer l'image avec les rectangles dans le dossier spécifié
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        cv2.imwrite(output_path, frame)
        print(f"Image avec visages détectés enregistrée à : {output_path}")

    def analyze_images_in_folder(self):
        # Créer le dossier de sortie s'il n'existe pas déjà
        os.makedirs(self.output_folder, exist_ok=True)

        # Parcourir toutes les images dans le dossier d'entrée
        for filename in os.listdir(self.input_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.input_folder, filename)
                self.detect_and_save_faces(image_path, self.output_folder)

    def launch_face_recognition(self):
        face_recognition_cli.main(self.input_folder, self.output_folder)