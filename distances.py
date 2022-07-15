import math


#Defines what to put into functions
def formats():
    print(f'position3d = [x,y,z]')
    print(f'point3d = [x,y,z]')
    print(f'sphere3d = [x,y,z,radius]')
    print(f'cube3d = [x,y,z,width_X,width_Y,width_Z]')

def distance_sphere(position3d,sphere3d):
    return (math.dist(position3d,[sphere3d[0],sphere3d[1],sphere3d[2]]) - sphere3d[3])

def distance_circle(position2d,sphere2d):
    return (math.dist(position2d,[sphere2d[0],sphere2d[1]]) - sphere2d[2])

def distance_point(position3d,point3d):
    return math.dist(position3d,point3d)

def distance_cube(position3d,cube3d):
    print(f'does not support yet')
    pass

def dtr(deg):
    return deg * 3.141592/180

def get_ratios(rot_x,rot_y):
    ratio_x = math.sin(dtr(rot_y))*math.sin(dtr(rot_x))
    ratio_y = math.cos(dtr(rot_y))
    ratio_z = math.cos(dtr(rot_x))
    return [ratio_x,ratio_y,ratio_z]

