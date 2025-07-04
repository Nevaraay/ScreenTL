import pytesseract
import re
from PIL import Image, ImageOps, ImageFilter

def get_ocr(lang):
    # Load & Enhance Image
    img = Image.open("SSArea.png")
    img = ImageOps.expand(img, border=1, fill='black')
    img = img.filter(ImageFilter.UnsharpMask(radius=0.75, percent=100, threshold=2))
    
    # Use tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang=lang)
    text = text.strip()
    linear_text = re.sub(r'\s+',' ', text) #replace any whitespace chars (space,tab,newline) to a single space
    
    return linear_text