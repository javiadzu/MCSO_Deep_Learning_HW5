import pystk
import numpy as np


Story = []
def control(aim_point, current_vel):
    """
    Set the Action for the low-level controller
    :param aim_point: Aim point, in screen coordinate frame [-1..1]
    :param current_vel: Current velocity of the kart
    :return: a pystk.Action (set acceleration, brake, steer, drift)
    """
    action = pystk.Action()

    """
    Your code here
    Hint: Use action.acceleration (0..1) to change the velocity. Try targeting a target_velocity (e.g. 20).
    Hint: Use action.brake to True/False to brake (optionally)
    Hint: Use action.steer to turn the kart towards the aim_point, clip the steer angle to -1..1
    Hint: You may want to use action.drift=True for wide turns (it will turn faster)
    """
    p_aim_point =0
    if(len(Story)>2):
         p_aim_point = Story[-1]
    Story.append(aim_point[0])
    terminal_vel = 25
   # print(aim_point)
    steer_angle = np.clip(aim_point[0], -1, 1) 
    Dir = steer_angle/abs(steer_angle)
    actions = 'o'
    p_vel = 0
   # print(Dir)

    if (np.abs(steer_angle) > 0.85 and current_vel > 10) :
        action.acceleration = 0 #Return
        action.brake = True
        action.steer = Dir
        action.drift = True
        actions = 'a'
        

    elif (np.abs(steer_angle) > 0.9 and current_vel < 5 ):
        action.acceleration = 1 #Return
        action.steer = Dir
        actions = 'b'

    elif ( np.abs(steer_angle) < 0.1 ):
        action.acceleration = 1 #Return
        action.brake = False
        action.nitro = True
        actions = 'N'    

    elif ( np.abs(steer_angle) < 0.3 and current_vel < terminal_vel):
        action.acceleration = 1 #Return
        actions = 'c'

    elif (np.abs(steer_angle) > 0.7 and current_vel > 15 and (abs(p_aim_point - steer_angle)>0.04)):
        action.acceleration = 0 #Return
        action.brake = True
        action.steer = Dir
        actions = 'd'

        
    elif ( np.abs(steer_angle) > 0.45 and current_vel > 15 and (abs(p_aim_point - steer_angle)>0.03)):
        action.acceleration = 0 #Return
        action.steer = Dir
        actions = 'e'


    elif ( np.abs(steer_angle) < 0.4 and current_vel < terminal_vel ):
        action.acceleration = 1 #Return
        action.brake = False
        action.steer = steer_angle*2
        actions = 'f'


    elif ( np.abs(steer_angle) < 0.1 ):
        action.acceleration = 1 #Return
        action.brake = False
        action.nitro = True
        actions = 'N'

    elif ( np.abs(steer_angle) > 0.5 and current_vel > 15 and (abs(p_aim_point - steer_angle)>0.03)):
        action.acceleration = 0 #Return
        action.steer = Dir
        actions = 'g'

    
    elif np.abs(steer_angle) > 0.7 and  current_vel < 11:
        action.acceleration = 0 #Return
        action.steer = Dir
        actions = 'h'

    elif np.abs(steer_angle) > 0.7 and  current_vel < 4:
        action.acceleration = 1 #Return
        action.steer = Dir
        actions = 'h'


    elif np.abs(steer_angle) > 0.7:
        action.acceleration = 0 #Return
        action.brake = True
        action.steer = Dir
        actions = 'h'
        
        
        
    elif np.abs(steer_angle) > 0.4:
        action.brake = False
        if current_vel < 20:
            action.acceleration = 1
        action.steer = steer_angle*2
        actions = 'j'
    else: 
        if current_vel > terminal_vel:
            action.acceleration = 0
            action.steer =  Dir
        else:
            action.acceleration = 1
            action.nitro = True
        actions = 'k'
    #print("angle: " + str(steer_angle),"\t cur vel: " +str(current_vel),"\t cdif: " +str(abs(p_aim_point - steer_angle)))#, actions)
    
    return action


if __name__ == '__main__':
    from .utils import PyTux
    from argparse import ArgumentParser

    def test_controller(args):
        import numpy as np
        pytux = PyTux()
        for t in args.track:
            steps, how_far = pytux.rollout(t, control, max_frames=1000, verbose=args.verbose)
            print(steps, how_far)
        pytux.close()


    parser = ArgumentParser()
    parser.add_argument('track', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    test_controller(args)
