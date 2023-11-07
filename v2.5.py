
import os
import cv2
import numpy as np
import fnmatch
import pprint



heightImg = 1080
widthImg = 1920


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        
        if area > 100:
         
            
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print(area,len(approx))

            if area > max_area:#and len(approx) == 6 :
                
               
                biggest = approx
                max_area = area
    return biggest,max_area

def read_files(folder,folder1,file):
    img = cv2.imread(f'cv_cut_innop/{folder}/{folder1}/{file}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    biggest, max_area = biggestContour(contours)
    cv2.drawContours(img, biggest, -1, (255,0,0), 25) # DRAW THE BIGGEST CONTOUR
    print('here')
    if not os.path.exists(f'cv_cut_innop/{folder}/{folder1}'):
        os.makedirs(f'cv_cut_innop/{folder}/{folder1}')
    
    cv2.imwrite(f'cv_cut_innop/{folder}/{folder1}/{file}', img) 
    pass

read_files('Ияк','фото асесмент 7','Screenshot-38.jpg')

























for folder in os.listdir('inn'):
    for folder1 in os.listdir(f'inn/{folder}/'):
        for file in fnmatch.filter(os.listdir(f'inn/{folder}/{folder1}'), '*.jpg'):
            read_files(folder,folder1,file)
            break
        break
    break