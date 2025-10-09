import stretch_body.robot
r=stretch_body.robot.Robot()

did_startup=r.startup()
print(f"The Robot is Connected to Hardware: {did_startup}")
is_homed=r.is_homed()
print(f"The Robot is Homed at: {is_homed}")

#basic arm movement up .25 then moves lifter to .5
r.arm.move_to(.25)
r.push_command
#to wait for the robot to complete the task before next
r.wait_command()

#moves lifter
r.lift.move_to(.5)
r.push_command
r.wait_command()

r.end_of_arm.move_to("wrist yaw", 1.57) #pi/2 radians
r.push_command
r.wait_command()

r.end_of_arm.move_to("stretch_gripper",50) #partially open 

#Gets wheel, arm, and lifter position 
# Wheel odometry
print(r.base.status['x'], r.base.status['y'], r.base.status['theta']) # (x meters, y meters, theta radians)

# Arm/lift positions
print(r.arm.status['pos'], r.lift.status['pos']) # (arm meters, lift meters)
