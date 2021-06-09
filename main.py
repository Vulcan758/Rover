from roverLibs.CamWebInterface import VideoCamera
from roverLibs.RoverBase import RoverBase
from flask import Flask, Response, request, redirect, render_template
from roverLibs.HAATyDummy import HAATyDummy
from roverLibs.HAATyIKv1 import HAATy
import numpy as np 
from time import sleep
from adafruit_servokit import ServoKit

a_1 = 5.25
a_2 = 11.80
a_3 = 7.0
a_4 = 5.25

app = Flask(__name__)
#cam = VideoCamera()
car = RoverBase()


''' 
 THIS IS THE TEST VERSION
class ArmDummy(HAATyDummy):

    def rotate(self, x, y, z, config):
        theta_1_r, theta_2_r, theta_3_r = self.first_3Degrees(x, y, z, config)
        theta1, theta2, theta3 = self.deg(theta_1_r), self.deg(theta_2_r), self.deg(theta_3_r)
        theta_4_r = self.fourth_Degree(config)
        theta4 = self.deg(theta_4_r)

        print('theta 1 ' + str(theta1))
        print('theta 2 ' + str(theta2))
        print('theta 3 ' + str(theta3))
        print('theta 4 ' + str(theta4))

        print("Positions found!")

        sleep(1)

        thetas = [theta1, theta2, theta3, theta4]
        limbs = [self.base, self.shoulder, self.elbow, self.wrist]
        
        for joints in range(len(limbs)):
            print("Servo " + str(limbs[joints]) + " has moved " + str(thetas[joints]))

        sleep(2)

    def verifier(self, x, y, z):

        limited_distance__ = np.sqrt(x**2 + y**2 + z**2)
        print("Euclidean distance is " + str(limited_distance__))

        if limited_distance__ < 9.75:
            return False

        if limited_distance__ > 26.0:
            return False

        else:
            return True

'''
class Arm(HAATy):

    def rotate(self, x, y, z, config):
        theta_1_r, theta_2_r, theta_3_r = self.first_3Degrees(x, y, z, config)
        theta1, theta2, theta3 = self.deg(theta_1_r), self.deg(theta_2_r), self.deg(theta_3_r)
        theta_4_r = self.fourth_Degree(config)
        theta4 = self.deg(theta_4_r)

        print("Positions found!")

        self.start_position()
        sleep(1)
        print("Beginning kinematics")

        thetas = [theta1, theta2, theta3, theta4]
        limbs = [self.base, self.shoulder, self.elbow, self.wrist]
        
        for joints in range(len(limbs)):
            self.smoother(thetas[joints], 1, limbs[joints])
            print(thetas[joints])
            print(limbs[joints])

        sleep(2)
        self.back_to_start()

    def verifier(self, x, y, z):

        limited_distance = np.sqrt(x**2 + y**2 + z**2)
        print(limited_distance)

        if limited_distance < 9.75:
            return False

        if limited_distance > 26.0:
            return False

        else:
            return True

arm = Arm(a_1, a_2, a_3, a_4)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        key = request.form['key']
        print(key)

    return render_template('homeTest.html')

@app.route('/cam', methods=['POST', 'GET'])
def cam():
#    cam = VideoCamera()
    if request.method == 'POST':
        key = request.form['key']
        print(key)
        if key == 'enter':
            y = CamModule.cam.get_y_coords()
            x = CamModule.cam.get_x_coords()
            print('X-Coordnate is {}'.format(x))
            print('and Y-Coordinate is {}'.format(y))
        else:
            CamModule.cam.move(key)

    return render_template('cam.html')

@app.route('/roverBase', methods = ['POST', 'GET'])
def roverBase():
    #car = roverbaseDummy()
    if request.method == 'POST':
        key = request.form['key']
        print(key)
        if key == 'enter':
            car.reset()
        else:
            car.move(key)

    return render_template('roverBase.html')

@app.route('/ikinematics', methods = ['POST', 'GET'])
def ikinematics():
    validity = None
    if request.method == 'POST':
        x_s = request.form['x_coordinates']
        y_s = request.form['y_coordinates']

        x = float(x_s)
        y = float(y_s)
        z = 5.0
        config = request.form['config']
        validity = arm.verifier(x, y, z)

        if validity == True:
            arm.rotate(x, y, z, config)

        else:
            print("Not a valid range, change coordinates")


        print(str(x) + " is x-coordinates")
        print(str(y) + " is y-coordinates")
        print(config)
    
    return render_template('ikinematics.html')

@app.route('/fkinematics', methods = ['POST', 'GET'])
def fkinematics():
    if request.method == 'POST':
        base_s = request.form['base']
        shoulder_s = request.form['shoulder']
        elbow_s = request.form['elbow']
        wrist_s = request.form['wrist']

        base = float(base_s)
        shoulder = float(shoulder_s)
        elbow = float(elbow_s)
        wrist = float(wrist_s)

        angles = [base, shoulder, elbow, wrist]
        for i in range(len(angles)):
            arm.smoother(angles[i], 0.5, i)
        sleep(2)
        arm.back_to_start()

    return render_template('fkinematics.html')
    
class CamModule():

    cam = None

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        CamModule.cam = VideoCamera()
        return Response(CamModule.gen(CamModule.cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
