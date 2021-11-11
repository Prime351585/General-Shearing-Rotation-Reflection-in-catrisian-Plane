from random import randint
import numpy as np
import pygame
from math import sin,cos
from pygame import font

#                               //////////////////////////////// Usage ////////////////////////////////////////

#                   first the programm will ask the number of Points the shape have which we want to work with
#                   After specifying the number of points it will ask the points in the form x,y
#                   After giving the coordinates a pygame window should open according to the Parameters we have setted.

#                     //////////////////////////////// Parameters You can change: //////////////////////////////////

# alpha(at line 78) - lets user specify the angle of axis of rotation or reflection Whatever the case is
# shearx,sheary(at line 81,82) - Lets user shear their shape in x or y direction in both cases reflection or rotation 
# Rotation or Reflection(at line 179) -Lets user choose weather to use Rotation or Reflection
#  For switiching from Reflection to Rotation user can switch the Rotationmatrix to Reflectionmatrix available at line 179 
# Animation(at line 179) - If you want to change theta continuously so we can add time with alpha Eg. alpha+time..........in line 179
# 

# Defining Color  For Further use
White=(255,255,255)
Black=(0,0,0)
Green=(0,255,0)
Blue = (0,0,255)
# //////////////////
width,height=850,850                # Defining Width and Height of Pygame window

# Now Pygame is only made for making games so we'll have to manually utilise it to make grids for plotting
# We First define the Xlim and Ylim for our graph

xlim=[-7,7]
ylim=[-7,7]

# Now we will scale our both x and y axis by dividing the whole width from number of lines we want

scalex=width/(xlim[1]-xlim[0])
scaley=height/(ylim[1]-ylim[0])

# ///// this is time we'll use in our infinite loop

time=0

gameDisplay=pygame.display.set_mode((width,height))     # This Line of code creates a pygame canvas for given width and height and we will draw on this canvas for further use
pygame.font.init()                                      # initialising font for further use
font=pygame.font.Font('freesansbold.ttf',15)            # We store font type and size in a font variable

# ////// This is a general Function which connects our cartisian coordinates to Pygame canvas For example if we want to plot a point as (1,1) so we will use this as T((1,1))

def T(twoDtuple):
    return(float(scalex*(twoDtuple[0]-xlim[0])),float(height-scaley*(twoDtuple[1]-ylim[0])))

# //////////////////////////////
# This Peice of we'll use after we create this build completely basically if this  function is called the program ends without closing the Pygame window

# def end():
#     while end:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         pygame.display.update()
#         pygame.time.Clock().tick(0)
# //////////////////////////////

# This is Function used if we want to trace any animation.....we can use this in rotation but not now..... : )

# Point=[]
# def drawpoint(k):
#     Point.append(k)
#     for i in range(len(Point)):
#         pygame.draw.circle(gameDisplay,Green,((int(Point[i][0]),int(Point[i][1]))),10)
    
#  Now this is the whole Transform Part
# /////////////////////////////Transform Part ////////////////////////////

alpha=90*np.pi/180     # <-------Change this to change theta
#  Change them to shear in x or y directions.

shearx=0                                    # Shearing if we want to Shear in x direction
sheary=0                                    # Shearing if we want to Shear in y direction

# /// Now this is our transformation matrix

#  For Reflection   [ cos(2*alpha)              sin(2*alpha)+shearx]
#                   [ sin(2*alpha)+sheary       -cos(2*alpha)      ]

#  For Rotation with shearing     [  cos(alpha)             -sin(alpha)+shearx]
#                                 [  sin(alpha)+sheary              cos(alpha)]

def ReflectionMatrix(alpha):
    a,b,c,d=round(cos(2*alpha),4),round(sin(2*alpha)+shearx,4),round(sin(2*alpha)+sheary,4),round(-cos(2*alpha),4)
    Rmatrix=np.array([[a,b],[c,d]])
    return(Rmatrix)

def RotationMatrix(alpha):
    a,b,c,d=round(cos(alpha),4),round(-sin(alpha)+shearx,4),round(sin(alpha)+sheary,4),round(cos(alpha),4)
    Rmatrix=np.array([[a,b],[c,d]])
    return(Rmatrix)

# ////////// Here we input number of points the Polygon has which has to be transformed

n=int(input("Number of points ="))

# ////////// This Array Will Hold the Points We input as inputPoint=[(Xn,Yn)]
inputPoint=[]

# ////////////////////// This Peice of code will ask input from user for the Points and 
# if by mistake someone makes any mistake while inputting the Points it will give warning and Prompt user to again input numbers from starting
# /////(Corr1...: ))

i=0
while True:

    a=tuple(map(float,(input("Enter Point P"+str(i+1)+"(x,y) ").split(','))))
    if len(a)!=2:
        print('Please Enter Correct tuple ')
        i=0
        continue
    inputPoint.append((a))
    i+=1
    if i==n:
        break
    else:pass
