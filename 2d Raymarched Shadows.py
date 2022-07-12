import pygame,time,ctypes,math
from enum import Enum, auto

from pygame.draw import circle

class Shape(Enum):
    #different shapes

    circle = auto()
    rectangle = auto()
    line = auto()
    circle_abs = auto()

pygame.init
pygame.font.init()

caption = 'engine'
myfont = pygame.font.SysFont("monospace", 15)


w_x = 1920
w_y = 1080
s_x = 1920 / w_x
s_y = 1080 / w_y
frame_dist = 0
fps_limit = 120
shapes = []
objects = []
default_color = (255,0,0)
camx = 1000
camy = 0
camrot = 0
rot_speed = 3
pos_speed = 5
pi = 3.14159265359
start_time = time.time()
counter = 0
delta_time = 0
fps = fps_limit*2
start_time = time.time()
rot = []
rays = 10000
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

    if shape == Shape.rectangle:
        pygame.draw.rect(win,color,pygame.Rect(x,y,shape_attrebutes[0],shape_attrebutes[1]),border)
        
    
#coverts drgrees to radians
def rad_convert(deg):
    return deg * pi/180     

#gets dist to a shape
def get_dist(shape,px,py,sx,sy,shape_attributes):

    #for circle shape attrebutes = r
    if shape == Shape.circle_abs:
        return math.dist([px,py],[sx,sy])-shape_attributes

    if shape == Shape.circle:
        return math.dist([px,py],[sx,sy])-shape_attributes

    if shape == Shape.rectangle:
        sx += shape_attributes[0]/2
        sy += shape_attributes[1]/2
        tx = abs(px - sx)
        ty = abs(py - sy)
        dx = (tx - (shape_attributes[0] /2))
        dy = (ty - (shape_attributes[1] /2))
        return math.sqrt(math.pow(max(dx,0),2)+pow(max(dy,0),2))

    if shape == Shape.line:
        pass

def true_dist(x,y):
    temp = []
    for char in objects:
        temp.append(get_dist(char[0],x,y,char[2],char[3],char[4]))

    return min(temp)


def draw_shape_stack(draw):
    for char in draw: 
        draw_shape(char[0],char[1],char[4],char[2],char[3],char[5])
        

    return None

#shoots a ray
def shoot_ray(x,y,dist,cos,sin):
    rx = x
    ry = y
    final_dist = dist
    while dist <= 2000 and dist >= 0.1:
        dist = true_dist(rx,ry)
        rx = rx + (dist * sin)  #moves the ray along the x axis
        ry = ry + (dist * cos)  #moves the ray along the y axis
        final_dist += dist

    create_shape(Shape.line,default_color,x,y,[rx,ry],1)

    if dist <= 0.1:
        return final_dist / 2

#setup before main loop runs once
def setup():
    initrot(rays)

def initrot(number):
    global rot
    for i in range(number+1):
        temp = []
        temp.append(math.cos(rad_convert((i/number)*360)))
        temp.append(math.sin(rad_convert((i/number)*360)))
        rot.append(temp)


def add_to_stack():
    global shapes
    global objects
    shapes = []
    objects = []
    create_object(Shape.circle,(0,0,255),w_x/2,w_y/2,100)
    #create_object(Shape.circle,default_color,1500,100,130,2)
    #create_object(Shape.rectangle,default_color,500,500,[800,500],2)
    #create_shape(Shape.circle,(0,0,255),mousepos[0],mousepos[1],abs(float(frame_dist)))
    #create_shape(Shape.circle,(255,0,0),mousepos[0],mousepos[1],abs(float(frame_dist)),2)


#setups the game
setup()


def calculations():
    global keys
    global mousepos
    global camx
    global camy
    global frame_dist
    keys=pygame.key.get_pressed()
    mousepos = pygame.mouse.get_pos()
    frame_dist = true_dist(camx,camy)
    camy = mousepos[1]
    camx = mousepos[0]
    calc_rays(rays,360)
    
def calc_rays(ray_ammount,degrees):
    cool = degrees / ray_ammount
    processes = []
    for x in range(ray_ammount+1):
        shoot_ray(camx,camy,frame_dist,rot[x-1][0],rot[x-1][1])


def gui():
    global fps
    global shapes
    global objects
    win.fill((0,0,0))

    #adds all of the objects/shapes to a list
    stack = []
    for char in objects:
        stack.append(char)
    for char in shapes:
        stack.append(char)
    
    #takes that list and renders it
    draw_shape_stack(stack)

    #displays fps in top right
    label = myfont.render(str(round(fps*10)/10), 1, (255,255,0))
    win.blit(label, (1865, 4))

    #updates window
    pygame.display.update()


run = True
#main loop
def main():
    global counter
    global start_time
    global fps
    global start_time
    global run
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        #if you click the x on the window it closes
        if event.type == pygame.QUIT:
            run = False

    #initalises scene
    add_to_stack()
    #does calculations to find stuff
    calculations()
    #renders the calculations
    gui()
    

    counter+=1
    if (time.time() - start_time) > .1 :
        fps = counter / (time.time() - start_time)
        counter = 0
        start_time = time.time()

if __name__ == '__main__':
    while run:
        main()