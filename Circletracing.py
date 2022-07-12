from typing import final
import pygame,time,ctypes,math
from enum import Enum, auto
from pygame.constants import K_LEFT, K_RIGHT, K_a, K_d, K_s, K_w

from pygame.draw import circle

class Shape(Enum):
    #different shapes

    circle = auto()
    rectangle = auto()
    line = auto()

pygame.init

caption = 'engine'

w_x = 1920
w_y = 1080
s_x = 1920 / w_x
s_y = 1080 / w_y
frame_dist = 0
fps_limit = 60
shapes = []
objects = []
default_color = (255,0,0)
camx = 0
camy = 0
camrot = 0
rot_speed = 1
pos_speed = 5
pi = 3.14159265359
#shapes template  [what shape,color,x,y,shape_attrebutes,thicknes]

ctypes.windll.user32.SetProcessDPIAware()
win = pygame.display.set_mode((w_x,w_y))
pygame.display.set_caption("seating")


#loads image
def loadify(image_path):
    return pygame.image.load(image_path).convert_alpha()

#creates a shape
def create_shape(shape,color,x,y,shape_attributes,thickness=0):
    global shapes
    temp = []
    temp.append(shape)
    temp.append(color)
    temp.append(x)
    temp.append(y)
    temp.append(shape_attributes)
    temp.append(thickness)
    shapes.append(temp)

def create_object(shape,color,x,y,shape_attributes,thickness=0):
    global objects
    temp = []
    temp.append(shape)
    temp.append(color)
    temp.append(x)
    temp.append(y)
    temp.append(shape_attributes)
    temp.append(thickness)
    objects.append(temp)

#renders sprite
def render(image,x,y):
    win.blit(image,(x * s_x, y * s_y))

#draws rectangle
def draw_shape(shape,color,shape_attrebutes,x,y,border = 0):
    if shape == Shape.circle:
        pygame.draw.circle(win,color,(x,y),shape_attrebutes,border)

    if shape == Shape.line:
        pygame.draw.line(win,color,(x,y),(shape_attrebutes[0],shape_attrebutes[1]),border)
    
#coverts drgrees to radians
def rad_convert(deg):
    return deg * pi/180

#shoots a ray
def shoot_ray(x,y,dist,rot = 0):
    rx = x
    ry = y
    final_dist = dist
    while dist <= 2000 and dist >= 0.1:

        rx = rx + (dist * math.sin(rad_convert(rot)))  #moves the ray along the x axis
        ry = ry + (dist * math.cos(rad_convert(rot)))  #moves the ray along the y axis
        final_dist += dist
        dist = true_dist(rx,ry)        

        create_shape(Shape.circle,default_color,rx,ry,dist,1)

    if dist <= 0.1:
        return final_dist / 2

#gets dist to a shape
def get_dist(shape,px,py,sx,sy,shape_attributes):

    #for circle shape attrebutes = r
    if shape == Shape.circle:
        return math.dist([px,py],[sx,sy])-shape_attributes

    if shape == Shape.rectangle:
        rx = shape_attributes[0]  #x of square
        ry = shape_attributes[1]  #y of square
        dx = (sx-rx) - px  #dist from the closest x side 
        dy = (sy-ry) - py  #dist from the closest y side 
        cx = sx-rx  #x of the side of the square
        cy = sy-ry  #y of the side of the square


def true_dist(x,y):
    temp = []
    for char in objects:
        temp.append(get_dist(char[0],x,y,char[2],char[3],char[4]))

    return min(temp)


def draw_shape_stack(draw):
    for char in draw: 
        draw_shape(char[0],char[1],char[4],char[2],char[3],char[5])
        

    return None


#setup before main loop runs once
def setup():
    pass



#main draw function
def draw():
    global shapes
    global objects
    win.fill((0,0,0))
    shapes = []
    objects = []

    add_to_stack()

    

    ray_ammount = 1
    cool = 360 / ray_ammount
    for x in range(0,ray_ammount+1):
        shoot_ray(camx,camy,frame_dist,x*cool+camrot)
    

    stack = []
    for char in objects:
        stack.append(char)
    for char in shapes:
        stack.append(char)

    draw_shape_stack(stack)
    pygame.display.update()

def add_to_stack():
    create_object(Shape.circle,default_color,500,100,130,2)
    create_object(Shape.circle,default_color,1400,100,130,2)
    create_object(Shape.circle,default_color,950,600,400,2)
    create_shape(Shape.circle,(0,0,255),camx,camy,abs(float(frame_dist)))
    create_shape(Shape.circle,(255,0,0),camx,camy,abs(float(frame_dist)),2)


#setups the game
setup()



run = True
#main loop
while run:

    time.sleep((1 / fps_limit)*0.625)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        #if you click the x on the window it closes
        if event.type == pygame.QUIT:
            run = False

    keys=pygame.key.get_pressed()
    mousepos = pygame.mouse.get_pos()

    if keys[K_LEFT]:
        camrot += 3
    if keys[K_RIGHT]:
        camrot -= 3
    #if keys[K_a]:
        #camx -= pos_speed
    #if keys[K_d]:
        #camx += pos_speed
    #if keys[K_s]:
        #camy += pos_speed
    #if keys[K_w]:
        #camy -= pos_speed

    camy = mousepos[1]
    camx = mousepos[0]

    add_to_stack()
    
    frame_dist = true_dist(camx,camy)

    draw()