print(inputPoint)

# ///////////////////////////////////////////////////

#  This is Transform function Which Will transform our Points according to Transformation matrix

def transform(A,B):
    Result=A.dot(B)
    return (float(Result[0]),float(Result[1]))


# //////////////////////////////////////////////////////////////////////// From Here an infinite loop will run and every time it runs 
# completely it will update our display in according.

while True:

# /////////////////////////////////////////////////// Display Grid Setup ////////////////////////////

    gameDisplay.fill(White)    # Every time this while loop will run  it will clear whole window and Set it White.

#  This Peice of code is used to terminate program when one clicks on close button of Pygame window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

# //////////////////////////////////////////   From This we are drawing COORDINATE AXIS Lines

    pygame.draw.line(gameDisplay,Black,(scalex*(-xlim[0]),0),(scalex*(-xlim[0]),height),2)
    pygame.draw.line(gameDisplay,Black,(0,height-scaley*(-ylim[0])),(width,height-scaley*(-ylim[0])),2)

    # ///////// This for loop will draw all the lines of our grid accordint to scale we calculated above

    for i in range(int(scalex)):
    	pygame.draw.line(gameDisplay,Black,(i*scalex,0),(i*scalex,height),1)
    for i in range(int(scaley)):
    	pygame.draw.line(gameDisplay,Black,(0,i*scaley),(width,i*scaley),1)

# /////every time while loop runs time will increase by 0.5 this can be used to control speed of animation

    time+=0.05
# /////////////////   This is for Colouring lines every time while loop runs again these values gets updated

    r=84*randint(0,3)
    g=84*randint(0,3)
    b=84*randint(0,3)

# ///////////////////////////////////////////////////////////////////////////////////////////////////

    TrasformPoints=[]

    for i in inputPoint:
        TrasformPoints.append(transform(ReflectionMatrix(alpha),i)) # <---------------- Change me to switch from Rotation to reflection mode by changing Rotationmatrix to Reflectionmatrix and if want to add animation change alpha to (alpha+time)

# ///////////////////////////////////////////////////////////////////////////////////////////////////
# We are taking INPUTPOINTS and drawing Circles of radius 6 pixels in order to show where input Points are and We are using T((x,y)) not (x,y) for Plotting 

    for i in inputPoint:
        pygame.draw.circle(gameDisplay,Blue,T(i),6)
        
# ///////// Here We are connecting the InputPoints For making a closed Polygon 

    for i in range(len(inputPoint)):
            pygame.draw.line(gameDisplay,(r,g,b),T(inputPoint[i-1]),T(inputPoint[i]),3)

# We are taking TRANSFORMPOINTS and drawing Circles of radius 6 pixels in order to show where input Points are and We are using T((x,y)) not (x,y) for Plotting 

    for i in TrasformPoints:
        pygame.draw.circle(gameDisplay,Green,T(i),4)

# ///////// Here We are connecting the TransformPoints For making the Transformed closed Polygon 

    for i in range(len(TrasformPoints)):
            pygame.draw.line(gameDisplay,(r,g,b),T(TrasformPoints[i-1]),T(TrasformPoints[i]),3)

# ////////  We are Drawing the lines betwwen each inputpoints and there corresponding transformedpoints

    for i in range(len(TrasformPoints)):
            pygame.draw.line(gameDisplay,Black,T(TrasformPoints[i]),T(inputPoint[i]),1)

# ////////  We are Drawing mid Point Of Input Point and its corresponding Transformed Points

    for i in range(len(TrasformPoints)):
        pygame.draw.circle(gameDisplay,Green,((T(inputPoint[i])[0]+T(TrasformPoints[i])[0])/2,(T(inputPoint[i])[1]+T(TrasformPoints[i])[1])/2),4)
    
# ///////////////////////////////////////////////////////////////////////////////////////////////

# ///// We are writing the input Point Coordinates on display at there correspoinding Location

    for i in inputPoint:
        Data=font.render('('+str(round(i[0],3))+','+str(round(i[1],3))+')',True,Black,White)
        Datarect=Data.get_rect()
        Datarect.center=(T((i[0],i[1])))
        gameDisplay.blit(Data,Datarect)
# ///// We are writing the Transformed Point Coordinates on display at there correspoinding Location

    for i in TrasformPoints:
        Data=font.render('('+str(round(i[0],3))+','+str(round(i[1],3))+')',True,Black,White)
        Datarect=Data.get_rect()
        Datarect.center=(T((i[0],i[1])))
        gameDisplay.blit(Data,Datarect)

    # ////////////////////////////////////////////////////////////////////////////////////////////////
    pygame.time.wait(100)   # This Function Gives a delay of 200 millisecond between each frame
    pygame.display.update() # This Program Updates the Window after everything is drawn


# In Process by Harsh Maurya with 💖 ............ :)