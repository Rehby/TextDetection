from PIL import Image,ImageDraw,ImageOps,ImageEnhance
import numpy as np

def func(pim,colors):
    im  = np.array(pim)
    Y, X = np.where(np.logical_and(im >= colors[0], im<=colors[1]))


    coords=[]
    for point in zip(X,Y):
  
        draw = ImageDraw.Draw(pim)
        draw.point((point[0],point[1]),fill='black') # Рисуем  точку
        if coords==[]:
            coords.append(point)
        elif coords[len(coords)-1][1]==point[1]:
            coords.append(point)
        elif len(coords)>800:
            return coords
            
        
        else:
            coords.clear()
            coords.append(point)

# Load image, ensure not palettised, and make into Numpy array
def cut(folder,folder1,file):
    pim = Image.open(f'inn/{folder}/{folder1}/{file}').convert('RGB')
    pim = ImageOps.grayscale(pim) 

    enhancer = ImageEnhance.Sharpness(pim) 
    factor = 1.3
    pim = enhancer.enhance(factor)
    enhancer = ImageEnhance.Brightness(pim) 
    
    colors=[150,160]
    coords1=func(pim,colors)
    if not coords1:
        return
    coords1x= coords1[0][0] if coords1[0][0]>200 and coords1[0][0]<400 else 250
    im_crop = pim.crop((coords1x,coords1[0][1], 1920,1080))
    colors=[240,255]
    coords=func(im_crop,colors)
    # print(coords1[0][1])
    print(f'inn/{folder}/{folder1}/{file}')
    print(coords1[0][0])
    
    if not coords:
        return
    # coords[len(coords)-1][0]  if coords[len(coords)-1][0]>1500 else 1500
    im_crop = pim.crop((coords[0][0]+coords1x,coords[0][1]+coords1[0][1], coords[len(coords)-1][0]  if coords[len(coords)-1][0]>1750 else 1750,1040))
    if not os.path.exists(f'rescutcolor/{folder}/{folder1}'):
        os.makedirs(f'rescutcolor/{folder}/{folder1}')
    im_crop.save(f'rescutcolor/{folder}/{folder1}/{file}', quality=1000)




    
    # im_crop.show()

import os
# files= os.listdir('data')
# print(files)
import fnmatch
import re
for folder in os.listdir('inn'):
    
        for folder1 in os.listdir(f'inn/{folder}/'):
        
            for file in fnmatch.filter(os.listdir(f'inn/{folder}/{folder1}'), '*.jpg'):
                cut(folder,folder1,file)
        
# for file in files:
#     
    