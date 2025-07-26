import tkinter as tk
import subprocess
import re
import cshot
import my_lang_dict
import my_ocr
import my_translator
import translation_history as th
import pycountry
from langdetect import detect
from deep_translator import GoogleTranslator

client = my_translator.client
parent = my_translator.parent
lang_list = my_lang_dict.lang_list
source_lang_codes = my_lang_dict.source_lang_codes
target_lang_codes = my_lang_dict.target_lang_codes

t_lang = "id"
target_language = "Indonesian"
ss_mode = False
ex_mode = False

history = th.TranslationHistory()

def non_whitespace(text):
    return bool(re.search(r'\S', text))  #True if there is a char other than whitespace 

def get_language_name(lang_code):
    try:
        language = pycountry.languages.get(alpha_2=lang_code)
        return language.name
    except:
        return "Unknown"

def ocr_lang():
    ocr = ocr_state.get()
    if ocr == 1:
        sl_button.place(x=140, y = 25)
        ocrm_1.config(text = "Paddle   ===>", fg='sky blue')
        ocrm_2.config(text = "Google Vision", fg='black')
    elif ocr == 2:
        sl_button.place_forget()
        ocrm_1.config(text = "Paddle", fg='black')
        ocrm_2.config(text = "Google Vision (Auto-detect)", fg='sky blue')
    else:
        sl_button.place_forget()
        ocrm_1.config(text = "Paddle", fg='black')
        ocrm_2.config(text = "Google Vision", fg='black')
        
        
def coll():
    ex_mode = ex_var.get()
    ss_mode = ss_var.get()
    if ex_mode is True & ss_mode is True:
        collect_button.place(relx=0.98,rely=0.0, anchor='ne')
    else:
        collect_button.place_forget()
        

def ss_toggle():
    coll()
    ss_mode = ss_var.get()
    if ss_mode is True:
        #ss_label.place(relx=1.0, rely=0.0, anchor='ne')
        ss_label.place(x=80, y = 2)
        ocrm_1.place(x=10, y = 25)
        ocrm_2.place(x=10, y = 55)
        roots.bind("<Alt_L>", take_screen)
    else:
        ss_label.place_forget()
        ocrm_1.place_forget()
        ocrm_2.place_forget()
        roots.unbind("<Alt_L>")
        ocr_state.set(0)
        ocr_lang()
        
    
def expand():
    coll()
    ex_mode = ex_var.get()
    if ex_mode is True:
        roots.geometry(f"600x600+{roots.winfo_screenwidth()-630}+{80}")
        source_text.config(width=73)
        target_text.config(width=73)
        
    else:
        roots.geometry(f"300x600+{roots.winfo_screenwidth()-330}+{80}")
        source_text.config(width=35)
        target_text.config(width=35)
        
     

def take_screen(event):
    img_name = "SSArea.png"
    col = col_var.get()
    ocr = ocr_state.get()
    source_text.config(fg="black")
    get_text = ''
    if ocr >=  1:
        roots.withdraw()
        cshot.ScreenCaptureTool(img_name) 
        roots.deiconify()
        
    if ocr == 1:
        try:
            get_text = my_ocr.padd_ocr(paddle_ocr,img_name)
        except Exception as e:
            source_text.config(fg="red")
            source_text.insert(tk.END, e)
            
    elif ocr == 2:
        try:
            get_text = my_ocr.visi_ocr(img_name)
        except Exception as e:
            source_text.config(fg="red")
            source_text.insert(tk.END, e)
    else:
        source_text.config(fg="red")
        source_text.delete("1.0", tk.END)
        source_text.insert(tk.END, "Please select OCR type")
    
    if col is True and ocr >= 1:
        source_text.insert(tk.END, get_text+"\n")
        pass
    elif col is False and ocr >= 1:
        source_text.delete("1.0", tk.END)
        source_text.insert(tk.END, get_text+"\n")
        translating()
    
      
def source_list():
    s_win = tk.Toplevel()
    s_win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+100)}')
    s_lb = tk.Listbox(s_win,height=4)
    for item in lang_list:
        s_lb.insert(tk.END, item)
    s_lb.pack()
    def source_lang():
        global s_lang
        global paddle_ocr
        select_source = s_lb.get(s_lb.curselection())
        s_lang = source_lang_codes[select_source]
        if 'select_source' in locals():
            paddle_ocr = my_ocr.padd_init(s_lang)
        sl_button.config(text=select_source)
        s_win.destroy()  
    tk.Button(s_win, text="OK", command=source_lang).pack()
    

def target_list():
    t_win = tk.Toplevel()
    t_win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+400)}')
    t_lb = tk.Listbox(t_win,height=4)
    for item in lang_list:
        t_lb.insert(tk.END, item)
    t_lb.pack()
    def target_lang():
        global t_lang
        global target_language
        target_language = t_lb.get(t_lb.curselection())
        t_lang = target_lang_codes[target_language]
        tl_button.config(text=t_lb.get(t_lb.curselection()))
        t_win.destroy()
    
    tk.Button(t_win, text="OK", command=target_lang).pack()

