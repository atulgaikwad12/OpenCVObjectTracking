#Press 'Esc' to Quit after clicking in any video window

#see blog for explanations : http://mypythonprojects.blogspot.com/

import cv2
import numpy as np
import pygame
import sys


pygame.init()

bindcolor=(255,255,0)#boundary highlight color [R,G,B]
pointg_1=(0,0)#first point
pointr_1=(0,0)
pointg_2=(0,0)#second point
pointr_2=(0,0)
center=(0,0)#center of the blob/object
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
g_list = []
r_list = []

window=pygame.display.set_mode((640,420), pygame.RESIZABLE)
pygame.display.set_caption("Drawing Window")
#open pygame window with given resolution with resizable ability
pygame.mouse.set_cursor(*pygame.cursors.diamond)
window.fill((255,255,255))
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))#used for erode operation

green_low=np.array([33,80,40],np.uint8)#lower limit HSV values for Green(using trial and error)
green_hi=np.array([102,255,255],np.uint8)#upper limit HSV value

#lower_red = np.array([169, 100, 100],np.uint8)
#upper_red = np.array([189, 255, 255],np.uint8)
lower_blue = np.array([110,50,50],np.uint8)#values are of blue 
upper_blue = np.array([130,255,255],np.uint8)



arlimit_l=400#lower area limit of valid blob
arlimit_h=2000#upper area limit of valid blob
asp_l=0.33#lower and upper limits for aspect ratio of valid blob
asp_h=2.33

cap=cv2.VideoCapture(0)
cv2.namedWindow('TrackingScreen',cv2.WINDOW_NORMAL)
cv2.namedWindow('ErodedGreen',cv2.WINDOW_NORMAL)
cv2.namedWindow('ErodedBlue',cv2.WINDOW_NORMAL)
cv2.resizeWindow('TrackingScreen',320,240)
cv2.resizeWindow('ErodedGreen',320,240)
cv2.resizeWindow('ErodedBlue',320,240)

def preprocess(frame):	#to preprocess image
    
    eroded=cv2.erode(frame,element)#erode to avoid peppers
    #return eroded
    maskOpen=cv2.morphologyEx(eroded,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    
    return maskClose

def segment(frT):
    contours, hierarchy = cv2.findContours(frT.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#find contours
    center=None
    for i,cnt in enumerate(contours):#iterate on possible blobs
        x,y,w,h=cv2.boundingRect(cnt)#rectangular boundary parameters
        cont_area=w*h#area of blob
        
        if cont_area>arlimit_l and cont_area<arlimit_h:#conditional nesting to select blob satisfying given constraints
            aspect=float(w)/float(h)
            if aspect>asp_l and aspect<asp_h:
                cv2.rectangle(frame,(x,y),(x+w,y+h),bindcolor,2)
                #global center
                center=(x+(w/2),y+(h/2))#center of blob in pixel coordinates
                break#select first blob with satisfying constraints
            else:
                center=None
                return frame,center
        else:
            center=None
            return frame,center    
    return frame,center


def draw_path(point_2,color):
  #global pointg_1,pointr_1
  if point_2==None or color == "nill":#return if no blob is detected
     return
  else:
     if color == "green":
        pointg_2=point_2
        #pygame.draw.line(window,(0,255,0),pointg_1,pointg_2,4)#draw line between points 1 & 2 in given color(0,255,0)
        pygame.draw.circle(window,(0,255,0),pointg_2,3)
     if color == "blue":
        pointr_2=point_2
        lstr = list(pointr_2)
        pygame.draw.rect(window,(255,255,255), (lstr[0]-10,lstr[1]-10,20,20))
        #pointr_1=pointr_2                 
   
     #pygame.display.flip()#update pygame display window
     pygame.display.update()
     return


while(True):#read from camera repeatedly
    
    f,o_frame=cap.read()   
    o_frame=cv2.resize(o_frame,(320,240))
    color = "nill"
    centerr=None
    centerg=None
    frame=cv2.flip(o_frame,1)#mirror in x direction(horizontal)**
    imblur=cv2.medianBlur(frame,3)#use median blur with given parameters
    imhsv=cv2.cvtColor(imblur,cv2.COLOR_BGR2HSV)#convert color space to HSV from RGB
    thresholdedgreen=cv2.inRange(imhsv,green_low,green_hi)#threshold HSV frame based on color limits
    thresholdedblue=cv2.inRange(imhsv,lower_blue,upper_blue)
    erodedgreen=preprocess(thresholdedgreen)
    erodedblue=preprocess(thresholdedblue)
    cv2.imshow('ErodedGreen',erodedgreen)
    cv2.imshow('ErodedBlue',erodedblue)
    frameg,centerg=segment(erodedgreen)
    framer,centerr=segment(erodedblue)
    r_list.append(centerr)
    g_list.append(centerg)
    cv2.imshow('TrackingScreen',frameg)

    #cv2.imshow('Video Red',framer)
    if(centerg!=None):      
      color="green"
      draw_path(centerg,color)
    if(centerr!=None):
      
      color="blue"
      draw_path(centerr,color)
     
    ch=cv2.waitKey(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            del g_list[:]
            del r_list[:]
            cap.release()
            cv2.destroyAllWindows()
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            break 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                del g_list[:]
                del r_list[:]
                cap.release()
                cv2.destroyAllWindows()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                break
        if event.type == pygame.VIDEORESIZE:
            # The main code that resizes the window:
            # (recreate the window with the new size)
            window = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            window.fill((255,255,255))
            for i in xrange(len(g_list)):
                 if(g_list[i]!=None):
                   color="green"  
                   draw_path(g_list[i],color)
                 if(r_list[i]!=None):
                   color="blue"  
                   draw_path(r_list[i],color)   
                
            
    if ch==27:
        break


#pygame.display.quit()
#pygame.quit()
#sys.exit()
