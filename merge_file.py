from PIL import ImageOps, ImageDraw, ImageFont, Image
import os
import shutil

OUTPUT_PATH = "./output_merge/"

def merge(files = [], id = 0):
    if len(files) == 0:
        return
    
    w, h = files[0].size
    
    
    final_img = Image.new(mode="RGBA", size=(w * 2, h * 2))
    x = 0
    y = 0
    for img in files:
        final_img.paste(img, (x,y), img)
        x += w
        if x >= w * 2:
            y += h
            x = 0
    
    final_img.save(OUTPUT_PATH + str(id) + ".png")
    print(f"{id} done!!")

def init_merge():
    if os.path.isdir(OUTPUT_PATH) == False:
        os.mkdir(OUTPUT_PATH)
    try:
        for root, dirs, files in os.walk(OUTPUT_PATH):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    except:
        pass
    lists = []
    count = 0
    for root, dirs, files in os.walk("./output/"):
        for f in files:
            lists.append(Image.open("./output/" + f).convert("RGBA"))
            
            if len(lists) == 4:
                merge(lists, count)
                lists.clear()
                count += 1
        merge(lists, count)
    
init_merge()