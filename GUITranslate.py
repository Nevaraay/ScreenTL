import tkinter as tk
import Shot
import MyOCR
from deep_translator import GoogleTranslator

ss_mode = False

def ss_toggle():
    ss_mode = var.get()
    # Bind to the left Alt key
    if ss_mode is True:
        tk.Label(text = "When this window appear,\nuse LEFT ALT key to take ScreenShoot",
                 font= ('Times', 9, 'italic')
                 ).place(relx=0.5, y = 45, anchor='center')  
        roots.bind("<Alt_L>", take_screen)
    else:
        roots.unbind("<Alt_L>")
    print(ss_mode)

def take_screen(event):
    roots.withdraw()
    Shot.ScreenCaptureTool()
    get_text = MyOCR.get_ocr("SSArea.png")
    source_text.delete("1.0", tk.END)
    source_text.insert(tk.END, get_text)
    roots.deiconify()
    translating()
    #roots.focus_set() # Optional: Give focus back to the window
    
def source_list():
    win = tk.Toplevel()
    win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+100)}')
    lb = tk.Listbox(win,height=4)
    for item in ["Apple", "Banana", "Cherry"]:
        lb.insert(tk.END, item)
    lb.pack()
    def source_lang():
        print("Source Language: ",lb.get(lb.curselection()))
        sl_button.config(text=lb.get(lb.curselection()))
        win.withdraw()
    tk.Button(win, text="Select Language", command=source_lang).pack()

def target_list():
    win = tk.Toplevel()
    win.geometry(f'100x100+{str(int(roots.winfo_x())+150)}+{str(int(roots.winfo_y())+300)}')
    lb = tk.Listbox(win,height=4)
    for item in ["Apple", "Banana", "Cherry"]:
        lb.insert(tk.END, item)
    lb.pack()
    def target_lang():
        # Gets current selection from listbox
        print("Target Language: ",lb.get(lb.curselection()))
        sl_button.config(text=lb.get(lb.curselection()))
        win.withdraw()
    tk.Button(win, text="Select Language", command=target_lang).pack()

def translating():
    translated_text= GoogleTranslator(source='auto', target='id').translate(source_text.get("1.0", tk.END))
    target_text.delete("1.0", tk.END)
    target_text.insert(tk.END, translated_text)
    #target_text.insert(tk.END, translated_text, "styled")
    
roots = tk.Tk()
roots.title("Nevar Translator")
roots.geometry(f"300x450+{roots.winfo_screenwidth()-330}+{100}")
  

var = tk.BooleanVar()
tk.Checkbutton(text="Screenshot Mode",
               font=('Times',10),
               variable= var, 
               command= ss_toggle
               ).place(relx=0.5, y = 20, anchor='center')
 
tk.Label(text = "Source Language :", font=('Times',12)).place(x=10, y = 80)
sl_button = tk.Button(text='English', font=('Times',11,'bold'), width=15, command=source_list)
sl_button.place(x=140, y = 77)

#Text
source_text = tk.Text(height=6, width=35)
source_text.focus()
#print(source_text.get("1.0", tk.END))
source_text.place(relx=0.5,y=160,anchor='center')


tk.Button(text='Translate', 
          font=('Times',10), 
          width=10, command= translating
          ).place(relx=0.5, y = 240, anchor='center')


tk.Label(text = "Target Language :", font=('Times',12)).place(x=10, y = 280)
tl_button = tk.Button(text='Indonesia', font=('Times',11,'bold'), width=15, command=target_list)
tl_button.place(x=140, y = 277)

target_text = tk.Text(height=6, width=35)
target_text.place(relx=0.5,y=360,anchor='center')
#target_text.tag_configure("styled", font=("Helvetica", 10))


roots.mainloop()
