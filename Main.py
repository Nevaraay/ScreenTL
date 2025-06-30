import pytesseract
import Shot
import keyboard
import os
import Textout
from PIL import Image, ImageOps, ImageFilter
from google.cloud import translate_v2 as translate
from pynput import keyboard

# Set the path to your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "imagetranslation-464309-0033b5674b8a.json"
# Initialize the client
translate_client = translate.Client()

# Track which keys are currently pressed
current_keys = set()

def on_press(key):
    current_keys.add(key)

    if (key == keyboard.Key.alt_l  or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr):    
        # Take image
        shoot = Shot.ScreenCaptureTool()
        x1,y1 = shoot.start_x, shoot.start_y
        x2,y2 = shoot.end_x, shoot.end_y
        
        # Load & Enhance Image
        img = Image.open("SSArea.png")
        img = ImageOps.expand(img, border=1, fill='black')
        img = img.filter(ImageFilter.UnsharpMask(radius=0.75, percent=100, threshold=2))
        
        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, lang='kor')
        lines = text.strip().split('\n')
        lin = ''
        for l in lines:
            lin += f'{l}'
        print(lin)
        print('-------------------------------------------------------------------------------------------------------------------------')
        
        # Translate text
        translated_text = translate_client.translate(text, target_language="en")
        Textout.text_out(x1,y1,x2,y2,translated_text["translatedText"])
            
def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

# Start listening
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()