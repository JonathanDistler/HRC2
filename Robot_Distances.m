in_to_m=1/39.37007874015748;

%measured in [in]
r_box_edge=19.75; 
r_edge_pole=5/8; 
r_telescope_edge=11+5/8; 
r_second_telescope_edge=9+5/8; 

%Had wanted a distance of .25 m
r_box_edge=r_box_edge*in_to_m;
r_edge_pole=r_edge_pole*in_to_m;
r_telescope_edge=r_telescope_edge*in_to_m;
r_second_telescope_edge=r_second_telescope_edge*in_to_m;
arm_total=r_box_edge+r_edge_pole;


%Measured from the projected plane of the front of the wheel
test_1=39+1/8;
test_2=39+1/8;
test_3=38+15/16;
Tests=[test_1,test_2,test_3];

average_distance=mean(Tests)*in_to_m;
%Average percentage error is .78%, very negligible, will not consider in
%testing
percent_error=(abs(average_distance-1)/1)*100;


%Had wanted a distance of 1m
r_bottomrig_toprobot=39.25*in_to_m; 
r_bottomrig_ground=(42.25+3.5)*in_to_m;
r_toprig_toprobot=r_bottomrig_toprobot+(2+7/8)*in_to_m;
r_stopper_toprobot=6.25*in_to_m; %might be measured relative to the stopper

r=abs(r_bottomrig_toprobot-r_bottomrig_ground);
disp(r+r_stopper_toprobot);


%Testing to see which point is the reference that goes up the correct
%amount
amount=.2;
stopper_top=(7+15/16-1.75)*in_to_m;

bottomplaque_top=(7+15/16)*in_to_m;
bottomplaque_stopper=bottomplaque_top-stopper_top;

middleplaque_top=(8.5)*in_to_m;
middleplaque_stopper=middleplaque_top-stopper_top;

topplaque_top=(6.5+3.5)*in_to_m;
topplaque_stopper=topplaque_top-stopper_top;

bottomarm_top=(5.5+3.5)*in_to_m;
bottomarm_stopper=bottomarm_top-stopper_top;

toparm_top=(6.75+3.5)*in_to_m;
toparm_stopper=toparm_top-stopper_top;

distances=[bottomplaque_top,bottomplaque_stopper,middleplaque_top,middleplaque_stopper,topplaque_top,topplaque_stopper,bottomarm_top,bottomarm_stopper,toparm_top,toparm_stopper];
disp(distances-amount);

%Put in a test height of .5m, then measured the bottom of the arm to the
%top of the base, and the top of the arm to the top of the base, as well as
%athe extrapolated middle of the arm

toparm_toprobot=(18+9/16+3.5)*in_to_m;
bottomarm_toprobot=(16+15/16+3.5)*in_to_m;

middledist=(toparm_toprobot-bottomarm_toprobot)/2;

midarm_toprobot=bottomarm_toprobot+middledist;

actuator_ground=(20+1/8+3.5)*in_to_m;
toprobot_ground=(2.75+3.5)*in_to_m;
actuator_toprobot=actuator_ground-toprobot_ground;

%Closest!
disp(bottomarm_toprobot-.5*in_to_m)

%End-effector ground distance
endeffector_ground=actuator_ground-3*in_to_m;
disp(endeffector_ground)

%IMPORTANT%
%For the global frame, the bottom of the plaque is the IMU that measures
%distance from the top of the robot
%So, dictating .25 m moves the bottom of the plaque .25 m from the top of
%the robot, which means an additional .1588 m from teh ground

%Or, the end effector is the specified distance +.0239 m off of the ground,
%so if you specify .35m, the end effector is .3739 m off of the ground

