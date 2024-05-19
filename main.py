import os
import argparse
import shutil
from PIL import ImageOps, ImageDraw, ImageFont, Image
from barcode import Code128
from barcode.writer import ImageWriter 
import csv
import uuid

OUTPUT_PATH = "./output/"

def make_qrcode(id, code):
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
    code_img = code_img.resize((round(1.8 * width), round(1.8 * height)))
    
    
    path = OUTPUT_PATH + f"{id}.png"
    if os.path.isfile(path):
        print("File đã có")
        return
    
    img = Image.open("./template.png").convert("RGBA")
    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./font/RedditSans-VariableFont_wght.ttf",44)
    draw.text((1100,125),id,font = font, fill = (0,0,0,255))
    img.paste(code_img,(850,1680),code_img)
    img.save(path)
    # img.show()
    print(f"{id} done!!")

def check_dup(file_path = "khach.csv"):
    store_id = {}
    store_code = {}
    try:
        file = open(file_path, mode = 'r', encoding = "utf-8-sig")    
    except:
        print("DEO CO FILE, DM THANG NGU")
    
    data = csv.reader(file)
    for row in data:
        if len(row) > 1:
            if store_id.get(row[0]):
                print(f"TRUNG ID: {row[0]}")
            if store_code.get(row[1]):
                print(f"TRUNG CODE: {row[1]}")

            store_id[row[0]] = True
            store_code[row[1]] = True
            
    print("DONE")

def generate_guests(start_id, end_id, type = 0):
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
        for id in range(start_id, end_id + 1):
            code = str(uuid.uuid4())[0:8]
            while store_id.get(code):
                print("same id, gen again")
                code = str(uuid.uuid4())[0:7]
            make_qrcode(id, code)
            khach_writer.writerow([id, f"\"{code}\""])
            store_id[code] = True
    
    check_dup()



if __name__ == "__main__":
    # print("Số id bắt đầu:")
    # start_id = input()
    # while True:
    #     try:
    #         start_id = int(start_id)
    #         break
    #     except:
    #         print("Thử lại, số id bắt đầu:")
    #         start_id = input()
    # print("Số id kết thúc:")
    # end_id = input()
    # while True:
    #     try:
    #         end_id = int(end_id)
    #         break
    #     except:
    #         print("Thử lại, số id kết thúc:")
    #         end_id = input()
    # print("Bạn có muốn xóa sạch file đã cho có không (0: không; 1: có):")
    # type = input()
    # while True:
    #     try:
    #         type = int(type)
    #         break
    #     except:
    #         print("Thử lại, bạn có muốn xóa sạch file đã cho có không (0: không; 1: có):")
    #         type = input()
    
    # generate_guests(start_id, end_id, type)
    generate_guests(0, 650, 1)
    
