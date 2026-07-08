## Domain description

A robot with two arms (left_arm and right_arm) is tasked with threading a needle through a set of rings in a specified sequence before finally placing the needle on a goal position. Threading the needle can be accomplished by first moving the needle to the desired rings and then handing over the needle to the free arm. Before handing over, picking up or placing the needle, the arm always has to first move to the required position (needle/ring/goal). Note, that when transferring the needle from one arm to the other, it should always be grasped by at least one arm so that it does not get dropped.

The actions available to the robot are:
- move
    - Moves the arm to a specified position (needle or ring)
- pick
    - Closes the arms gripper at the current position
- place
    - Opens the arms gripper at the current position
