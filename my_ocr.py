from paddleocr import PaddleOCR
import os
import re
from google.cloud import vision

# Look for .json files in the current directory
json_files = [f for f in os.listdir(".") if f.endswith(".json")]

if len(json_files) != 1:
    raise FileNotFoundError(f"Expected exactly one JSON file, found {len(json_files)}: {json_files}")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_files[0]

def visi_ocr(img_name):
    with open(img_name, "rb") as image_file:
        content = image_file.read()

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    # Call the OCR method
    response = client.document_text_detection(image=image)

    # Get the TextAnnotation object
    text_annotation = response.full_text_annotation

    linear_text = re.sub(r'\s+',' ', text_annotation.text) #replace any whitespace chars (space,tab,newline) to a single space
    
    return linear_text

def padd_init(lang='en'):
    ocr = PaddleOCR(
        lang=lang, # Specify French recognition model with the lang parameter
        use_doc_orientation_classify=False, # Disable document orientation classification model
        use_doc_unwarping=False, # Disable text image unwarping model
        use_textline_orientation=False, # Disable text line orientation classification model
    )
    return ocr

def padd_ocr(ocr,img_name):
    result = ocr.predict(img_name)
    linear_text = ' '.join(result[0]['rec_texts'])
    
    return linear_text