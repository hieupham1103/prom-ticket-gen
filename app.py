import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk, ImageFilter
import packages.generator as Gen
import packages.merge_file as Merge
import os
import shutil
import csv
import uuid

root = tk.Tk()
root.title("Ticket Auto Generator - ORZLab")
root.geometry("1000x800")
root.config(bg="white")

base_path = "./mattrc.png"
OUTPUT_PATH = "./output/"
image_zoom_size = 1

id_pos = (0,0)
id_x = tk.IntVar()
id_y = tk.IntVar()
id_size = tk.IntVar()
code_pos = (0,0)
code_x = tk.IntVar()
code_y = tk.IntVar()
code_size = tk.IntVar()

number_ticket = tk.IntVar()

merge_row = tk.IntVar()
merge_col = tk.IntVar()

left_frame = tk.Frame(root, width=200, height=600, bg="grey")
left_frame.pack(side="left", fill="y")

canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

def render(image):
    width, height = round(image.width * image_zoom_size), round(image.height * image_zoom_size)
    image = image.resize((width, height), Image.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def add_base_file():
    global base_path
    base_path = filedialog.askopenfilename(filetypes=(("png files","*.png"),("jpg files","*.jpg"),))
    image = Image.open(base_path)
    render(image)

def update_image_zoom_size(value):
    global image_zoom_size
    image_zoom_size = float(value) / 100
    image = Image.open(base_path)
    if id_size.get() * code_size.get() == 0:
        render(image)
        return
    apply()


def apply():
    global id_pos
    global code_pos
    id_pos = (id_x.get(), id_y.get())
    code_pos = (code_x.get(), code_y.get())
    image = Gen.make_qrcode(base_path = base_path,
                            id = 0,
                            code = "abcdefgh",
                            id_pos = id_pos,
                            id_size = id_size.get(),
                            code_pos = code_pos,
                            code_size = float(code_size.get()) / 10
                            )
    render(image)
    
def generate():
    if os.path.isdir(OUTPUT_PATH) == False:
        os.mkdir(OUTPUT_PATH)
    if type == 1:
        try:
            for root, dirs, files in os.walk(OUTPUT_PATH):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        except:
            pass
                
    store_id = {}
    
    with open('khach.csv', mode='w') as khach:
        khach_writer = csv.writer(khach, delimiter=',', lineterminator = '\n')
        for id in range(0, number_ticket.get()):
            code = str(uuid.uuid4())[0:8]
            while store_id.get(code):
                print("same id, gen again")
                code = str(uuid.uuid4())[0:7]
            image = Gen.make_qrcode(base_path = base_path,
                        id = id,
                        code = code,
                        id_pos = id_pos,
                        id_size = id_size.get(),
                        code_pos = code_pos,
                        code_size = float(code_size.get()) / 10
                        )
            image.save(f"{OUTPUT_PATH}/{id}.png")
            khach_writer.writerow([id, f"\"{code}\""])
            store_id[code] = True

def merge():
    Merge.init_merge(row = merge_row.get(), col = merge_col.get())

left_frame_tittle = tk.Label(left_frame,
                             text = "Ticket Auto Generator - ORZLab",
                             font = ('Helvetica bold', 10),
                             bg="grey"
                             )
left_frame_tittle.pack(pady = 10)

add_base_button = ttk.Button(left_frame,
                         text="Add Image",
                         command = add_base_file
                         )
add_base_button.pack(pady = 10)

image_zoom_size_slider= ttk.Scale(left_frame,
                            from_ = 1,
                            to = 200,
                            orient = tk.HORIZONTAL,
                            command = update_image_zoom_size
                            )
image_zoom_size_slider.pack(pady = 10)

id_frame = tk.Frame(left_frame)
id_frame.pack()
id_tittle = tk.Label(id_frame,
                             text = "Id",
                             font = ('Helvetica bold', 10),
                             bg="grey"
                             )
id_tittle.pack(pady = 10)
id_x_input = tk.Entry(id_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = id_x
                       )
id_x_input.pack()
id_y_input = tk.Entry(id_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = id_y
                       )
id_y_input.pack()
id_size_input = tk.Entry(id_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = id_size
                       )
id_size_input.pack()

code_frame = tk.Frame(left_frame)
code_frame.pack(pady = 10)
code_tittle = tk.Label(code_frame,
                             text = "Code",
                             font = ('Helvetica bold', 10),
                             bg="grey"
                             )
code_tittle.pack(pady = 10)
code_x_input = tk.Entry(code_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = code_x
                       )
code_x_input.pack()
code_y_input = tk.Entry(code_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = code_y
                       )
code_y_input.pack()
code_size_input = tk.Entry(code_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = code_size
                       )
code_size_input.pack()
apply_button = ttk.Button(left_frame,
                          text = "Apply",
                          command = apply
                          )
apply_button.pack(pady = 10)

number_ticket_tittle = tk.Label(left_frame,
                             text = "Number Ticket",
                             font = ('Helvetica bold', 10),
                             bg="grey"
                             )
number_ticket_tittle.pack(pady = 10)
number_ticket_input = tk.Entry(left_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = number_ticket
                       )
number_ticket_input.pack()
generate_button = ttk.Button(left_frame,
                          text = "Generate",
                          command = generate
                          )
generate_button.pack(pady = 10)

merge_frame = tk.Frame(left_frame)
merge_frame.pack()
merge_tittle = tk.Label(merge_frame,
                             text = "Merge file",
                             font = ('Helvetica bold', 10),
                             bg="grey"
                             )
merge_tittle.pack(pady = 10)
merge_row_input = tk.Entry(merge_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = merge_row
                       )
merge_row_input.pack()
merge_col_input = tk.Entry(merge_frame,
                       font = ('Helvetica bold', 10),
                       textvariable = merge_col
                       )
merge_col_input.pack()
generate_button = ttk.Button(merge_frame,
                          text = "Merge",
                          command = merge
                          )
generate_button.pack(pady = 10)


root.mainloop()