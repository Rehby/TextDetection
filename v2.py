
import os
import cv2
import numpy as np
import fnmatch
import pprint


########################################################################

heightImg = 1080
widthImg = 1920

########################################################################

def preProcess(img):
    img=img[0:1060,0:1920]
    # img = cv2.line(img,(0,1040),(1920,1040),(245,246,248),20)
    # img = cv2.line(img,(0,1040),(1920,1040),(255,255,255),10)
    brown_lo=np.array([140,140,140])
    brown_hi=np.array([199,199,210])
    mask=cv2.inRange(img,brown_lo,brown_hi)

#  Change image to red where we found brown
    img[mask>0]=(245,246,248)
    # cv2.imshow('image window', img)
    # # # add wait key. window waits until user presses a key
    # cv2.waitKey(0)
    # # # and finally destroy/close all open windows
    # cv2.destroyAllWindows()
   
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    # imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    # kernel = np.ones((1,1),np.uint8)
    # dilated_img = cv2.dilate(imgGray, kernel, iterations = 2)

    imgThreshold = cv2.adaptiveThreshold(imgGray, 255, 1, 1, 27, 2)
    
    # imgThreshold = cv2.adaptiveThreshold(imgGray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #         cv2.THRESH_BINARY_I,11,3)  # APPLY ADAPTIVE THRESHOLD
    return imgThreshold

########################################################################

def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        
        if area > 100000:
         
            
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            print(area,len(approx))

            if area > max_area and len(approx) == 4 :
                
               
                biggest = approx
                max_area = area
    return biggest,max_area

########################################################################

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

########################################################################

#### 1. PREPARE THE IMAGE
def find(folder,folder1,file):
    img = cv2.imread(f'inn/{folder}/{folder1}/{file}')
    # img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgThreshold = preProcess(img)

    # #### 2. FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    # imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(contours)
    # cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 30) # DRAW ALL DETECTED CONTOURS
  
    #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
    biggest, max_area = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    # if not os.path.exists(f'cv_cut_innop/{folder}/{folder1}'):
    #         os.makedirs(f'cv_cut_innop/{folder}/{folder1}')
        
    # cv2.imwrite(f'cv_cut_innop/{folder}/{folder1}/{file}', imgThreshold) 

    if biggest.size != 0:

        biggest = reorder(biggest)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(biggest)
        cv2.drawContours(imgThreshold, biggest, -1, (255,0,0), 25) # DRAW THE BIGGEST CONTOUR
        if not os.path.exists(f'cv_cut_innop/{folder}/{folder1}'):
            os.makedirs(f'cv_cut_innop/{folder}/{folder1}')
        
        cv2.imwrite(f'cv_cut_innop/{folder}/{folder1}/{file}', imgThreshold) 
        # if not os.path.exists(f'cv_cut_innop/{folder}/{folder1}'):
        #     os.makedirs(f'cv_cut_innop/{folder}/{folder1}')
    
        # cv2.imwrite(f'cv_cut_innop/{folder}/{folder1}/{file}', imgThreshold) 
        # cv2.imshow('image window', imgThreshold)
        # # add wait key. window waits until user presses a key
        # cv2.waitKey(0)
        # # and finally destroy/close all open windows
        # cv2.destroyAllWindows()
        # imgThreshold=imgThreshold[biggest[0]:biggest[3],biggest[1]:biggest[2]]
        # cv2.imshow('Stacked Images', imgThreshold)
        # cv2.imshow('image window', imgThreshold)
        # # add wait key. window waits until user presses a key
        # cv2.waitKey(0)
        # # and finally destroy/close all open windows
        # cv2.destroyAllWindows()
       
        
    

for folder in os.listdir('inn'):
    for folder1 in os.listdir(f'inn/{folder}/'):
        for file in fnmatch.filter(os.listdir(f'inn/{folder}/{folder1}'), '*.jpg'):
            find(folder,folder1,file)
        #     break    
        # break
        
    # break