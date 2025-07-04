import tkinter as tk
import Shot
import os
import MyOCR
import pycountry
from langdetect import detect
from deep_translator import GoogleTranslator
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account

# Look for .json files in the current directory
json_files = [f for f in os.listdir(".") if f.endswith(".json")]

if len(json_files) != 1:
    raise FileNotFoundError(f"Expected exactly one JSON file, found {len(json_files)}: {json_files}")

SERVICE_ACCOUNT_KEY_PATH = json_files[0] 
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


lang_list = ["English","Simplified Chinese","Traditional Chinese","Korean",
                 "Japanese","Indonesian","Italian"]
lang_list = sorted(lang_list)

source_lang_codes = {
    "English": "eng",
    "Simplified Chinese": "chi_sim",
    "Traditional Chinese": "chi_tra", 
    "Korean": "kor",
    "Japanese": "jpn",
    "Indonesian": "ind",
    "Italian": "ita"
}

target_lang_codes = {
    "English": "en",
    "Simplified Chinese": "zh-CN",
    "Traditional Chinese": "zh-TW",
    "Korean": "ko",
    "Japanese": "ja",
    "Indonesian": "id",
    "Italian": "it"
}

s_lang = "eng"
t_lang = "id"
ss_mode = False
ex_mode = False

def get_language_name(lang_code):
    try:
        language = pycountry.languages.get(alpha_2=lang_code)
        return language.name
    except:
        return "Unknown"

def ss_toggle():
    ss_mode = ss_var.get()
    # Bind to the left Alt key
    if ss_mode is True:
        # Make the window always stay on top
        #roots.attributes('-topmost', True)
        ss_label.place(relx=1.0, rely=0.0, anchor='ne')
        ocr_label.place(x=10, y = 45)
        sl_button.place(x=140, y = 45)
        roots.bind("<Alt_L>", take_screen)
    else:
        roots.geometry(f"300x600")
        ss_label.place_forget()
        ocr_label.place_forget()
        sl_button.place_forget()
        roots.unbind("<Alt_L>")
    #print(ss_mode)
    
def expand():
    ex_mode = ex_var.get()
    if ex_mode is True:
        roots.geometry(f"600x600+{roots.winfo_screenwidth()-630}+{80}")
        source_text.config(width=73)
        target_text.config(width=73)
        ss_label.config(text="While this window pop up, press L_ALT to capture screen")
    else:
        roots.geometry(f"300x600+{roots.winfo_screenwidth()-330}+{80}")
        source_text.config(width=35)
        target_text.config(width=35)
        ss_label.config(text="While this window pop up,\npress L_ALT to capture screen")

def take_screen(event):
    roots.withdraw()
    Shot.ScreenCaptureTool() 
    get_text = MyOCR.get_ocr(s_lang)
    roots.deiconify()
    source_text.delete("1.0", tk.END)
    source_text.insert(tk.END, get_text)
    translating()
    #roots.focus_set() # Optional: Give focus back to the window
    
    
def source_list():
    s_win = tk.Toplevel()
    s_win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+100)}')
    s_lb = tk.Listbox(s_win,height=4)
    for item in lang_list:
        s_lb.insert(tk.END, item)
    s_lb.pack()
    def source_lang():
        global s_lang
        #print("Source Language: ",lb.get(lb.curselection()))
        s_lang = source_lang_codes[s_lb.get(s_lb.curselection())]
        sl_button.config(text=s_lb.get(s_lb.curselection()))
        s_win.destroy()
        #print("source: ",s_lang)
    tk.Button(s_win, text="Select Language", command=source_lang).pack()

def target_list():
    t_win = tk.Toplevel()
    t_win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+400)}')
    t_lb = tk.Listbox(t_win,height=4)
    for item in lang_list:
        t_lb.insert(tk.END, item)
    t_lb.pack()
    def target_lang():
        global t_lang
        # Gets current selection from listbox
        #print("Target Language: ",lb.get(lb.curselection()))
        t_lang = target_lang_codes[t_lb.get(t_lb.curselection())]
        tl_button.config(text=t_lb.get(t_lb.curselection()))
        t_win.destroy()
        #print("target: ",t_lang)
    tk.Button(t_win, text="Select Language", command=target_lang).pack()

def translating():
    text_to_translate = source_text.get("1.0", tk.END)
    nmt = radio_state.get()
    if nmt == 1:
        d_lang = detect(text_to_translate)
        translated_text= GoogleTranslator(source='auto', target=t_lang).translate(text_to_translate)
    elif nmt == 2:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_to_translate],
                "mime_type": "text/plain",
                "target_language_code": t_lang,
            }
        )
        translated_text=''
        for t in response.translations:
            translated_text += t.translated_text
            d_lang = t.detected_language_code
            #print(detected_language)
    target_text.delete("1.0", tk.END)
    target_text.insert(tk.END, translated_text)
    #target_text.insert(tk.END, translated_text, "styled")
    language_name = get_language_name(d_lang[:2])
    detect_lang.config(text = f"Source Language : {language_name}")
  
roots = tk.Tk()
roots.title("Nevar Translator")
roots.geometry(f"300x600+{roots.winfo_screenwidth()-330}+{80}")
roots.resizable(False, False) 
  

ss_var = tk.BooleanVar()
tk.Checkbutton(text="Screenshot Mode",
               font=('Times',10),
               variable= ss_var, 
               command= ss_toggle
               ).place(x=10, y = 0)

ex_var = tk.BooleanVar()
tk.Checkbutton(text="Expand",
               font=('Times',10),
               variable= ex_var, 
               command= expand
               ).place(relx=0.5,x=-100, y = 315, anchor='center')

ss_label = tk.Label(text = "While this window pop up,\npress L_ALT to capture screen",
                 font= ('Times', 9, 'italic'))
 
ocr_label = tk.Label(text = f"OCR Source :", font=('Times',12))

sl_button = tk.Button(text='English', font=('Times',11,'bold'), width=15, command=source_list)



detect_lang = tk.Label(text = "Source Language : Auto", font=('Times',12))
detect_lang.place(x=10, y = 95)


#Text
source_text = tk.Text(height=10, width=35)
source_text.focus()
source_text.place(relx=0.5,y=205,anchor='center')


tk.Button(text='Translate', 
          font=('Times',10), 
          width=10, command= translating
          ).place(relx=0.5, y = 315, anchor='center')


tk.Label(text = "Target Language :", font=('Times',12)).place(x=10, y = 345)
tl_button = tk.Button(text='Indonesian', font=('Times',11,'bold'), width=15, command=target_list)
tl_button.place(x=140, y = 342)

target_text = tk.Text(height=10, width=35)
target_text.place(relx=0.5,y=455,anchor='center')
#target_text.tag_configure("styled", font=("Helvetica", 10))

tk.Label(text = "Neural Machine Translation (NMT) :", font=('Times',10)).place(x=10, y = 545)
radio_state = tk.IntVar()
radio_state.set(1)
nmt_1 = tk.Radiobutton(text="Deep Translation\n(max = 5k chars)",font=('Times',10), value=1, variable=radio_state).place(x=10, y = 560)
nmt_2 = tk.Radiobutton(text="Cloud Translation\n(recommended ≤ 10k)",font=('Times',10), value=2, variable=radio_state).place(x=150, y = 560)

roots.mainloop()
