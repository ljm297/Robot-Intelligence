import sys
import math
import numpy as np
import random
import gym
from gym import spaces
from gym.envs.box2d.car_dynamics import Car
from gym.utils import seeding, EzPickle
from gym.envs.box2d import Box2D
from Box2D.b2 import polygonShape
from Box2D.b2 import contactListener
from Box2D.b2 import fixtureDef

import pyglet
import controller
from easytrack import EasyTrack
import matplotlib.pyplot as plt
import time
pyglet.options["debug_gl"] = False
from pyglet import gl
import cv2


if __name__ == "__main__":
    from pyglet.window import key

    a = np.array([0.0, 0.0, 0.0])

    env = EasyTrack()
    env.render()
    record_video = False
    if record_video:
        from gym.wrappers.monitor import Monitor

        env = Monitor(env, "/tmp/video-test", force=True)
    isopen = True
    while isopen:
        env.reset()
        total_reward = 0.0
        steps = 0
        restart = False
        for i in range(30):
            s, r, done, info = env.step(a)
            isopen = env.render()
        #TODO: try choosing an action at random before implementing the pd controller
        plt.ion()
        ctr = 0

        while True:
            #PART 1: Detecting the track
            track_location = controller.detect_track(s, False)
            #PART 2: Detecting the car
            car_pos = controller.get_car_pos(s)
            a = controller.pd_control(track_location, car_pos)
            s, r, done, info = env.step(a)

            print("\nHERE",s,r,done,info)

            total_reward += r
            if steps % 200 == 0 or done:
                print("\naction " + str(["{:+0.2f}".format(x) for x in a]))
                print("step {} total_reward {:+0.2f}".format(steps, total_reward))
            steps += 1

            isopen = env.render()
            if done or restart or isopen == False:
                break
    env.close()