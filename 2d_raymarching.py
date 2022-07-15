import pygame,ctypes,math,copy

pygame.init

circles = [[0,0,400],[-800,300,300],[700,700,300]]
CAPTION = 'engine'
XRES = 1920
YRES = 1080
MAX_RAY_ITTER = 50
RAYCOUNT = 360

ctypes.windll.user32.SetProcessDPIAware()
win = pygame.display.set_mode((XRES,YRES))
pygame.display.set_caption(f"{CAPTION}")

def shoot_ray(raypos,initaldist,rayangle):
    dist = initaldist
    pos = copy.copy(raypos)
    xrot = math.sin(math.radians(rayangle))
    yrot = math.cos(math.radians(rayangle))
    for _ in range(MAX_RAY_ITTER):
        pos[0] += dist*xrot
        pos[1] += dist*yrot
        dist = true_dist(pos)
        if dist > 5000 or dist < 0.01:
            break
    return pos

def true_dist(pos):
    dist = math.inf
    for circle in circles:
        temp = math.dist([circle[0],circle[1]],pos)-circle[2]
        if temp < dist: dist = temp
    return dist

run = True
#main loop
while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        #if you click the x on the window it closes
        if event.type == pygame.QUIT:
            run = False

    win.fill((0,0,0))

    mouse = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    inital_dist = true_dist(mouse)

    for circle in circles:
        pygame.draw.circle(win,(255,0,0),[circle[0],circle[1]],circle[2],1)
    
    for i in range(0,RAYCOUNT):
        ray = shoot_ray(mouse,inital_dist,(i/RAYCOUNT)*360)
        pygame.draw.line(win,(255,0,0),mouse,ray)

    pygame.display.update()