import cv2 
import matplotlib.pyplot as plt
import numpy as np
import imutils
import random
from PIL import Image as im

LEFT = 'left'
RIGHT = 'right'
FORWARD = 'forward'
BACKWARD = 'backward'
CAR_COLOR = (204,0,0)

prev_error = 0
derror = 0
acc = 1

def set_action(movement):
    a = np.array([0.0, 0.0, 0.0])
    if movement == LEFT:
        a[0] = -0.1
    if movement == RIGHT:
        a[0] = +0.1
    if movement == FORWARD:
        a[1] = +0.015
    if movement == BACKWARD:
        a[2] = +0.01
    return a

def get_car_pos(img_rgb):
    lower = np.asarray([200, 0, 0]) #color ranges of the car
    upper = np.asarray([220, 5, 5])
    mask = cv2.inRange(img_rgb, lower, upper)
    y_axis_lower = 0
    y_axis_upper = 0
    car_arr = mask.tolist()
    #get the y coordinates of the car
    for i in range(len(car_arr)):
        if y_axis_lower ==0 and sum(car_arr[i])!=0:
            y_axis_lower = i
        if y_axis_lower !=0 and sum(car_arr[i])==0:
            y_axis_upper = i-1
            break
    y_center = (y_axis_lower+y_axis_upper)/2    #center of the car on y-axis

    x_axis_lower = 0
    x_axis_upper = 0
    for i in range(len(car_arr[y_axis_lower])):
        if x_axis_lower==0 and car_arr[y_axis_lower][i]!=0:
            x_axis_lower = i
        if x_axis_lower!=0 and car_arr[y_axis_lower][i]==0:
            x_axis_upper = i-1
            break
    x_center = (x_axis_lower+x_axis_upper)/2

    return [x_center,y_center]

def pd_control(track, car):
    a = np.array([0.0, 0.0, 0.0])

    track_x = track[0]
    car_x = car[0]
    diff_std = -6.0
    offset = track_x - car_x -diff_std

    a[0] = offset*0.1   #adjust the steering proportionally to the deviation from the track center
    if abs(offset) < 1:
        a[1] = 0.015
    if abs(offset) > 3:
        a = set_action("backward")
    return a

def detect_track(im_rgb, display_plot):
    track_img = im_rgb
    lower = np.asarray([85, 85, 85])
    upper = np.asarray([110, 110, 110])
    mask = cv2.inRange(track_img, lower, upper)
    track_arr = mask.tolist()
    y_center = int(get_car_pos(im_rgb)[1]-2)
    x_axis_lower = 0
    x_axis_upper = 0
    #get center of the track on x-axis
    for i in range(len(track_arr[y_center])):
        if x_axis_lower == 0 and track_arr[y_center][i] != 0:
            x_axis_lower = i
        if x_axis_lower != 0 and track_arr[y_center][i] == 0:
            x_axis_upper = i - 1
            break
    x_center = (x_axis_lower + x_axis_upper) / 2

    if(display_plot):
        plt.imshow(mask)
        plt.draw()   

    return [x_center, y_center]

#### EXTRA CREDIT ####
def pid_control(track, car):
    pass

def pd_control_difficult(track, car):
    pass
