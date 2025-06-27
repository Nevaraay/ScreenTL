import pytesseract
import Shot
import keyboard
from PIL import Image, ImageEnhance, ImageOps
from deep_translator import GoogleTranslator

    
while True:
    if keyboard.is_pressed('esc'):
        print("ESC pressed. Exiting...")
        break
    
    elif keyboard.is_pressed('ctrl+.'):
        # Take & Load image
        Shot.ScreenCaptureTool()
        img = Image.open("SSArea.png")
        img = ImageOps.expand(img, border=3, fill='black')

        # Enhance Image
        # Enhance contrast
        enhancer_contrast = ImageEnhance.Contrast(img)
        img_contrast = enhancer_contrast.enhance(2.0)  # 1.0 = original, >1 = more contrast

        # Enhance brightness
        enhancer_brightness = ImageEnhance.Brightness(img_contrast)
        img_bright = enhancer_brightness.enhance(1.0)  # 1.0 = original, >1 = brighter

        # Enhance sharpness
        enhancer_sharpness = ImageEnhance.Sharpness(img_bright)
        img_sharp = enhancer_sharpness.enhance(0.1)  # 1.0 = original, >1 = sharper
        
        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img_sharp, lang='eng')
        lines = text.split('\n')
        lin = ''
        for l in lines:
            lin += f'{l} '
        print(lin)
        print('--------------------------------------------')
        
        translated_text= GoogleTranslator(source='auto', target='id').translate(lin)
        print(translated_text)
        
    else:
        pass