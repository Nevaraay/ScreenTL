import cv2
import numpy as np
from PIL import ImageGrab, Image, ImageDraw, ImageFont

def text_out(x1,y1,x2,y2,text):
    # Capture fullscreen screenshot
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)  # red rectangle

   
    # --- 3. Convert OpenCV image to PIL
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # --- 4. Define text and font
    text = text
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)
    
    # --- 5. Calculate max box size
    box_width = x2 - x1
    box_height = y2 - y1

    # --- 6. Wrap the text to fit width
    def wrap_text(text, font, max_width):
        lines = []
        for paragraph in text.split('\n'):
            line = ''
            for word in paragraph.split():
                test_line = line + (' ' if line else '') + word
                if font.getbbox(test_line)[2] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        return lines

    lines = wrap_text(text, font, box_width)

    # --- 7. If text too tall, reduce font size to fit
    line_height = font.getbbox("Ay")[3] + 5  # line height with spacing

    while len(lines) * line_height > box_height and font_size > 10:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(text, font, box_width)
        line_height = font.getbbox("Ay")[3] + 5

    # --- 8. Draw text inside the rectangle (top-aligned or centered)
    y_text = y1 + (box_height - len(lines) * line_height) // 2  # vertically center
    for line in lines:
        draw.text((x1 + 5, y_text), line, font=font, fill=(0, 0, 0))
        y_text += line_height

    # --- 9. Convert back to OpenCV and display
    img_result = np.array(img_pil)


    # Show image
    cv2.namedWindow("Screenshot", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Screenshot", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Screenshot", img_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    