import os
import numpy as np
import cv2
import pandas as pd
import glob
import re

def getLocation(string):
    """
    This function is for pulling numbers from a string.
    """
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    string = string.replace(',',' ')
    string = string.replace(':',' ')
    location = []
    if re.search(p, string) is not None:
        for catch in re.finditer(p, string):
            location.append(int(catch[0]))
    return location
    

def listOfName(data):
    """
    This function pulls all image names in data. It takes each name once.
    """
    imageNames = data["image_name"]
    names = []
    for imageName in imageNames:
        if not (imageName in names):
            names.append(imageName)

    return names

def ComponentLocationsForImages(data,names,component):
    """
    In this function, data about the images containing the selected
    component is obtained.
    """
    components = data["component_type"]
    imageNames = data["image_name"]
    location = data["component_location"]
    
    finalLocation = []
    for name in names:
        arrayLoca = []
        counter = 0
        for imageName in imageNames:
            if name == imageName and component == components[counter]:
                loca = getLocation(location[counter])
                arrayLoca.append(loca)

            counter += 1
        finalLocation.append(arrayLoca)

    return finalLocation
        
def listOfImageAndInfo(data,component):
    """
    In this function, the images containing the selected component
    and the array containing the data are obtained.
    """
    names = listOfName(data)
    locations = ComponentLocationsForImages(data,names,component)
    numberOfComponents = []
    for location in locations:
        numberOfComponents.append(len(location))

    size = len(names)
    i = 0
    finalInfo = []
    while i < size:
        if numberOfComponents[i] != 0:
            info = [names[i],locations[i]]
            finalInfo.append(info)

        i += 1
    return finalInfo  

def createPath(folder, i, frontOrBack):
    """
    In this function, the path of the image is edited.
    """
    if '_1x_' in folder:
        x = 1
    elif '_1.5x_' in folder:
        x = 1.5
    elif '_2x_' in folder:
        x = 2
    if 'x_20' in folder:
        y = 20
    elif 'x_40' in folder:
        y = 40
    elif 'x_60' in folder:
        y = 60
    if 'p1_' in folder:
        p = 1
    elif 'p2_' in folder:
        p = 2
    elif 'p3_' in folder:
        p = 3
    elif 'p4_' in folder:
        p = 4
    elif 'p5_' in folder:
        p = 5
    
    pathImg = "D:/indir/s{}/Microscope/img/" + frontOrBack + "/{}x/s{}_p{}_{}x_{}_ring/TileScan_001/".format(i,x,i,p,x,y)

    return pathImg


i = 1
counter = 1
while i < 32:
    path = "D:/indir/s{}/Microscope/annotation".format(i)
    folders = os.listdir(path)
    if i == 11 or i == 14 or i == 15 or i == 26:
        i += 1
        continue
    if "front" in folders:
        pathCSV = "D:/indir/s{}/Microscope/annotation/front".format(i)
        folders2 = glob.glob(pathCSV + "/*.csv")

        for folder in folders2:
            
            pathImg = createPath(folder, i, "front")
            pcbcsv = pd.read_csv(folder)
            component = "resistors"
            infos = listOfImageAndInfo(pcbcsv,component)
            
            j, size = 0, len(infos)
            while j < size:
                pathImgcik = pathImg + infos[j][0]
                img = cv2.imread(pathImgcik)
                row, col, ch = img.shape
                cv2.imwrite("D:/data 4/images/{}.jpg".format(counter), img)
                f = open("D:/data 4/text/{}.txt".format(counter), "x")
                size2, k = len(infos[j][1]), 0
                while k < size2:
                    centerX = (infos[j][1][k][0] + infos[j][1][k][2]/2.0)/col
                    centerY = (infos[j][1][k][1] + infos[j][1][k][3]/2.0)/row
                    rateX = infos[j][1][k][2]/float(col)
                    rateY = infos[j][1][k][3]/float(row)
                    f.write("0 {} {} {} {}\n".format(centerX, centerY, rateX, rateY))
                    k += 1
                f.close()
                j += 1
            
                counter += 1

    if "back" in folders:
        pathCSV = "D:/indir/s{}/Microscope/annotation/back".format(i)
        folders2 = glob.glob(pathCSV + "/*.csv")

        for folder in folders2:
            pathImg = createPath(folder, i, "back")
            pcbcsv = pd.read_csv(folder)
            component = "resistors"
            infos = listOfImageAndInfo(pcbcsv,component)
            
            j, size = 0, len(infos)
            while j < size:
                pathImgcik = pathImg + infos[j][0]
                img = cv2.imread(pathImgcik)
                row, col, ch = img.shape
                cv2.imwrite("D:/data 4/images/{}.jpg".format(counter), img)
                f = open("D:/data 4/text/{}.txt".format(counter), "x")
                size2, k = len(infos[j][1]), 0
                while k < size2:
                    centerX = (infos[j][1][k][0] + infos[j][1][k][2]/2.0)/col
                    centerY = (infos[j][1][k][1] + infos[j][1][k][3]/2.0)/row
                    rateX = infos[j][1][k][2]/float(col)
                    rateY = infos[j][1][k][3]/float(row)
                    f.write("0 {} {} {} {}\n".format(centerX, centerY, rateX, rateY))
                    k += 1
                f.close()
                j += 1
            
                counter += 1
    i += 1
        
                
































