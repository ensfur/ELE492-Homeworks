import cv2
import numpy as np
import math

def averagePix(img):
    row, col = img.shape
    sumPix = 0
    
    for (x,y),px in np.ndenumerate(img):
        sumPix += px

    averagePix = int(sumPix/(row*col))
    img[:,:] = [averagePix]
    
    return img

def sampling(img,delta):
    row, col = img.shape
    divRow = int(row/delta)
    divCol = int(col/delta)

    i=j=0
    while j < divRow:
        while i < divCol:
            img[j*delta:j*delta+delta, i*delta:i*delta+delta] = averagePix(
                img[j*delta:j*delta+delta, i*delta:i*delta+delta])
            i+=1
        i=0
        j+=1

    i=j=0
    
    if (row - divRow*delta) != 0:
        remeaning = row - divRow*delta
        while i < divCol:
            img[row - remeaning:row, i*delta:i*delta+delta] = averagePix(
                img[row - remeaning:row, i*delta:i*delta+delta])
            i += 1  

    if (row - divRow*delta) != 0:
        remeaning = row - divRow*delta
        while j < divRow:
            img[j*delta:j*delta+delta , col - remeaning:col] = averagePix(
                img[j*delta:j*delta+delta , col - remeaning:col])
            j += 1

    if (row - divRow*delta) != 0 and (row - divRow*delta) != 0:
        img[row - remeaning:row , col - remeaning:col] = averagePix(
            img[row - remeaning:row , col - remeaning:col])
        
    return img

def upScale(img,scale):
    row,col = img.shape
    newImg = np.zeros((int(row*scale),int(col*scale)),np.uint8)

    for (x,y),px in np.ndenumerate(img):
        newImg[x*scale:x*scale+scale,y*scale:y*scale+scale] = img[x,y]

    return newImg

def downScale(img,scale):
    row,col = img.shape
    img = sampling(img,scale)
    newImg = np.zeros((int(row/scale),int(col/scale)),np.uint8)
    
    for (x,y),px in np.ndenumerate(newImg):
        newImg[x,y] = img[x*scale,y*scale]

    return newImg

def reScale(img,upOrDown,scale):
    if upOrDown == 'up':
        img = upScale(img,scale)
    elif upOrDown == 'down':
        img = downScale(img,scale)

    return img

def gammaTransform(img,gamma):
    c = 255.0/(255.0**gamma)
    img = img.astype(np.float64)
    for (x,y),px in np.ndenumerate(img):
        img[x,y] = (px**gamma)*c
    img = img.astype(np.uint8)    
    return img

def negativeImg(img):
    img[:,:] = [255] - img[:,:]
    return img

def logTransformation(img):
    c = 255 / math.log(1 + np.max(img))

    for (x,y),px in np.ndenumerate(img): 
        img[x,y] = int(c * math.log(1 + px))

    return img

def logTransformation2(img):
    minPx = np.min(img)
    img[:,:] -= minPx
    c = 255 / math.log(1 + np.max(img))    

    for (x,y),px in np.ndenumerate(img): 
        img[x,y] = int(c * math.log(1 + px))

    return img

def readImagesFromFile(path):
    images = []
    for image in os.listdir(path):
        img = cv2.imread(os.path.join(path,image))
        if img is not None:
            images.append(img)
    return images

def averageImages(images):
    numberOfImages = len(images)
    row,col,px = images[0].shape
    newImg = np.zeros((row,col,px),np.int64)

    for i in range(numberOfImages):
        newImg += images[i]
    newImg = newImg / numberOfImages
    newImg = newImg.astype(np.uint8)

    return newImg

img = cv2.imread("photo/4.png",0)
grayCopy = img.copy()
grayCopy2 = img.copy()
log = logTransformation(grayCopy)
log2 = logTransformation2(grayCopy2)

cv2.imwrite("photo/save/gray13.png",img)
cv2.imwrite("photo/save/log3.png",log)
cv2.imwrite("photo/save/log32.png",log2)







































