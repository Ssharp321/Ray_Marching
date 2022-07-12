import pygame,time,ctypes,math
from enum import Enum, auto

from pygame.draw import circle

class Shape(Enum):
    #different shapes

    circle = auto()
    rectangle = auto()

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

#gets dist to a shape
def get_dist(shape,px,py,sx,sy,shape_attributes):

    #for circle shape attrebutes = r
    if shape == Shape.circle:
        return math.dist([px,py],[sx,sy])-shape_attributes

    if shape == Shape.rectangle:
        temp = []
        sidex_l = sx - shape_attributes[0]
        sidex_r = sx + shape_attributes[0]
        sidey_u = sy - shape_attributes[1]
        sidey_b = sy + shape_attributes[1]
        tl_corner = (sidex_l ,sidey_u)
        tr_corner = (sidex_r ,sidey_u)
        br_corner = (sidex_r ,sidey_b)
        bl_corner = (sidex_l ,sidey_b)

        if px - sx < sx:
            temp.append(abs(px-sidex_l))
            temp.append(math.dist([px,py],tl_corner))
            temp.append(math.dist([px,py],bl_corner))
        if px - sx >= sx:
            temp.append(abs(px-sidex_r))
            temp.append(math.dist([px,py],tr_corner))
            temp.append(math.dist([px,py],br_corner))
        if py - sy >= sy:
            temp.append(abs(py-sidey_u))
        else:
            temp.append(abs(py-sidey_b))
        
        return min(temp)



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

    stack = []
    for char in objects:
        stack.append(char)
    for char in shapes:
        stack.append(char)

    draw_shape_stack(stack)
    pygame.display.update()

def add_to_stack():
    create_object(Shape.circle,(255,0,0),1000,800,100,2)
    create_shape(Shape.circle,(0,0,255),mousepos[0],mousepos[1],abs(float(frame_dist)))
    create_shape(Shape.circle,(255,0,0),mousepos[0],mousepos[1],abs(float(frame_dist)),2)


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

    mousepos = pygame.mouse.get_pos()

    add_to_stack()
    
    frame_dist = true_dist(mousepos[0],mousepos[1])

    draw()