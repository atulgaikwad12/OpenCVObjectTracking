# ex09DrawHousesWithTests.py  Starting Point for drawing functions
# P. Conrad for CS5nm, 10/14/2008

# NOTE: When you run this file, it does NOT draw anything until you type:
#    draw()
# at the Python Shell prompt.


# stuff we need to import in order to use PyGame

import pygame
from pygame.locals import *
from sys import exit


# A function for running test cases
# Note that \ character at the end of a line means that the line continues
# on the next line

def check_expect(test,check,expect):
    if (check == expect):
        print "Test " + test + " passed."
    else:
        print "Test " + test + " failed: expected " + str(expect)  + \
              " but I got " + str(check)

# makeHouseFrame   make the list of points for the frame of a house
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
# produces
#     a list of points
#
# Note that this doesn't actually draw a house.  It just returns a list
#  of points we can pass to pygame.draw.lines (with closed=False)

def makeHouseFrame(x,y,width,height):
    points = [] # start with an empty list
    points.append((x,y- ((2/3.0) * height))) # top of 1st story, upper left
    points.append((x,y))  # lower left corner
    points.append((x+width,y)) # lower right corner
    points.append((x+width,y-(2/3.0) * height)) # top of 1st story upper right
    points.append((x,y- ((2/3.0) * height))) # top of first story, upper left
    points.append((x + width/2.0,y-height)) # top of roof
    points.append((x+width,y-(2/3.0)*height)) # top of 1st story, upper right
    return points

# Test cases for makeHouseFrame

check_expect("makeHouseFrame test 1",
             makeHouseFrame(100,200,120,150),
             [(100,100), (100,200),  (220,200), (220,100),
              (100,100), (160,50), (220,100)])
                  
check_expect("makeHouseFrame test 2",
             makeHouseFrame(200,200,120,150),
             [(200,100), (200,200),  (320,200), (320,100),
              (200,100), (260,50), (320,100)])

check_expect("makeHouseFrame test 3",
             makeHouseFrame(100,200,100,75),
             [(100,150), (100,200),  (200,200), (200,150),
              (100,150), (150,125), (200,150)])

# makeHouseWindowFrame    make the list of points for the window frame on a house
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
# produces
#     a list of points
#
# Note: to draw, pass these points to pygame.draw.lines (with closed=True)

def makeHouseWindowFrame(x,y,width,height):
   winLeft = x + 0.5 * width
   winRight = x + 0.9 * width
   winTop = y - 0.4 * height
   winBot = y - 0.2 * height
   points = [(winLeft, winBot), (winRight, winBot), (winRight, winTop), (winLeft, winTop)]
   return points

check_expect("makeHouseWindowFrame test 1",
             makeHouseWindowFrame(100,200,120,150),
             [(160,170), (208,170),  (208,140), (160,140)])

# @@@ ADD ONE MORE TEST CASE FOR THIS FUNCTION


# makeHouseWindowHoriz    make the list of points for the horizontal line through the window
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
# produces
#     a list of points
#
# Note: to draw, pass these points to pygame.draw.lines (with closed=False)

def makeHouseWindowHoriz(x,y,width,height):
   winLeft = x + 0.5 * width
   winRight = x + 0.9 * width
   winTop = y - 0.4 * height
   winBot = y - 0.2 * height
   winMidHoriz = y - 0.3 * height   # horizontal midpoint line passes through here
   points = [(winLeft, winMidHoriz), (winRight, winMidHoriz)]
   return points

check_expect("makeHouseWindowHoriz test 1",
             makeHouseWindowHoriz(100,200,120,150),
             [(160,155), (208,155)])

check_expect("makeHouseWindowHoriz test 2",
             makeHouseWindowHoriz(150,250,100,200),
             [(200,190),(240,190)])


# makeHouseWindowVert    make the list of points for the vertical line through the window
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
# produces
#     a list of points
#
# Note: to draw, pass these points to pygame.draw.lines (with closed=False)

def makeHouseWindowVert(x,y,width,height):
   winTop = y - 0.4 * height
   winBot = y - 0.2 * height
   winLeft = x + 0.5 * width
   winRight = x + 0.9 * width
   winMidVert = x + 0.7 * width   # horizontal midpoint line passes through here
   points = [(winMidVert, winLeft), (winMidVert, winRight)]
   return points

check_expect("makeHouseWindowVert test 1",
             makeHouseWindowVert(100,200,120,150),
             [(184,140),(184,170)])

# @@@ ADD ONE MORE TEST CASE FOR THIS FUNCTION

# makeHouseDoor    make the list of points for the door
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
# produces
#     a list of points
#
# Note: to draw, pass these points to pygame.draw.lines (with closed=False)

def makeHouseDoor(x,y,width,height):
   points = [] # a stub with a empty list of points
   return points


# @@@ ADD TWO TEST CASES FOR THIS FUNCTION
                                    
# a function to draw a house with PyGame
# consumes:
#     x, y  (numbers: lower left corner of the house)
#     width, height  (numbers: width and height of house)
#     screen (the screen where we should draw this house)
#     color (a tuple of (r, g, b) representing a color)
# produces
#     nothing
# side effect
#     draws a house on the screen of the size and color given,
#     at the location given
                  
def drawHouse(x,y,width,height,screen,color):
    lineThickness = 2              
    pygame.draw.lines(screen, color, False,
                      makeHouseFrame(x,y,height,width), lineThickness)
    pygame.draw.lines(screen,color, True,
                      makeHouseWindowFrame(x,y,height,width), lineThickness)
    pygame.draw.lines(screen,color,False,
                      makeHouseWindowVert(x,y,height,width), lineThickness)
    pygame.draw.lines(screen,color,False,
                      makeHouseWindowHoriz(x,y,height,width), lineThickness)
    # @@@ Add code here to draw the door after makeHouseDoor is defined properly

# draw()  a function to actually do the drawing
#  consumes and produces nothing
#  side effect: we see a window with our drawing
#  to call this function, type draw() in the Python Shell after you do "Run Module" in IDLE

def draw():
    
    # set up a window (a.k.a. a screen)

    size = width, height = 640,480
    pygame.init()
    screen = pygame.display.set_mode(size)

    # set up variables for colors

    red = (255, 0, 0 )  # an RGB 3-tuple representing red
    green = (0, 255, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)

    # main loop

    while True: # loop forever (or at least until someone generates a QUIT event)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()

        screen.fill(white); # Make the whole screen white

        # Now, draw three houses
    
        drawHouse(100,200,120,150,screen,red) 
        drawHouse(400,200,120,150,screen,green) 
        drawHouse(400,400,120,150,screen,blue) 

        # But, we don't actually SEE the houses until we call "update".
        pygame.display.update()
