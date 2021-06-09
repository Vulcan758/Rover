from adafruit_servokit import ServoKit
from time import sleep
import numpy as np

kit = ServoKit(channels = 16)

a_1 = 5.25
a_2 = 11.80
a_3 = 7.0
a_4 = 5.25

class HAATy():

    
    theta_1_rad = 0
    theta_2_rad = 0
    theta_3_rad = 0
    theta_4_rad = 0
    

    R0_1 = [[np.cos(theta_1_rad), 0,  np.sin(theta_1_rad)],
            [np.sin(theta_1_rad), 0, -np.cos(theta_1_rad)],
            [0                  , 1,                    0]]

    R1_2 = [[np.cos(theta_2_rad), -np.sin(theta_2_rad), 0],
            [np.sin(theta_2_rad),  np.cos(theta_2_rad), 0],
            [0                  ,  0                  , 1]]

    R2_3 = [[np.cos(theta_3_rad), -np.sin(theta_3_rad), 0],
            [np.sin(theta_3_rad),  np.cos(theta_3_rad), 0],
            [0                  ,  0                  , 1]]

    #R3_4 = [[np.cos(theta_4_rad), -np.sin(theta_4_rad), 0],
    #        [np.sin(theta_4_rad),  np.cos(theta_4_rad), 0],
    #        [0                  ,  0                  , 1]]

    #These are all the rotation matricies where Rn-1_n means the projection of nth frame with respect to the (n-1)th frame
    #They help out in finding the forward kinematics which will further help in finding the orientation of the last 
    #few degrees of freedom
    
    up = [[0,  -1,  0],
          [0,   0, -1],
          [1,   0,  0]]

    down = [[ 0,   1,  0],
            [ 0,   0, -1],
            [-1,   0,  0]]

    zero = [[1,  0,  0],
            [0,  0, -1],
            [0,  1,  0]]

    #These are basically the possible R0_4 matricies we would want. It tells us how our 4th frame (the end-effector)
    #would look with respect to the 0th frame (the base). Pretty much just how the effector pose will be.
    
    def __init__(self, a_1, a_2, a_3, a_4):

        
        
        #initializing the link lengths of the arm
        
        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3
        self.a_4 = a_4

        self.base = 0 #Use theta 1 
        self.shoulder = 1 #Use theta 2 
        self.elbow = 2 #Use theta 3 
        self.wrist = 3 #Use theta 4

        self.start_0 = 90
        self.start_1 = 135
        self.start_2 = -80
        self.start_3 = -80

        
    def check_validity(self, x, y, z):
        
        #The manipulator has a range of movement unfortunately as its links are not of infinite length. This helps in
        #making sure our given coordinates arent anything outside the robots range.
        
        limited_distance = np.sqrt(x**2 + y**2 + z**2)
        print(limited_distance)
        if limited_distance < 11.80:
            raise Exception('Euclidean distance is too small')
            import sys
            sys.exit(1)

            
        if limited_distance > 18.80:
            raise Exception('Euclidiean distance is too big ')
            import sys
            sys.exit(1)

        else:
            print("just right")
            
    def deg(self, theta):
        
        #Pretty self-explanatory, it changes angles from radians to degrees as numpys trigonometric functions returns
        #angle values in radians
        
        return theta * (180/np.pi)

    def rad(self, theta):
        
        #Similar to the above, it changes degrees to radians if needed. 
        
        return theta * (np.pi/180)

    def start_position(self):
        #initial position

        kit.servo[0].angle = self.start_0
        kit.servo[1].angle = self.start_1
        kit.servo[2].angle = - self.start_2 + 90
        kit.servo[3].angle = self.start_3 + 90

    def smoother(self, end_angle, time_, joint):
        #smoother and slower rotations

        if joint == 2:
            actual_end = - end_angle + 90
        elif joint == 3:
            actual_end = 90 + end_angle
        else:
            actual_end = end_angle

        start_angle = kit.servo[joint].angle 
        incmove = (actual_end - start_angle)/100.0
        inctime = time_/100.0
        for x in range(100):
            kit.servo[joint].angle = start_angle + x * incmove
            sleep(inctime)

    def back_to_start(self):
        self.smoother(90, 0.5, self.wrist)
        self.smoother(90, 0.5, self.elbow)
        self.smoother(90, 0.001, self.shoulder)
        print("Going behind up")

        self.smoother(0, 0.5, self.wrist)
        self.smoother(0, 0.5, self.elbow)
        self.smoother(90, 0.5, self.shoulder)
        print("Zero stage")

        self.smoother(self.start_0, 0.5, self.base)
        self.smoother(self.start_1, 0.5, self.shoulder)
        self.smoother(self.start_2, 0.5, self.elbow)
        self.smoother(self.start_3, 0.5, self.wrist)
        print("Stablelized")

    
    def first_3Degrees(self, x, y, z, config):
        
        #This method finds the inverse kinematics of the manipulator by making calculations to find the angle for the 
        #first three joints. The robot will be in an elbow up orientation meaning the arm will look convex from the side
        #I plan on changing combine this method and the method following it so I can get my bot to move an exact location/
        
        theta_1_rad = np.arctan2(y, x) #1
        theta_1 = self.deg(theta_1_rad)

        r_1 = np.sqrt(y**2 + x**2) #2

        r_3 = z - self.a_1 #3

        r_2 = np.sqrt(r_3**2 + r_1**2) #4

        B_rad = np.arctan2(r_3, r_1) #5
        B = self.deg(B_rad)

        l = r_2 ** 2 - self.a_2 ** 2 - self.a_3 ** 2
        k = - 2 * self.a_2 * self.a_3 
        a_rad = np.arccos( l / k ) #6
        a = self.deg(a_rad)


        theta_3_rad = -(np.pi - a_rad) #7
        theta_3_rad__ = -1 * theta_3_rad #8
        theta_3 = self.deg(theta_3_rad)

        o = self.a_3 * np.sin(theta_3_rad__)
        p = (self.a_3 * np.cos(theta_3_rad__)) + self.a_2
        phi_rad = np.arctan2(o, p) #9
        phi = self.deg(phi_rad)


        theta_2_rad = phi_rad + B_rad #10
        theta_2 = self.deg(theta_2_rad)

        if theta_1_rad > np.pi:
            theta_1_rad = np.pi

        if theta_2_rad > np.pi:
            theta_2_rad = np.pi

        if theta_1_rad < 0:
            theta_1_rad = 0

        if theta_2_rad < 0:
            theta_2_rad = 0

        if theta_3_rad > np.pi/2:
            theta_3_rad = np.pi/2

        if theta_3_rad < -np.pi/2:
            theta_3_rad = -np.pi/2  
    

        return theta_1_rad, theta_2_rad, theta_3_rad
    
    def fourth_Degree(self, config):
        
        #for manipulator kinematics, as far as I know, the first 3 joints are usually for positioning the arm while 
        #the joints after that are for the orientation of the end-effector. Since my bot has 4 degrees of freedom,
        #the 4th joint is concerned with the orientation of my end-effector. The possible orientations for the 4th
        #joint is restricted within a single axis. So instead of using the complicated matricies to figure out what 
        #orientation I want my bot, I could've just said up = 90, down = -90, zero = 0. Buuut that really just makes
        #things too easy so here we are.
        
        R0_2 = np.dot(self.R0_1, self.R1_2)
        R0_3 = np.dot(R0_2, self.R2_3)
        
        #R0_3 = R0_1 x R1_2 x R2_3 
        
        R0_3Inverse = np.linalg.inv(R0_3)
        
        #you'll see why I did this later
        
        if config == "up":
            R0_4 = self.up
        elif config == "down":
            R0_4 = self.down
        elif config == "zero":
            R0_4 = self.zero
        
        R3_4_use = np.dot(R0_3Inverse, R0_4)
        
        #If you scroll up you'll see R3_4 commented out. Its basically the template of what R3_4 wouldve looked like.
        #Notice R3_4 only consists of theta_4_rad. This is gonna help find theta_4_rad. 
        
        #R0_4 = R0_3 x R3_4
        #So rearrange making R3_4 the subject and you get a matrix for R3_4
        
        theta_4_rad_1 = np.arccos(R3_4_use[0][0])
        theta_4_rad_2 = np.arcsin(-(R3_4_use[0][1]))
        theta_4_rad_3 = np.arcsin(R3_4_use[1][0])
        theta_4_rad_4 = np.arccos(R3_4_use[1][1])
        
        #the fourth dof has a range of possible solutions so I'll be using the one that will best suits it by using 
        #a pretty simple algorithm(?) you'll see below. 

        theta_4_possible = [theta_4_rad_1, theta_4_rad_2, theta_4_rad_3, theta_4_rad_4]
        
        if config == "up":
        
            for y in theta_4_possible:
                if y > 90 and y < 0:
                    theta_4_possible.remove(y)

            theta_4_rad = max(theta_4_possible)

        elif config == "down":

            for y in theta_4_possible:
                if y > 0 and y < -90:
                    theta_4_possible.remove(y)

            theta_4_rad = min(theta_4_possible)

        elif config == "zero":
            

            theta_4_rad = theta_4_possible[0]

        return theta_4_rad
    

