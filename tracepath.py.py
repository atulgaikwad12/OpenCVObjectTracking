#Press 'Esc' to Quit after clicking in any video window

#see blog for explanations : http://mypythonprojects.blogspot.com/

import cv2
import numpy as np
import pygame
import sys


pygame.init()

bindcolor=[255,0,0]#boundary highlight color [R,G,B]
point_1=(0,0)#first point
point_2=(0,0)#second point
center=(0,0)#center of the blob/object

window=pygame.display.set_mode((640,480))#open pygame window with given resolution

element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))#used for erode operation

blue_low=np.array([105,75,0],np.uint8)#lower limit HSV values for blue(using trial and error)
blue_hi=np.array([135,255,255],np.uint8)#upper limit HSV values

arlimit_l=500#lower area limit of valid blob
arlimit_h=10000#upper area limit of valid blob
asp_l=0.33#lower and upper limits for aspect ratio of valid blob
asp_h=2.33

cap=cv2.VideoCapture(0)

def preprocess(frame):	#to preprocess image
    imblur=cv2.medianBlur(frame,3)#use median blur with given parameters
    imhsv=cv2.cvtColor(imblur,cv2.COLOR_BGR2HSV)#convert color space to HSV from RGB
    thresholded=cv2.inRange(imhsv,blue_low,blue_hi)#threshold HSV frame based on color limits
    eroded=cv2.erode(thresholded,element)#erode to avoid peppers
    return eroded

def segment(frT):
    contours, hierarchy = cv2.findContours(frT.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#find contours
    for i,cnt in enumerate(contours):#iterate on possible blobs
        x,y,w,h=cv2.boundingRect(cnt)#rectangular boundary parameters
        cont_area=w*h#area of blob
        if cont_area>arlimit_l and cont_area<arlimit_h:#conditional nesting to select blob satisfying given constraints
            aspect=float(w)/float(h)
            if aspect>asp_l and aspect<asp_h:
                cv2.rectangle(frame,(x,y),(x+w,y+h),bindcolor,2)
                global center
                center=(x+(w/2),y+(h/2))#center of blob in pixel coordinates
                break#select first blob with satisfying constraints
    return frame,center


def draw_path(point_2):
    global point_1
    if point_2==None:#return if no blob is detected
        return
    pygame.draw.line(window,(0,255,0),point_1,point_2)#draw line between points 1 & 2 in given color(0,255,0)
    point_1=point_2#point_2 updated with point_1
    pygame.display.flip()#update pygame display window
    return


while(True):#read from camera repeatedly
    
    f,o_frame=cap.read()
    
    o_frame=cv2.resize(o_frame,(640,480))
    frame=cv2.flip(o_frame,1)#mirror in x direction(horizontal)**
    eroded=preprocess(frame)
    cv2.imshow('Eroded',eroded)
    frame,center=segment(eroded)
    cv2.imshow('Video',frame)
    draw_path(center)
    ch=cv2.waitKey(50)
    
    if ch==27:
        break

cap.release()

cv2.destroyAllWindows()
