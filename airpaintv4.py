import pygame, sys
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
from pygame.locals import *

mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)


lowerBound=np.array([33,80,40],np.uint8)#lower limit HSV values for Green(using trial and error)
upperBound=np.array([102,255,255],np.uint8)#upper limit HSV value

cam= cv2.VideoCapture(0)
cv2.namedWindow('ErodedGreen',cv2.WINDOW_NORMAL)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0



    
windowSurface = pygame.display.set_mode((640,420), pygame.RESIZABLE)

## Colors list
GREEN = (0, 255, 0)
GRAY = (197, 197, 197)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (107, 104, 99)
PINK = (249, 57, 255)
LIGHT_BLUE = (54, 207, 241)
YELLOW = (255, 241, 73)
ORANGE = (252, 155, 64)
PURPLE = (167, 0, 238)
DARK_GREEN = (58, 158, 73)
WHITE = (255, 255, 255)
BROWN = (85, 46, 46)
PRETTY_BLUE = (0, 238, 195)







##
fish = pygame.image.load("img/fish.jpg")
shark = pygame.image.load("img/flower.png")
eraser1 = pygame.image.load("img/eraser.jpg")
fish_button_1 = pygame.transform.scale(fish, (40, 40))
fish_button_2 = pygame.transform.scale(shark, (40, 40))
eraser = pygame.transform.scale(eraser1, (40, 40))
fish_rect = pygame.Rect(5, 120, 40, 40)
shark_rect = pygame.Rect(47, 120, 40, 40)
stamp = "Fish"
stamp_state = False


pygame.init()


## font setup
menu_font = pygame.font.Font("font/FreeSans.ttf", 17)
menu_text = menu_font.render("Air Paint", True, BLACK)

clear_text = menu_font.render("  Clear", True, BLACK)
brush_text = menu_font.render("Brushes", True, BLACK)

save_text = menu_font.render("  SAVE", True, BLACK)



draw = False
brush_size = 10
brush_color = GREEN


menu_rect = pygame.Rect(0, 0, 100, 640)
screen_rect = pygame.Rect(100, 0, 640, 420)



green_rect = pygame.Rect(5, 55, 20, 20)
red_rect = pygame.Rect(27, 55, 20, 20)
blue_rect = pygame.Rect(49, 55, 20, 20)
pink_rect = pygame.Rect(71, 55, 20, 20)
light_blue_rect = pygame.Rect(5, 77, 20, 20)
yellow_rect = pygame.Rect(27, 77, 20, 20)
orange_rect = pygame.Rect(49, 77, 20, 20)
purple_rect = pygame.Rect(71, 77, 20, 20)
dark_green_rect = pygame.Rect(5, 99, 20, 20)
brown_rect = pygame.Rect(27, 99, 20, 20)
white_rect = pygame.Rect(49, 99, 20, 20)
pretty_blue_rect = pygame.Rect(71, 99, 20, 20)

clear_rect = pygame.Rect(10, 290, 70, 25)

eraser_rect = pygame.Rect(27, 210, 40, 40)

thin_brush = pygame.Rect(5, 185, 20, 20)
medium_brush = pygame.Rect(27, 185, 20, 20)
thick_brush = pygame.Rect(49, 185, 20, 20)
supa_brush = pygame.Rect(71, 185, 20, 20)


save_rect = pygame.Rect(5, 260, 90, 25)
save_flag = False
file_number = 1

element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))#used for erode operation

arlimit_l=400#lower area limit of valid blob
arlimit_h=2000#upper area limit of valid blob
asp_l=0.33#lower and upper limits for aspect ratio of valid blob
asp_h=2.33
conts = list()



