import os
import shutil
from PIL import ImageOps, ImageDraw, ImageFont
from barcode import Code128
from barcode.writer import ImageWriter 
import csv
import uuid

OUTPUT_PATH = "./output/"

def make_qrcode(id, code):
    id = "{:08d}".format(id)
    print(f"==Generate {id} - {code}==")
    code_img = Code128(code, writer=ImageWriter()).render()
    
    # Add id number
    expand_value = 30
    img = ImageOps.expand(code_img, border = expand_value, fill = "white") 
    width, height = img.size
    img = img.crop((expand_value, expand_value, width - expand_value, height))
    width, height = img.size
    
    
    if img.mode != "RGB":
        img = img.convert("RGB")

    
    font = ImageFont.truetype("./font/RedditSans-VariableFont_wght.ttf",50)

    draw = ImageDraw.Draw(img)
    w = draw.textlength(id, font = font)
    draw.text(
        ((width-w)/2, height - 65),
        id,
        fill=(0, 0, 0),
        font = font
    )
    path = OUTPUT_PATH + f"{id}.png"
    if os.path.isfile(path):
        print("File đã có")
        return
        
    img.save(path)
    print(f"{id} done!!")


def generate_guests(number, type = 0):
    if type == 1:
        for root, dirs, files in os.walk(OUTPUT_PATH):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
                
    store_id = {}
    
    with open('khach.csv', mode='w') as khach:
        khach_writer = csv.writer(khach, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for id in range(number):
            code = str(uuid.uuid4())[0:7]
            while store_id.get(code):
                print("same id, gen again")
                code = str(uuid.uuid4())[0:7]
            make_qrcode(id, code)
            khach_writer.writerow([id, f"\"{code}\""])
            store_id[code] = True

generate_guests(600, 1)
