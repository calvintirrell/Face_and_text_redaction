from PIL import Image
import cv2
import pytesseract
from pytesseract import Output

# For Apple Silicon Macs (M1, M2, etc)
# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# For Intel-based Macs; Install homebrew and then run: "brew install tesseract"
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def redact_faces_and_text(image_path, output_path):
    """
    Redacts both faces and text in an image.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path where the redacted image will be saved.

    Returns:
        None
    """
    try:
        # Load the image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Face Detection and Redaction ---
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)  # Black rectangle for redaction

        # --- Text Detection and Redaction ---
        text_data = pytesseract.image_to_data(gray, output_type=Output.DICT)
        for i, word in enumerate(text_data['text']):
            if word.strip():
                (x, y, w, h) = (text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)  # Black rectangle for redaction

        # Save the redacted image
        cv2.imwrite(output_path, img)
        print(f"Image with redacted faces and text saved: {output_path}")

    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        print("Please make sure the image path is correct and Tesseract OCR is installed properly.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ai_privacy_filter(image_path, output_path):
    """
    Applies AI privacy filters to an image: redacts faces and text using a single function.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path where the redacted image will be saved.

    Returns:
        None
    """
    print("Redacting faces and sensitive text...")
    redact_faces_and_text(image_path, output_path)

# Example usage
ai_privacy_filter("input.jpg", "output.jpg")