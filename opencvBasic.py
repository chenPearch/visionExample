import cv2
import numpy as np
import math
import json
class helperClass:
    
    
    def __init__(self,winName,isPi,path):
        self.winName = winName
        self.isPi = isPi
        self.path = path
        self.vals = json.load(open(self.path))
    def nothing(self,x):
        pass
    #gets distance between 2 points
    def distance(self,x1,y1,x2,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)
    #returns the HSV values
    def writeHSVvals(self,winName):
        #json thingy
        data = { 
            "H min": cv2.getTrackbarPos("h min", winName),
            "H max": cv2.getTrackbarPos("H max", winName),
            "S min": cv2.getTrackbarPos("s min", winName),
            "S max": cv2.getTrackbarPos("S max", winName),
            "V min": cv2.getTrackbarPos("v min", winName),
            "V max": cv2.getTrackbarPos("V max", winName),
        }
        #puts the json thingy in to a txt file
        with open("HSVdata.txt","w") as outFile:
            json.dump(data,outFile)
    def getHSV(self,winName):
        self.vals = json.load(open(self.path))
        Upper = np.array([
            self.vals["H max"],self.vals["S max"],self.vals["V max"]
            ])

        Lower = np.array([
            self.vals["H min"],self.vals["S min"],self.vals["V min"]
        ])
        return Upper,Lower
    #creates the trackbars
    def createTrackBars(self,winName):
        # Create a black image, a window
        img = np.zeros((1 ,1, 3), np.uint8)
        cv2.namedWindow(winName)
        

        # create trackbars for color change
        cv2.createTrackbar('h min', winName, self.vals["H min"], 255, self.nothing)
        cv2.createTrackbar('s min', winName, self.vals["S min"], 255, self.nothing)
        cv2.createTrackbar('v min', winName, self.vals["V min"], 255, self.nothing)
        cv2.createTrackbar('H max', winName, self.vals["H max"], 255, self.nothing)
        cv2.createTrackbar('S max', winName, self.vals["S max"], 255, self.nothing)
        cv2.createTrackbar('V max', winName, self.vals["V max"], 255, self.nothing)
        #return img
    #creates a masked img,hsv and a bit wise img 
    def createMask(self,Img,lower,upper):
        #creates hsv Img
        hsvImg = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV_FULL)
        #gets lower array values
        mask = cv2.inRange(hsvImg,lower,upper)
        bitImg = cv2.bitwise_and(Img,Img, mask=mask)
        return bitImg,mask,hsvImg
    
    #sorts the contuors from the left of the image to the right
    def sort_contours(self,cnts):
        # initialize the reverse flag and sort index
        reverse = True
        i = 0
        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b: b[1][i], reverse=reverse))
        # return the list of sorted contours and bounding boxes
        return cnts
    