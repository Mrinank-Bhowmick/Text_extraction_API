import pathlib
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "absolute path of tesseract.exe"

BASE_DIR=pathlib.Path(__file__).parent  # Will return the path of this file
IMG_DIR=BASE_DIR/"images"
img_path=IMG_DIR/'ingredients-1.png'

img=Image.open(img_path)
prediction=pytesseract.image_to_string(img)
print(prediction)