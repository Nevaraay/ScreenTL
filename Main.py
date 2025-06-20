import pytesseract
from PIL import Image
from googletrans import Translator

# Load image
img = Image.open('korean.PNG')

# Use tesseract to do OCR on the image
text = pytesseract.image_to_string(img, lang='kor')  # 'kor' for Korean
print(text)
print('')
translator = Translator()

translated_text = translator.translate(text, src='ko', dest='en').text
print(translated_text)