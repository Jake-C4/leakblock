import pytesseract

# Force path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image

def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)
