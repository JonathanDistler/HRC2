#Combined code base from previous PDDL_Output, String_to_Pos, and Path_Drive files
#Goal of this code is to take the output of a PDDL and convert that to an action in the Stretch Robot's Action space

#Using an absolute difference methodology to control where the robot moves 
#imports
import stretch_body.robot
import stretch_body.base
import time
robot = stretch_body.robot.Robot()
robot.startup()


#outputs from the PDDL 
output1="drive-robot stretch a b"
output2="load-robot bottle stretcharm stretch b heightlo"
output3="drive-robot-package stretch b tableloc bottle"

strings=[output1, output2, output3] #very much subject to change

strs=["a","b","tableloc"] #from PDDL output, subject to change
locs=[[0,0],[5,5],[5,25]] #arbitrary array of tuples corresponding to each string's real-world-global location

####Code Base Mapping Robot Positional Goals to Movement Outputs####
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


#assume everything is orthogonal, this will keep the center of the robot along the same axis after a turn
def turn_interp(angle):
    offset_distance=0.05715; #measured empirically for a 90 degree turn, had been using .05 m 
    if angle!=90 or angle!=-90: 
        angle=angle%90 #in the case angle is 180 degrees

    distance=0+(offset_distance/90)*(angle) #from interpolation formula, gives how much the base needs to move to counteract center of mass offset
    #turns the base by the "angle" amount degrees CCW
    base_rotate(angle)
    #moves the base forward by the amount at which the center of mass if offset
    base_move(distance)

####Code Base Mapping PDDL String Outputs to Locations####

#Goal of this script is to assign an absolute location to each string
# i.e. "a" represents a specific table, which is at a specific location

def string_to_seq (current, final):
    #finds the appropriate index of each position
    current_idx=find_string(strs,current)
    final_idx=find_string(strs,final)
    if current_idx==-1 or final_idx==-1:
        return("Error, not a valid location")
    
    #maps the index of each position to a position
    current_pos=locs[current_idx]
    final_pos=locs[final_idx]
    return(current_pos,final_pos)


#function to find a specific string in an array, used to search for locations in the state-space 
def find_string (arr,str):
    for i in range(len(arr)):
        if (arr[i]==str):
            return(i)
    else:
        return(-1)
    
####Code Base Mapping PDDL Locations to Robot Movements####
#Goal of this code is to take two positions [xi,yi] and [xf,yf] and drive from the start to the finish with the Stretch robot

def path_drive(current_pos_arr,final_pos_arr):
    #pulls out the xi, xf, yi, yf from the arrays provided by the PDDL output
    xi=current_pos_arr[0]
    xf=final_pos_arr[0]
    yi=current_pos_arr[1]
    yf=final_pos_arr[1]

    #gets relative difference between the components, assumes robot is facing forward in the y direction
    dx=xf-xi
    dy=yf-yi

    #moves forward according to the global coordinate system
    base_move(dy)
    #turns 90 degrees and then makes up for offset with recalibration
    turn_interp(90)
    #moves sideways (x-direction) from previous perspective
    base_move(dx)
    #turns -90 degrees and gets back to the original orientation at the new position
    turn_interp(-90)
