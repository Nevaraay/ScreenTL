import pytesseract
import cshot
import keyboard
import Textout
from PIL import Image, ImageOps, ImageFilter
from pynput import keyboard
from deep_translator import GoogleTranslator
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account

SERVICE_ACCOUNT_KEY_PATH = "imagetranslation-464309-0033b5674b8a.json" 
LOCATION = 'global'
# Load credentials from the service account JSON file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY_PATH
)

# Get the project ID from the loaded credentials
project_id = credentials.project_id
if not project_id:
    raise ValueError("Project ID not found in service account key file.")

client = translate.TranslationServiceClient(credentials=credentials)
parent = f"projects/{project_id}/locations/{LOCATION}"

# Track which keys are currently pressed
current_keys = set()

def on_press(key):
    current_keys.add(key)

    if (key == keyboard.Key.alt_l  or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr):    
        # Take image
        shoot = cshot.ScreenCaptureTool()
        x1,y1 = shoot.start_x, shoot.start_y
        x2,y2 = shoot.end_x, shoot.end_y
        
        # Load & Enhance Image
        img = Image.open("SSArea.png")
        img = ImageOps.expand(img, border=1, fill='black')
        img = img.filter(ImageFilter.UnsharpMask(radius=0.75, percent=100, threshold=2))
        
        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, lang='chi_sim')
        lines = text.strip().split('\n')
        linear_text = ''
        for l in lines:
            linear_text += f'{l}'
        print(linear_text)
        print('-------------------------------------------------------------------------------------------------------------------------')
        
        # Translate text
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [linear_text],
                "mime_type": "text/plain",
                "target_language_code": 'en',
            }
        )
        translated_text=''
        for t in response.translations:
                translated_text += t.translated_text
                
        Textout.text_out(x1,y1,x2,y2,translated_text)
        print(translated_text)
        print('-------------------------------------------------------------------------------------------------------------------------')
        #translated_text= GoogleTranslator(source='auto', target='en').translate(linear_text)
        #print(translated_text)
        #print('')
            
def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

# Start listening
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()