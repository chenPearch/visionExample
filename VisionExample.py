import cv2
import numpy as np
import math
from networktables import NetworkTables
from opencvBasic import helperClass

fov = 27.7665349671
tan_frame = math.tan(math.radians(fov))
tm = 0.325
def nothing(x):
    pass


def main():
    debug = True
    # cap = cv2.VideoCapture('http://root:root@10.45.86.12/mjpg/video.mjpg') #Axis cam IP
    cap = cv2.VideoCapture(1) #using an external USB camera

    winName = "slider" #string for windows names

    #the first thing that shoulden't bother you #wtf is the first thing
    path = "HSVdata.txt"
    t = helperClass(winName,False,path)

    # creates the sliders for the HSV vaules
    slidersWin = np.zeros((1, 400, 3), np.uint8)
    cv2.namedWindow(winName)
    cv2.createTrackbar('h min', winName, 0, 255, nothing)
    cv2.createTrackbar('s min', winName, 0, 255, nothing)
    cv2.createTrackbar('v min', winName, 0, 255, nothing)
    cv2.createTrackbar('H max', winName, 255, 255, nothing)
    cv2.createTrackbar('S max', winName, 255, 255, nothing)
    cv2.createTrackbar('V max', winName, 255, 255, nothing)

    #the second thing that shouldn't bother you #wtf is the second thing
    # t.createTrackBars(winName)

    #the Actual loop. condition is True to always run
    while (True):
        _, img = cap.read() #sets img to what the camera sees every time the loop runs

        #this line adds a blur effect to the img (it helps with the HSV calibration)
        frame1 = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT) #not absolutely necessary

        #this sesction down scales the img by 60%, not absolutely necessary
        scale_percent = 60  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame1, dim, interpolation = cv2.INTER_AREA)

        #gets the width of the frame and the middle of the frame
        _, ABpx, _ = frame.shape
        midFrame = ABpx/2

        #coverts the photo from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

        #the thrid thing that really shouldent bouther you
        # if(debug):
        #     t.writeHSVvals(winName)
        # upper, lower = t.getHSV(winName)

        #this if statment is for separating debug mode from regular mode
        if(debug):
            #gets the lower and upper HSV  values from the track bars created above
            lower = np.array([cv2.getTrackbarPos('h min',winName),
            cv2.getTrackbarPos('s min',winName),
            cv2.getTrackbarPos('v min',winName)])
            upper = np.array([cv2.getTrackbarPos("H max", winName),
            cv2.getTrackbarPos("S max", winName),
            cv2.getTrackbarPos("V max", winName)])
        else:
            #sets the hsv values premnently
            lower = np.array([0,155,25])
            upper = np.array([134,255,255])

        mask = cv2.inRange(hsv, lower, upper)

        bit = cv2.bitwise_and(frame, frame, mask=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        fillteredCont = [] #a new list to store the filtered contours.
        #filtering the contours
        for con in contours:
            if (cv2.contourArea(con) > 900):
                fillteredCont.append(con)

        # cv2.drawContours(frame, fillteredCont, -1, (0, 0, 255), 3)
       
    
        for cnt in fillteredCont:
            #sorrunds the counturs with a bounding rect and returns the hight width and x,y values of one of the points
            x, y,w,h = cv2.boundingRect(cnt)
            #draws a rectangle on screen
            cv2.rectangle(bit, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cntMid = x + w/2
            cv2.line(bit,(int(cntMid),0),(int(cntMid),1000),(0,0,255),3)

            #cal the things
            tan_alfa = (cntMid - midFrame) * tan_frame / midFrame
            alfa = math.degrees(math.atan(tan_alfa))
            d = (0.325 * midFrame) / (2*w * tan_frame)
            Dfinal = d/math.cos(tan_alfa)
            print("alfa: " + str(alfa))
            # print("d   : " + str(d))
            # print("Dfinal: " + str(Dfinal))



        cv2.line(bit, (int(midFrame), 0), (int(midFrame), 1000), (0, 255, 0), 3)
        cv2.imshow("image", frame)
        cv2.imshow("bit",bit)

        k = cv2.waitKey(1)
        if (k == 27):
            break
    cv2.destroyAllWindows()
main()