def inputUser():
    
    x = float(input("Enter x-coordinate "))
    y = float(input("Enter y-coordinate "))
    z = float(input("Enter z-coordinate "))
    config = input("Set end-effector configuration ")

    return x, y, z, config

def initialization():
    kit.servo[0].angle = 90
    kit.servo[1].angle = 135
    kit.servo[2].angle = 170
    kit.servo[3].angle = 10

def smoother(end_one, delta, joint):
    if joint == 2:
        end = - end_one + 90
    elif joint == 3:
        end = 90 + end_one
    else:
        end = end_one
        
    start = kit.servo[joint].angle 
    incmove = (end - start)/100.0
    inctime = delta/100.0
    for x in range(100):
        kit.servo[joint].angle = start + x * incmove
        sleep(inctime)



if __name__ == '__main__':

    arm = HAATy(a_1, a_2, a_3, a_4)
    t = 0.5

    while True:

        #The main loop
        
        arm.start_position()
        x, y, z, config = inputUser()
        arm.check_validity(x, y, z)
        theta_1_rad, theta_2_rad, theta_3_rad = arm.first_3Degrees(x, y, z, config)
        theta_1, theta_2, theta_3 = arm.deg(theta_1_rad), arm.deg(theta_2_rad), arm.deg(theta_3_rad)
        theta_4_rad = arm.fourth_Degree(config)
        theta_4 = arm.deg(theta_4_rad)

        thetas = [theta_1, theta_2, theta_3, theta_4]
        limbs = [arm.base, arm.shoulder, arm.elbow, arm.wrist]
        print(limbs)
        print(thetas)
        for joints in range(len(limbs)):
            arm.smoother(thetas[joints], t, limbs[joints])

        sleep(2)

        thetas = []
        limbs = []
        
