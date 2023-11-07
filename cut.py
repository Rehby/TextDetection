from PIL import Image,ImageOps,ImageEnhance
import os
import fnmatch
import re
for folder in os.listdir('inn'):
    for folder1 in os.listdir(f'inn/{folder}/'):
        for file in fnmatch.filter(os.listdir(f'inn/{folder}/{folder1}'), '*.jpg'):
            
            im = Image.open(f'inn/{folder}/{folder1}/{file}')

            im_crop = im.crop((250, 220, 1800, 1000))
            im_crop = ImageOps.grayscale(im_crop) 
            enhancer = ImageEnhance.Contrast(im_crop) 
            factor = 1.5
            im_crop = enhancer.enhance(factor)
            enhancer = ImageEnhance.Sharpness(im_crop) 
            factor = 1.3
            im_crop = enhancer.enhance(factor)
            enhancer = ImageEnhance.Brightness(im) 

            factor = 0.5 #gives original image 
            im_output = enhancer.enhance(factor)
            if not os.path.exists(f'rescut_innop/{folder}/{folder1}'):
                os.makedirs(f'rescut_innop/{folder}/{folder1}')
            im_crop.save(f'rescut_innop/{folder}/{folder1}/{file}', quality=1000)