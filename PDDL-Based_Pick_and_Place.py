
#Goal of this code is to take the output of a PDDL and convert that to an action in the Stretch Robot's Action space
#Need to map verb to action

#Using an absolute difference methodology to control where the robot moves 
#imports
import stretch_body.robot
import stretch_body.base
import time
robot = stretch_body.robot.Robot()
robot.startup()

#stretch_robot_home.py #sets up the normalized height
#need to define locations and heights in domain.pddl file

#outputs from the PDDL 
output1="drive-robot stretch a b"
output2="load-robot bottle stretcharm stretch b heightlo"
output3="drive-robot-package stretch b tableloc bottle"

strings=[output1, output2, output3]

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

#defines verbs and locations from PDDL output
def define_verb(pddl_output):
    #finds the verb
    stringval=pddl_output
    dash=stringval.find("-")
    verb=stringval[0:dash]

    #finds the locations from the strings based on spaces
    positions=[]

    for i in range(len(stringval)-1, -1, -1):
        if stringval[i] == " ":
            positions.append(i)

    #return a string array with the locations and actions
    index1=positions[0]
    index2=positions[1]
    loc2=stringval[index1:]
    loc1=stringval[index2:index1]

    data=[verb,loc1,loc2]
    return(data)

#need to robustify the positions of drive -ie a tuple such as (x,y) then can drive x turn 90 -make up for turn with interpolation, then drive to y then turn again and make up for it 4
#or, just define another positional element in the PDDL (one for x, y, z)
def verb_map(arr):
    #maps the drive verb to position start and finish
    if arr[0]=="drive":
        position_current=arr[1]
        position_final=arr[2]
        delta_dist=position_final-position_current
        base_move(delta_dist) #moves the base a specific distance
        print(f"drive from {position_current} to {position_final}")

    #maps load verb to height start and finish
    elif arr[0]=="load":
        height_current=arr[1]
        height_final=arr[2]
        delta_height=height_final-height_current
        arm_up(delta_height+.05) #moves the arm up a specific distance
        print(f"load from {height_current} to {height_final}")

###Double Check Method###
#assume everything is orthogonal, this will keep the center of the robot along the same axis after a turn
offset_distance=0.05715; #measured empirically for a 90 degree turn, had been using .05 m 
def turn_interp(angle):
    if angle!=90: 
        angle=angle%90 #in the case angle is 180 degrees

    distance=0+(offset_distance/90)*(angle) #from interpolation formula, gives how much the base needs to move to counteract center of mass offset
    #turns the base by the "angle" amount degrees CCW
    base_rotate(angle)
    #moves the base forward by the amount at which the center of mass if offset
    base_move(distance)





    