#while True:
while(cam.isOpened()):
    ret, img=cam.read()
    conts=[]
    img2=cv2.resize(img,(340,220))
    #imgflip=cv2.flip(img2,1)#mirror in x direction(horizontal)**
    img=cv2.medianBlur(img2,3)#use median blur with given parameters
    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    eroded=cv2.erode(mask,element)#erode to avoid peppers
    #return eroded

    #morphology
    maskOpen=cv2.morphologyEx(eroded,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    
    maskFinal=maskClose
    cv2.imshow('ErodedGreen',maskClose)
    contss,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for i,cnt in enumerate(contss):#iterate on possible blobs
        x,y,w,h=cv2.boundingRect(cnt)#rectangular boundary parameters
        cont_area=w*h#area of blob
        
        if cont_area>arlimit_l and cont_area<arlimit_h:#conditional nesting to select blob satisfying given constraints
            aspect=float(w)/float(h)
            if aspect>asp_l and aspect<asp_h:
               conts.append(cnt)
               


    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
            
            #mouse.release(Button.left)
            cv2.putText(img,"Mouse is Released ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,0.5, 2)
            draw = False
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=x1+w1/2
        cy1=y1+h1/2
        cx2=x2+w2/2
        cy2=y2+h2/2
        cx=(cx1+cx2)/2
        cy=(cy1+cy2)/2
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc 
        #while mouse.position!=mouseLoc:
            #pass
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchFlag==0):
            pinchFlag=1           
     
            #mouse.press(Button.left)
            cv2.putText(img,"Mouse is Pressed ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,0.5, 2)
            draw = True
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx=x+w/2
        cy=y+h/2
        cv2.circle(img,(cx,cy),(w+h)/4,(0,0,255),2)
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc 
        #while mouse.position!=mouseLoc:
            #pass
    cv2.imshow("cam",img)

    
    for event in pygame.event.get():
        if event.type == QUIT:
            cam.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                cam.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            draw = True
        if event.type == MOUSEBUTTONUP:
            draw = False

        
    # Drawing dot when mousebuttondown
    mouse_pos = pygame.mouse.get_pos()
    if draw == True and mouse_pos[0] > 100 and brush_color != BLACK and stamp_state == False:
        pygame.draw.circle(windowSurface, brush_color, mouse_pos, brush_size)
        save_flag = False
    #if eraser is selected     
    if draw == True and mouse_pos[0] > 100 and brush_color == BLACK and stamp_state == False:
        lstr = list(mouse_pos)
        pygame.draw.rect(windowSurface, brush_color, (lstr[0]-brush_size,lstr[1]-brush_size,brush_size*2,brush_size*2))
        #pygame.draw.rect(window,(255,255,255), (lstr[0]-10,lstr[1]-10,20,20))
        save_flag = False



    ## Drawing stamp when mousebuttondown
    mouse_pos = pygame.mouse.get_pos()
    if draw == True and mouse_pos[0] > 100 and stamp == "Fish" and stamp_state == True:
        windowSurface.blit(fish_button_1, mouse_pos)
        draw = False
        save_flag = False
                    
        

    mouse_pos = pygame.mouse.get_pos()
    if draw == True and mouse_pos[0] > 100 and stamp == "Shark" and stamp_state == True:
        windowSurface.blit(fish_button_2, mouse_pos)
        draw = False
        save_flag = False





    
    # collision detection for COLOR
    if draw == True:    
        if green_rect.collidepoint(mouse_pos):
            brush_color = GREEN
            stamp_state = False
        if red_rect.collidepoint(mouse_pos):
            brush_color = RED
            stamp_state = False
        if blue_rect.collidepoint(mouse_pos):
            brush_color = BLUE
            stamp_state = False
        if pink_rect.collidepoint(mouse_pos):
            brush_color = PINK
            stamp_state = False
        if light_blue_rect.collidepoint(mouse_pos):
            brush_color = LIGHT_BLUE
            stamp_state = False
        if yellow_rect.collidepoint(mouse_pos):
            brush_color = YELLOW
            stamp_state = False
        if orange_rect.collidepoint(mouse_pos):
            brush_color = ORANGE
            stamp_state = False
        if purple_rect.collidepoint(mouse_pos):
            brush_color = PURPLE
            stamp_state = False
        if dark_green_rect.collidepoint(mouse_pos):
            brush_color = DARK_GREEN
            stamp_state = False
        if white_rect.collidepoint(mouse_pos):
            brush_color = WHITE
            stamp_state = False
        if brown_rect.collidepoint(mouse_pos):
            brush_color = BROWN
            stamp_state = False
        if pretty_blue_rect.collidepoint(mouse_pos):
            brush_color = PRETTY_BLUE
            stamp_state = False

    ## collision detection for eraser
    if draw == True:
        if eraser_rect.collidepoint(mouse_pos):
            brush_color = BLACK
            stamp_state = False

    
    ## collision detection for CLEAR
    if draw == True:
        if clear_rect.collidepoint(mouse_pos):
            pygame.draw.rect(windowSurface, BLACK, screen_rect)
            
    
    pygame.draw.rect(windowSurface, GRAY, menu_rect)
    windowSurface.blit(menu_text, (10, 20))
    
    pygame.draw.line(windowSurface, BLACK, (0, 40), (100, 40))
    pygame.draw.line(windowSurface, BLACK, (0, 45), (100, 45))
    
    pygame.draw.rect(windowSurface, DARK_GRAY, clear_rect)
    windowSurface.blit(clear_text, (10, 290))

    ##
    windowSurface.blit(brush_text, (10, 160))
    pygame.draw.line(windowSurface, BLACK, (0, 180), (100, 180))
    

    ## Blit the save rect
    pygame.draw.rect(windowSurface, DARK_GRAY, save_rect)
    windowSurface.blit(save_text, (13, 262))




## Collision detection for SAVE
    
    if draw == True and save_flag == False:
        if save_rect.collidepoint(mouse_pos):
            print("File has been saved :P")
            save_surface = pygame.Surface((380, 320))
            save_surface.blit(windowSurface, (0, 0), (100, 0, 380, 320))
            
            
            try:
                with open("saved_files/PaintImage_" + str(file_number) + ".png"):
                    print("file already exists")
                    file_number = file_number + 1
                    save_flag = True
            except IOError:
                save_flag = True
                
            pygame.image.save(save_surface, "saved_files/PaintImage_" + str(file_number) + ".png")
        




 ## collision detectin for BRUSH SIZE
    if draw == True:
        if thin_brush.collidepoint(mouse_pos):
            brush_size = 1
        if medium_brush.collidepoint(mouse_pos):
            brush_size = 3
        if thick_brush.collidepoint(mouse_pos):
            brush_size = 5
        if supa_brush.collidepoint(mouse_pos):
            brush_size = 10
    



## collision detection for STAMP
    if draw == True:
        if fish_rect.collidepoint(mouse_pos):
            stamp = "Fish"
            stamp_state = True
        if shark_rect.collidepoint(mouse_pos):
            stamp = "Shark"
            stamp_state = True


    
    
    # rect for brush_color
    pygame.draw.rect(windowSurface, GREEN, green_rect)
    if brush_color == GREEN:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, green_rect, border)
    
    
    
    pygame.draw.rect(windowSurface, RED, red_rect)
    if brush_color == RED:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, red_rect, border)
    
    
    
    pygame.draw.rect(windowSurface, BLUE, blue_rect)
    if brush_color == BLUE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, blue_rect, border)

    pygame.draw.rect(windowSurface, PINK, pink_rect)
    if brush_color == PINK:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, pink_rect, border)

    pygame.draw.rect(windowSurface, LIGHT_BLUE, light_blue_rect)
    if brush_color == LIGHT_BLUE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, light_blue_rect, border)

    pygame.draw.rect(windowSurface, YELLOW, yellow_rect)
    if brush_color == YELLOW:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, yellow_rect, border)

    pygame.draw.rect(windowSurface, ORANGE, orange_rect)
    if brush_color == ORANGE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, orange_rect, border)
    
    pygame.draw.rect(windowSurface, ORANGE, orange_rect)
    if brush_color == ORANGE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, orange_rect, border)
    
    pygame.draw.rect(windowSurface, DARK_GREEN, dark_green_rect)
    if brush_color == DARK_GREEN:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, dark_green_rect, border)
    
    pygame.draw.rect(windowSurface, PURPLE, purple_rect)
    if brush_color == PURPLE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, purple_rect, border)
    
    pygame.draw.rect(windowSurface, WHITE, white_rect)
    if brush_color == WHITE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, white_rect, border)
    
    pygame.draw.rect(windowSurface, BROWN, brown_rect)
    if brush_color == BROWN:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, brown_rect, border)
    
    pygame.draw.rect(windowSurface, PRETTY_BLUE, pretty_blue_rect)
    if brush_color == PRETTY_BLUE:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, pretty_blue_rect, border)
    
    
    
    #### RECT FOR ERASER
    windowSurface.blit(eraser, eraser_rect)
    if brush_color == BLACK:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, BLACK, eraser_rect, border)
 



    # Rect for brush size

    
    if brush_size == 1:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, BLACK, thin_brush, brush_border)
    pygame.draw.circle(windowSurface, BLACK, thin_brush.center, 1)
    pygame.draw.rect(windowSurface, BLACK, thin_brush, brush_border)
    
    
    if brush_size == 3:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, BLACK, medium_brush, brush_border)
    pygame.draw.circle(windowSurface, BLACK, medium_brush.center, 3)
    pygame.draw.rect(windowSurface, BLACK, medium_brush, brush_border)
    
    
    if brush_size == 5:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, BLACK, thick_brush, 1)
    pygame.draw.circle(windowSurface, BLACK, thick_brush.center, 5)
    pygame.draw.rect(windowSurface, BLACK, thick_brush, brush_border)
    
    
    if brush_size == 10:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, BLACK, supa_brush, brush_border)
    pygame.draw.circle(windowSurface, BLACK, supa_brush.center, 10)
    pygame.draw.rect(windowSurface, BLACK, supa_brush, brush_border)





## Blitting the stamp
    if stamp == "Fish":
        stamp_border = 3
    else:
        stamp_border = 1
    windowSurface.blit(fish_button_1, (5, 120))
    pygame.draw.rect(windowSurface, BLACK, fish_rect, stamp_border)


    if stamp == "Shark":
        stamp_border = 3
    else:
        stamp_border = 1
    windowSurface.blit(fish_button_2, (47, 120))
    pygame.draw.rect(windowSurface, BLACK, shark_rect, stamp_border)
    
    pygame.display.update()
