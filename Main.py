import pytesseract
import Shot
import keyboard
import os
from PIL import Image, ImageEnhance, ImageOps
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

    if (keyboard.Key.alt_l in current_keys or keyboard.Key.alt_r in current_keys):
        current_keys.discard(key)
        
        # Take & Load image
        Shot.ScreenCaptureTool()
        img = Image.open("SSArea.png")
        img = ImageOps.expand(img, border=1, fill='black')
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
        text = pytesseract.image_to_string(img_sharp, lang='kor')
        lines = text.strip().split('\n')
        lin = ''
        for l in lines:
            lin += f'{l} '
        print(lin)
        print('-------------------------------------------------------------------------------------------------------------------------')
        
        # Translate text
        translated_text = translate_client.translate(text, target_language="en")
        print(translated_text["translatedText"])
        print('')
            
def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

# Start listening
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()