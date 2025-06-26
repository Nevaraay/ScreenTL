import tkinter as tk
from PIL import ImageGrab

class ScreenCaptureTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Make window semi-transparent
        self.root.configure(bg='black')
        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('<B1-Motion>', self.on_drag)
        self.root.bind('<ButtonRelease-1>', self.on_release)

        self.canvas = tk.Canvas(self.root, cursor="cross", bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def on_click(self, event):
        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()
        self.rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.canvas.canvasx(self.start_x - self.root.winfo_rootx()),
                                     self.canvas.canvasy(self.start_y - self.root.winfo_rooty()),
                                     event.x, event.y)

    def on_release(self, event):
        end_x = self.root.winfo_pointerx()
        end_y = self.root.winfo_pointery()

        self.root.withdraw()  # Hide the tkinter window so it’s not in the screenshot
        self.root.after(100, lambda: self.take_screenshot(self.start_x, self.start_y, end_x, end_y))

    def take_screenshot(self, x1, y1, x2, y2):
        bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        img = ImageGrab.grab(bbox=bbox)
        img.save("SSArea.png")
        self.root.quit()
