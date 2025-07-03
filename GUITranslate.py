import tkinter as tk
import Shot
import os
import MyOCR
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

def ss_toggle():
    ss_mode = var.get()
    # Bind to the left Alt key
    if ss_mode is True:
        # Make the window always stay on top
        #roots.attributes('-topmost', True)
        
        ss_label.place(relx=0.5, y = 45, anchor='center')  
        roots.bind("<Alt_L>", take_screen)
    else:
        ss_label.place_forget()
        roots.unbind("<Alt_L>")
    #print(ss_mode)

def take_screen(event):
    roots.withdraw()
    Shot.ScreenCaptureTool()
    get_text = MyOCR.get_ocr(s_lang)
    source_text.delete("1.0", tk.END)
    source_text.insert(tk.END, get_text)
    roots.deiconify()
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
        s_win.withdraw()
        #print("source: ",s_lang)
    tk.Button(s_win, text="Select Language", command=source_lang).pack()

def target_list():
    t_win = tk.Toplevel()
    t_win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+300)}')
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
        t_win.withdraw()
        #print("target: ",t_lang)
    tk.Button(t_win, text="Select Language", command=target_lang).pack()

def translating():
    nmt = radio_state.get()
    if nmt == 1:
        translated_text= GoogleTranslator(source='auto', target=t_lang).translate(source_text.get("1.0", tk.END))
    elif nmt == 2:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [source_text.get("1.0", tk.END)],
                "mime_type": "text/plain",
                "target_language_code": t_lang,
            }
        )
        translated_text=''
        for t in response.translations:
            translated_text += t.translated_text
            #detected_language = t.detected_language_code
            #print(detected_language)
    target_text.delete("1.0", tk.END)
    target_text.insert(tk.END, translated_text)
    #target_text.insert(tk.END, translated_text, "styled")
  
roots = tk.Tk()
roots.title("Nevar Translator")
roots.geometry(f"300x600+{roots.winfo_screenwidth()-330}+{80}")
  

var = tk.BooleanVar()
tk.Checkbutton(text="Screenshot Mode",
               font=('Times',10),
               variable= var, 
               command= ss_toggle
               ).place(relx=0.5, y = 20, anchor='center')

ss_label = tk.Label(text = "While this window pop up,\nuse LEFT ALT key to take Screenshot",
                 font= ('Times', 9, 'italic'))
 
tk.Label(text = "OCR Source :", font=('Times',12)).place(x=10, y = 80)
sl_button = tk.Button(text='English', font=('Times',11,'bold'), width=15, command=source_list)
sl_button.place(x=140, y = 77)

#Text
source_text = tk.Text(height=10, width=35)
#source_text.config(width=80)
source_text.focus()
source_text.place(relx=0.5,y=190,anchor='center')


tk.Button(text='Translate', 
          font=('Times',10), 
          width=10, command= translating
          ).place(relx=0.5, y = 300, anchor='center')


tk.Label(text = "Target Language :", font=('Times',12)).place(x=10, y = 345)
tl_button = tk.Button(text='Indonesian', font=('Times',11,'bold'), width=15, command=target_list)
tl_button.place(x=140, y = 342)

target_text = tk.Text(height=10, width=35)
target_text.place(relx=0.5,y=455,anchor='center')
#target_text.tag_configure("styled", font=("Helvetica", 10))

tk.Label(text = "Neural Machine Translation (NMT) :", font=('Times',12)).place(x=10, y = 550)
radio_state = tk.IntVar()
radio_state.set(1)
nmt_1 = tk.Radiobutton(text="Deep Translation",font=('Times',12), value=1, variable=radio_state).place(x=10, y = 570)
nmt_2 = tk.Radiobutton(text="Cloud Translation",font=('Times',12), value=2, variable=radio_state).place(x=150, y = 570)

roots.mainloop()
