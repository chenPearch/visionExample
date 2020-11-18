import cv2
import numpy as np
import math
from networktables import NetworkTables
from opencvBasic import Sliders
from pathlib import Path

fov = 27.7665349671
tan_frame = math.tan(math.radians(fov))
tm = 0.325


def main():
    debug = True;
    # cap = cv2.VideoCapture('http://root:root@10.45.86.12/mjpg/video.mjpg') # use this line if you want to fetch video from the web.
    cap = cv2.VideoCapture(0)

    winName = "sliders"

    #the first thing that shoulden't bother you
    path = Path.joinpath(Path.cwd,"HSVdata.json")
    t = Sliders(winName = winName,isPi=False,path= path)

    while (True):
        _, img = cap.read()

        #this line adds a blur effect to the img (it helps with the HSV calibration)
        frame1 = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

        #this sesction down scales the img by 60%
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
        if(debug):
            t.writeHSVvals()
            upper, lower = t.getHSV()

        else:
            #sets the hsv values premnently
            lower = np.array([0,155,25])
            upper = np.array([134,255,255])

        mask = cv2.inRange(hsv, lower, upper)

        bit = cv2.bitwise_and(frame, frame, mask=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # filters the countures by area
        fillteredCont = []
        for con in contours:
            if (cv2.contourArea(con) > 900):
                fillteredCont.append(con)

        cv2.drawContours(frame, fillteredCont, -1, (0, 0, 255), 3)

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



        cv2.line(bit, (int(midFrame), 0), (int(midFrame), 1000), (0, 255, 0), 3)
        cv2.imshow("image", frame)
        cv2.imshow("bit",bit)

        k = cv2.waitKey(1)
        if (k == 27):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__": # this is how you write the main function in python.
    main()
