import pytesseract
from PIL import Image, ImageOps, ImageFilter

def get_ocr(event):
    # Load & Enhance Image
    img = Image.open("SSArea.png")
    img = ImageOps.expand(img, border=1, fill='black')
    img = img.filter(ImageFilter.UnsharpMask(radius=0.75, percent=100, threshold=2))
    
    # Use tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='kor')
    lines = text.strip().split('\n')
    linear_text = ''
    for l in lines:
        linear_text += f'{l}'
    
    return linear_text