import tkinter as tk
from PIL import ImageTk,Image
from agent import Agent
import json, random

chroma_key = '#FF00FF'
scale = 128

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.agent = Agent('links')
        self.animation_frame = 0
        self.animation = self.agent.get_animation('Print')
        self.master = master
        self.create_widgets()
        self.master.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(root, background=chroma_key, width = scale, height = scale, highlightthickness=0)  
        self.canvas.pack()  
        self.img = ImageTk.PhotoImage(self.agent.get_frame(0, 0))  
        self.image_on_canvas = self.canvas.create_image(scale / 2, (scale / 2) - 1, anchor=tk.CENTER, image=self.img)
        self.canvas.bind("<Button-1>", self.click)

    def set_image(self, newimg):
        self.canvas.itemconfig(self.image_on_canvas, image = newimg)
        self.img = newimg

    def animate(self, event=None):
        try:
            frame = self.animation['frames'][self.animation_frame]
        except IndexError:
            newimg = ImageTk.PhotoImage(self.agent.get_frame(0, 0))
            self.set_image(newimg)
            self.animation_frame = 0
            return

        image_x = frame['images'][0][0]
        image_y = frame['images'][0][1]

        newimg = ImageTk.PhotoImage(self.agent.get_frame(image_x, image_y))
        self.set_image(newimg)

        if 'branching' in frame:
            for branch in frame['branching']['branches']:
                prob = branch['weight']
                rand = random.randrange(0,100)
                if prob > rand:
                    self.animation_frame = branch['frameIndex']
                    break
            self.animation_frame = self.animation_frame + 1
        else:
            self.animation_frame = self.animation_frame + 1

        self.master.after(frame['duration'], self.animate)

    def click(self, event):
        self.animate()

root = tk.Tk()

#root.overrideredirect(True)
root.attributes("-toolwindow", True)

root.configure(bg=chroma_key)
root.geometry("-100-100")
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", chroma_key)

app = Application(master=root)
root.mainloop()
