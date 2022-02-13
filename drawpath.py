#Press 'Esc' to Quit after clicking in any video window

#see blog for explanations : http://mypythonprojects.blogspot.com/

import cv2
import numpy as np
import pygame
import sys


pygame.init()

bindcolor=[255,0,0]#boundary highlight color [R,G,B]
pointg_1=(0,0)#first point
pointr_1=(0,0)
pointg_2=(0,0)#second point
pointr_2=(0,0)
center=(0,0)#center of the blob/object
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

window=pygame.display.set_mode((640,420))#open pygame window with given resolution

element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))#used for erode operation

green_low=np.array([33,80,40],np.uint8)#lower limit HSV values for Green(using trial and error)
green_hi=np.array([102,255,255],np.uint8)#upper limit HSV value

#lower_red = np.array([169, 100, 100],np.uint8)
#upper_red = np.array([189, 255, 255],np.uint8)
lower_red = np.array([110,50,50],np.uint8)#values are of blue 
upper_red = np.array([130,255,255],np.uint8)

#lower_blue = np.array([110,50,50],np.uint8)
#upper_blue = np.array([130,255,255],np.uint8)

arlimit_l=400#lower area limit of valid blob
arlimit_h=2000#upper area limit of valid blob
asp_l=0.33#lower and upper limits for aspect ratio of valid blob
asp_h=2.33

cap=cv2.VideoCapture(0)

def preprocess(frame):	#to preprocess image
    
    eroded=cv2.erode(frame,element)#erode to avoid peppers
    #return eroded
    maskOpen=cv2.morphologyEx(eroded,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    
    return maskClose

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


def draw_path(point_2,color):
    global pointg_1,pointr_1
    if point_2==None:#return if no blob is detected
       
        return
    if color=="red":
        pointg_2=point_2
        #pygame.draw.line(window,(0,255,0),pointg_1,pointg_2,4)#draw line between points 1 & 2 in given color(0,255,0)
        window.set_at(pointg_2,(0,255,0))
        lstg = list(pointg_2)
        lstg[1] = lstg[1]+1
        lstg[0] = lstg[0]+1
        tg = tuple(lstg)
        window.set_at(tg,(0,255,0))
        lstg[1] = lstg[1]-2
        lstg[0] = lstg[0]-2
        tg = tuple(lstg)
        window.set_at(tg,(0,255,0))
        pointg_1=pointg_2#point_2 updated with point_1
    if color=="green":
        pointr_2=point_2
        #pygame.draw.line(window,(255,0,0),pointr_1,pointr_2,4)
        window.set_at(pointr_2,(0,0,255))
        lstr = list(pointr_2)
        lstr[1] = lstr[1]+1
        lstr[0] = lstr[0]+1
        tr = tuple(lstr)
        window.set_at(tr,(0,0,255))
        lstr[1] = lstr[1]-2
        lstr[0] = lstr[0]-2
        tr = tuple(lstr)
        window.set_at(tr,(0,0,255))
        pointr_1=pointr_2                 
   
    pygame.display.flip()#update pygame display window
    return


while(True):#read from camera repeatedly
    
    f,o_frame=cap.read()
    
    o_frame=cv2.resize(o_frame,(340,220))
    frame=cv2.flip(o_frame,1)#mirror in x direction(horizontal)**
    imblur=cv2.medianBlur(frame,3)#use median blur with given parameters
    imhsv=cv2.cvtColor(imblur,cv2.COLOR_BGR2HSV)#convert color space to HSV from RGB
    thresholdedgreen=cv2.inRange(imhsv,green_low,green_hi)#threshold HSV frame based on color limits
    thresholdedred=cv2.inRange(imhsv,lower_red,upper_red)
    erodedgreen=preprocess(thresholdedgreen)
    erodedred=preprocess(thresholdedred)
    cv2.imshow('ErodedGreen',erodedgreen)
    cv2.imshow('ErodedRed',erodedred)
    frameg,center1=segment(erodedgreen)
    framer,center2=segment(erodedred)
    cv2.imshow('Video Green',frameg)
    cv2.imshow('Video Red',framer)
    draw_path(center1,"green")
    draw_path(center2,"red")
    ch=cv2.waitKey(50)
    
    if ch==27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.display.quit()
pygame.quit()
sys.exit()
