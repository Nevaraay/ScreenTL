import pytesseract
import Shot
import keyboard
from PIL import Image
from googletrans import Translator

    
while True:
    if keyboard.is_pressed('esc'):
        print("ESC pressed. Exiting...")
        break
    
    elif keyboard.is_pressed('ctrl+.'):
        # Take & Load image
        Shot.ScreenCaptureTool()
        img = Image.open("SSArea.png")

        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, lang='eng')
        lines = text.split('\n')
        lin = ''
        for l in lines:
            lin += f'{l} '
        print(lin)
        print('--------------------------------------------')
        
        translator = Translator()
        translated_text = translator.translate(lin, src='en', dest='id').text
        print(translated_text)
        
    else:
        pass