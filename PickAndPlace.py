#Fully Functional Codebase-Need to figure out how to start the robot and have it run this. . . maybe a huge wait time after starting to unplug everything
#could also optimize the wait time between actions, shorter actions don't need to have as much wait priority as longer actions
#finally, make sure to keep wires away from base 


#imports
import stretch_body.robot
import stretch_body.base
import time
robot = stretch_body.robot.Robot()
robot.startup()

#to define the zero position: 
#stretch_robot_home.py #sets up the normalized height

#will use an absolute difference methodologys, so all of the position of the objects will be defined with respect to the origin 

#distance from initial position of bottle to final position of the bottle is .361 m
#distance from start of robot to the start of table is .77 m
#distance from the start of the robot to the start of the hand is .20 m
#distance from the start of the table to the start of the bottle is .05 m
#distance from the table to the ground is .72 m
#distance from the arm to the ground is .285 m (might not be the case after )
#need to get the distance from the robot to the ground and subtract that off of the arm_height_dist
r_robot_table=.77
r_robot_hand=.2
r_table_bottle=.05
r_robot_ground=.155 #now the zero point of the robot is the top of the stopper

r_bi_bf=.361
r_table_ground=.77

base_forward_dist=r_robot_table-r_robot_hand+r_table_bottle
arm_forward_dist=r_bi_bf
arm_height_dist=r_robot_table+.2 -r_robot_ground #add tolerance, also make sure that it is the height relative to the robot in which the arm moves up


#moves the base of the robot a specified distance forward, not to an absolutely defined position
def base_move (distance):
    robot.base.translate_by(distance)
    robot.push_command()
    print(f"base at {distance}")

#moves the arm of the robot up to a specified height, this is an absolutely defined position which is defined wrt the robot's body frame
def arm_up (distance_up):
    #maximum distance is 1.1 m
    robot.lift.move_to(distance_up)
    robot.push_command()
    print(f"arm at {distance_up} upwards")

#moves the arm of the robot to a specified distance forward, this is an absolutely defined position wrt the robot's body frame
def arm_forward (distance_forward):
    #maximum distance forward is .52m
    robot.arm.move_to(distance_forward)
    robot.push_command()
    print(f"arm at {distance_forward} forward")

#changes the gripper amount, this closes it about 50% from start 
def gripper_open (amount):
    #closes about half-way
    if amount!=90:
        amount=-50                                                                 
    robot.end_of_arm.move_to("stretch_gripper",amount)
    print(f"gripper at {amount}")  

def base_rotate (rad_angle):
    robot.base.rotate_by(rad_angle)
    robot.push_command()
    print(f"base rotated by {rad_angle} radians")                   

#defines the zero position of the robot after the height has been normalized 
arm_up(.25)
arm_forward(0)
gripper_open(90)
time.sleep(7.5)


#movement parttern should be arm_up [wait], base_move [wait], base_rotate [wait], gripper open [wait]. . . etc (concern is that with rotation the base won't be alligned, then we can just pivot forward or backwards)
#need to take the robot's arm up higher, then turn, then lower, also maybe only .05 
height_tolerance=.2
arm_up(arm_height_dist+height_tolerance)
time.sleep(7.5)
base_move(base_forward_dist)
time.sleep(7.5)
base_rotate(1.57)
time.sleep(7.5)
base_move(.05) #to make up for angular rotation putting the robot off-centered
time.sleep(7.5)

#should be over top of the bottle
height_tolerance_2=.05 #should be .05 
arm_up(arm_height_dist-height_tolerance_2) #goes a little bit further down on the bottle to be more secutre
time.sleep(7.5)
gripper_open(-50)
time.sleep(7.5)
arm_up(arm_height_dist+.05) 
time.sleep(7.5)
arm_forward(arm_forward_dist)
time.sleep(7.5)
arm_up(arm_height_dist -.035-height_tolerance_2)
time.sleep(7.5)
gripper_open(90)        

""""
#common sense solution:

#to move the arm the right height
arm_up(arm_height_dist)

#to move the base the correct amount forward
base_move(base_forward_dist)

#to rotate the arm to the right orientation, facing the bottle (-90 degrees)
robot.base.rotate_by(-1.57)

gripper_open(-50)

#moves the arm up a little bit so it doesn't scrape the table
arm_up(arm_height_dist+.05) #moves the arm up before moving forward

#moves the arm forward to the location of the final holding spot
arm_forward(arm_forward_dist)

#drops the bottle to the correct height
arm_up(arm_height_dist -.05)

#opens the gripper
gripper_open(90)
"""
