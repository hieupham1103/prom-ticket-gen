import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk, ImageDraw, ImageFont
from barcode import Code128
from barcode.writer import ImageWriter 
import os
import shutil
import csv
import uuid

class Generator():
    def __init__(self):
        self.OUTPUT_PATH = "./output/"
    def make_ticket(self, base_path, id, code, id_pos = (0,0), id_size = 10, code_pos = (0,0), code_size = 1):
        id = "{:08d}".format(id)
        print(f"==Generate {id} - {code}==")
        code_img = Code128(code, writer=ImageWriter()).render()
        
        if code_img.mode != "RGBA":
            code_img = code_img.convert("RGBA")

        width, height = code_img.size
        code_img = code_img.crop((0,100, width, height))
        expand_value = 10
        code_img = ImageOps.expand(code_img, border = expand_value, fill = "white") 
        width, height = code_img.size
        code_img = code_img.crop((25, 0, width - 20, height - 40))
        width, height = code_img.size
        code_img = code_img.resize((round(code_size * width), round(code_size * height)))
        
        
        img = Image.open(base_path).convert("RGBA")
        
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./font/RedditSans-VariableFont_wght.ttf",id_size)
        draw.text((id_pos[0],id_pos[1]),id,font = font, fill = (0,0,0,255))
        img.paste(code_img,(code_pos[0],code_pos[1]),code_img)

        return img

    def generate_guests(self, number, base_path, id_pos, id_size, code_pos, code_size):
        if os.path.isdir(self.OUTPUT_PATH) == False:
            os.mkdir(self.OUTPUT_PATH)
        if type == 1:
            try:
                for root, dirs, files in os.walk(self.OUTPUT_PATH):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            except:
                pass
                    
        store_id = {}
        
        with open('khach.csv', mode='w') as khach:
            khach_writer = csv.writer(khach, delimiter=',', lineterminator = '\n')
            for id in range(0, number):
                code = str(uuid.uuid4())[0:8]
                while store_id.get(code):
                    print("same id, gen again")
                    code = str(uuid.uuid4())[0:7]
                image = self.make_ticket(base_path = base_path,
                            id = id,
                            code = code,
                            id_pos = id_pos,
                            id_size = id_size,
                            code_pos = code_pos,
                            code_size = float(code_size) / 10
                            )
                image.save(self.OUTPUT_PATH + str(id) + ".png")
                khach_writer.writerow([id, f"\"{code}\""])
                store_id[code] = True

class Merge():
    def __init__(self):
        super().__init__()
        self.OUTPUT_PATH = "./output_merge/"
        
    
    def merge(self, files = [], id = 0, row = 2, col = 4):
        if len(files) == 0:
            return
        
        w, h = files[0].size
        
        
        final_img = Image.new(mode="RGBA", size=(w * col, h * row))
        
        x = 0
        y = 0
        for img in files:
            final_img.paste(img, (x,y), img)
            x += w
            if x >= w * col:
                y += h
                x = 0
        
        final_img.save(self.OUTPUT_PATH + str(id) + ".png")
        print(f"{id} done!!")

        
    def execute(self, images_path = "./output/", col = 1, row = 1):
        if os.path.isdir(self.OUTPUT_PATH) == False:
            os.mkdir(self.OUTPUT_PATH)
        try:
            for root, dirs, files in os.walk(self.OUTPUT_PATH):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        except:
            pass
        lists = []
        count = 0
        for root, dirs, files in os.walk(images_path):
            for f in files:
                lists.append(Image.open(images_path + f).convert("RGBA"))
                
                if len(lists) == row * col:
                    self.merge(lists, count, row, col)
                    lists.clear()
                    count += 1
            self.merge(lists, count, row, col)
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ticket Auto Generator - ORZLab")
        self.geometry("1000x800")
        self.config(bg="white")
        
        self.left_menu = LeftMenu(self)
        self.BASE_PATH = self.left_menu.base_file.BASE_PATH
        self.BASE_PATH.trace_add("write", self.base_path_trace)
        
        self.canvas = Canvas(self)
        self.left_menu.set_canvas(self.canvas)
        self.id = self.left_menu.id_editor
        self.code = self.left_menu.code_editor
        
        self.Gen = Generator()
        
        self.mainloop()
        
    def base_path_trace(self, var, index, mode):
        self.canvas.render()

class Canvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=750, height=600)
        self.pack()
        self.image_zoom_size = 1

    def render(self):
        try:
            image = Image.open(self.master.BASE_PATH.get())
        except:
            return
        
        id = self.master.id
        code = self.master.code
        
        if id.size.value.get() * code.size.value.get() != 0:
            image = self.master.Gen.make_ticket(base_path = self.master.BASE_PATH.get(),
                            id = 0,
                            code = "abcdefgh",
                            id_pos = (id.x.value.get(), id.y.value.get()),
                            id_size = id.size.value.get(),
                            code_pos = (code.x.value.get(), code.y.value.get()),
                            code_size = float(code.size.value.get()) / 10
                            )
        
        width, height = round(image.width * self.image_zoom_size), round(image.height * self.image_zoom_size)
        image = image.resize((width, height), Image.LANCZOS)
        self.config(width=image.width, height=image.height)
        image = ImageTk.PhotoImage(image)
        self.image = image
        self.create_image(0, 0, image=image, anchor="nw")

    def update_zoom(self, zoom_value):
        self.image_zoom_size = float(zoom_value) / 100
        self.render()

class LeftMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=600, bg="grey")
        self.pack(side="left", fill='y')
        tk.Label(self,
                 text="Ticket Auto Generator - ORZLab",
                 font=('Helvetica bold', 10),
                 bg="grey"
                 ).pack(pady = 10)
        
        
        self.canvas = None
        
        self.base_file = File(self, "Template image")
        self.BASE_PATH = self.base_file.BASE_PATH
        self.image_zoom = Scale(self)
        
        self.id_editor = ElementEditor(self, "ID")
        self.code_editor = ElementEditor(self, "Code")
        
        ttk.Button(self,
                   text = "Apply change",
                   command = self.apply
                   ).pack()

        self.generate_ticket = Generate_ticket(self)
        self.merge_ticket = Merge_ticket(self)
    
    def set_canvas(self, canvas):
        self.canvas = canvas
        self.image_zoom.set_canvas(canvas)
    
    def apply(self):
        self.canvas.render()
        
class Generate_ticket(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(pady = 10)
        
        self.id = self.master.id_editor
        self.code = self.master.code_editor
        
        self.number = InputEntry(self, "number of ticket")
        ttk.Button(self,
                   text = "Generate",
                   command = self.generate
                   ).pack(pady = 10)

    def generate(self):
        id = self.id
        code = self.code
        if id.size.value.get() * code.size.value.get() != 0:
            self.master.master.Gen.generate_guests(
                number = self.number.value.get(),
                base_path = self.master.BASE_PATH.get(),
                id_pos = (id.x.value.get(), id.y.value.get()),
                id_size = id.size.value.get(),
                code_pos = (code.x.value.get(), code.y.value.get()),
                code_size = code.size.value.get()
                )

class Merge_ticket(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(pady = 10)
        self.Merge = Merge()
        self.col = InputEntry(self, "Col")
        self.row = InputEntry(self, "Row")
        
        ttk.Button(self,
                   text = "Merge ticket",
                   command = self.merge
                   ).pack(pady = 10)
    
    def merge(self):
        self.Merge.execute(col = self.col.value.get(), row = self.row.value.get())
        
class Scale(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        ttk.Label(self,
                  text = "zoom"
                  ).pack(side = "left", expand = True)
        ttk.Scale(self,
                  from_=1,
                  to=200,
                  orient=tk.HORIZONTAL,
                  command=self.update_value
                  ).pack(side = "left", expand = True)
        self.value = 0
        self.canvas = None
        
    def update_value(self, value):
        self.value = value
        if self.canvas:
            self.canvas.update_zoom(value)

    def set_canvas(self, canvas):
        self.canvas = canvas

class File(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.pack()
        ttk.Button(self,
                   text=title,
                   command=self.add_base_file
                   ).pack()
        self.BASE_PATH = tk.StringVar()
        
        ttk.Label(self,
                  textvariable=self.BASE_PATH
                  ).pack()
        
    def add_base_file(self):
        self.BASE_PATH.set(filedialog.askopenfilename(filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"))))

class ElementEditor(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.pack(pady=10)
        tk.Label(self,
                 text=title,
                 font=('Helvetica bold', 10)
                 ).pack(expand=True, pady=10)
        self.x = InputEntry(self, "x")
        self.y = InputEntry(self, "y")
        self.size = InputEntry(self, "size")
        
class InputEntry(tk.Frame):
    def __init__(self, parent, label):
        super().__init__(parent)
        self.pack()
        self.value = tk.IntVar()
        ttk.Label(self,
                  text=label,
                  ).pack(side='left', expand=True)
        ttk.Entry(self,
                  font=('Helvetica bold', 10),
                  textvariable=self.value
                  ).pack(side='left', expand=True)

if __name__ == '__main__':
    App()
