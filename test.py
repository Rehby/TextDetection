from PIL import Image,ImageDraw,ImageOps,ImageEnhance
import numpy as np
import os

def test(file):
    pim = Image.open(f'test/data/{file}').convert('RGB')
    pim = ImageOps.grayscale(pim) 
    # enhancer = ImageEnhance.Contrast(pim) 
    # factor = 1.5
    # im_crpimp = enhancer.enhance(factor)
    enhancer = ImageEnhance.Sharpness(pim) 
    factor = 1.3
    pim = enhancer.enhance(factor)
    enhancer = ImageEnhance.Brightness(pim) 
    pim.save(f'test/res/{file}')

files=os.listdir('test/data')
for file in files:
    test(file)