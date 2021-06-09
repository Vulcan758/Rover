
import numpy as np
import cv2
from flask import Flask
import os

class VideoCamera():

    x = 320
    y = 240
    rate = 10

    def __init__(self):
        self.x_world = 0
        self.y_world = 0
#        if os.environ.get('WERKZEUG_RUN_MAIN') is False: #or Flask.debug is False:
        self.video = cv2.VideoCapture(0)
        print("Video Captured")
        

    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        success, image = self.video.read()

        image = cv2.circle(image, (VideoCamera.x, VideoCamera.y), 5, (255, 255, 255), 10)
        frame_flip = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

            #image = cv2.circle(image, (VideoCamera.x, VideoCamera.y), 5, (255, 255, 255), 10)

            #frame_flip = cv2.flip(image,1)
            #ret, jpeg = cv2.imencode('.jpg', frame_flip)
            #return jpeg.tobytes()


    def get_y_coords(self):

        y_world = 53.9 + (-0.187 * (VideoCamera.y)) + ((1.56 * 10**-4) * (VideoCamera.y)**2)

        #px_cm = 27.5 + (-0.64 * (y_world)) + (-0.0216 * (y_world)**2)

        #x_world = (x - 310) / px_cm

        #print(f"the real world y coordinates is {y_world}")

        self.y_world = y_world

        return y_world

    def get_x_coords(self):

        px_cm = 27.5 + (-0.64 * (self.y_world)) + (-0.0216 * (self.y_world)**2)

        x_world = (VideoCamera.x - 310) / px_cm

        #print(f"the real world x coordinates is {x_world}")
        self.x_world = x_world

        return x_world

    def move(self, dir):
        if dir == 'left':
            VideoCamera.x = VideoCamera.x + VideoCamera.rate
            print("going left")

        if dir == 'right':
            VideoCamera.x = VideoCamera.x - VideoCamera.rate
            print("going right")

        if dir == 'up':
            VideoCamera.y = VideoCamera.y - VideoCamera.rate
            print("going up")

        if dir == 'down':
            VideoCamera.y = VideoCamera.y + VideoCamera.rate
            print("going down")