def translating():
    text_to_translate = source_text.get("1.0", "end-1c")
    count = len(text_to_translate)
    nmt = nmt_state.get()
    target_text.delete("1.0", tk.END)
    if non_whitespace(text_to_translate) is True:
        if nmt == 1 and count <= 5000:
            try:
                d_lang = detect(text_to_translate)
                translated_text= GoogleTranslator(source='auto', target=t_lang).translate(text_to_translate)
                target_text.config(fg="black")       
                target_text.insert(tk.END, translated_text)
                source_language = get_language_name(d_lang[:2])
                detect_lang.config(text = f"Source : {source_language}")
                history.insert_row([source_language,target_language,text_to_translate,translated_text])
                
            except Exception as e:
                print(e)
                target_text.config(fg="red")
                target_text.insert(tk.END, e)
            
        elif nmt == 2 and count <= 10000:
            try:
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
                    
                target_text.config(fg="black")       
                target_text.insert(tk.END, translated_text)
                source_language = get_language_name(d_lang[:2])
                detect_lang.config(text = f"Source : {source_language}")
                history.insert_row([source_language,target_language,text_to_translate,translated_text])
                
            except Exception as e:
                target_text.config(fg="red")
                target_text.insert(tk.END, e)
        
        else:
            target_text.config(fg="red")
            target_text.insert(tk.END, "Text is overlimit")
            detect_lang.config(text = f"Source : Auto-detect")
            
    else:
        target_text.config(fg="red")
        target_text.insert(tk.END, "No Text")
  
roots = tk.Tk()
roots.title("Nevar Translator")
roots.geometry(f"300x600+{roots.winfo_screenwidth()-330}+{80}")
roots.resizable(False, False) 
  

ss_var = tk.BooleanVar()
tk.Checkbutton(text="OCR",
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

col_var = tk.BooleanVar()
collect_button = tk.Checkbutton(text="Collect Mode",
               font=('Times',10),
               variable= col_var)

ss_label = tk.Label(text = "(While this window pop up, press L_ALT)",
                 font= ('Times', 9, 'italic'))

sl_button = tk.Button(text='Select Language', font=('Times',11,'bold'), 
                      fg= 'sky blue',width=15, command=source_list)



detect_lang = tk.Label(text = "Source : Auto-detect", font=('Times',12))
detect_lang.place(x=10, y = 95)


#Text
def text_count(event):
    nmt = nmt_state.get()
    source_text.edit_modified(False)  # Reset the modified flag
    content = source_text.get("1.0", "end-1c")  # Get all text, excluding trailing newline
    if nmt == 1:
        char_count.set(f"{len(content)}/5000")
    elif nmt == 2:
        char_count.set(f"{len(content)}/10000")
        

# StringVar to update label dynamically
char_count = tk.StringVar()
char_count.set("0/0")
tk.Label(textvariable=char_count).place(relx=0.98, y = 100, anchor='ne')

source_text = tk.Text(height=10, width=35)
source_text.focus()
source_text.place(relx=0.5,y=205,anchor='center')

# Bind the <<Modified>> virtual event to the text widget
source_text.bind("<<Modified>>", text_count)


tk.Button(text='Translate', 
          font=('Times',10, 'bold'), 
          width=10, command= translating, fg = 'sea green', 
          ).place(relx=0.5, y = 315, anchor='center')

tk.Button(text='History', 
          font=('Times', 8, 'bold','italic'), 
          width=10, command= lambda: subprocess.Popen(["streamlit", "run", "stream.py"]), 
          bg = 'slate grey', fg = 'white'
          ).place(relx=0.5,x = 105, y = 315, anchor='center')

tk.Label(text = "Target :", font=('Times',12)).place(x=10, y = 345)
tl_button = tk.Button(text='Indonesian', font=('Times',11,'bold'), 
                      fg = 'crimson', width=15, command=target_list)
tl_button.place(x=70, y = 342)

target_text = tk.Text(height=10, width=35)
target_text.place(relx=0.5,y=455,anchor='center')
#target_text.tag_configure("styled", font=("Helvetica", 10))

tk.Label(text = "Neural Machine Translation (NMT) :", font=('Times',10)).place(x=10, y = 545)
nmt_state = tk.IntVar()
nmt_state.set(1)
tk.Radiobutton(text="Deep Translation\n(max = 5k chars)",font=('Times',10), value=1, variable=nmt_state
                       ).place(x=10, y = 560)
tk.Radiobutton(text="Cloud Translation\n(recommended ≤ 10k)",font=('Times',10), value=2, variable=nmt_state
                       ).place(x=150, y = 560)

ocr_state = tk.IntVar()
ocrm_1 = tk.Radiobutton(text = "Paddle",font=('Times',12), value=1, variable=ocr_state, command= ocr_lang)
ocrm_2 = tk.Radiobutton(text = "Google Vision",font=('Times',12), value=2, variable=ocr_state, command=ocr_lang)

roots.protocol("WM_DELETE_WINDOW", lambda: (history.conn.close(), roots.destroy()))
roots.mainloop()
