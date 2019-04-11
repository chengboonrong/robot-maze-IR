from line_tracker import line_tracker
from motor import motor
import time
from rules import LHR, back_travel

### Alphabot-PiZero-06  ###
address = "192.168.0.106" 
###########################
mot = motor(address)
lt = line_tracker(address)
lt.start()

############################
th_0 = 450  # left most
th_1 = 450  # left
th_2 = 450  # middle
th_3 = 450  # right
th_4 = 450  # right most
############################

start = True
end = False

# Left_hand_rule, so no turn right
actions = []
checkpoints = []

try:

    while start:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        
        # delay
        time.sleep(0.5)

        if lt.data[3] < th_3 or lt.data[4] < th_4:
            print(lt.data, 'slightly right')
            mot.command("right", 4, 0.3)

        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 4, 0.4)

        if lt.data[1] < th_1 or lt.data[0] < th_0:
            print(lt.data, 'slightly left')
            mot.command("left", 4, 0.3)

        # when met a right corner or T-junction at right
        # elif (lt.data[3] < th_3 and lt.data[4] < th_4) and (lt.data[0] > th_0 and lt.data[1] > th_1):
        #     mot.command("forward", 5, 0.5)
        #     print(lt.data, 'junction at right and speed up')
        #     # append S
        #     actions.append("S")
        #     LHR(actions, checkpoints)


        elif lt.data[0] < th_0 or (lt.data[1] < th_1 and lt.data[2] < th_2):
            print(lt.data, 'stop and turn left')
            # mot.command("forward", 5, 0.5)
            mot.command("left", 8, 0.6)
            # append L
            actions.append("L")
            LHR(actions, checkpoints)

        # all white
        elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
            print(lt.data, 'stop and U-Turn')
            mot.command("right", 8, 0.5)
            # append B
            actions.append("B")
            LHR(actions, checkpoints)

        elif (lt.data[3] < th_3 and lt.data[4] < th_4) and (lt.data[0] > th_0 and lt.data[1] > th_1):
            mot.command("forward", 5, 0.4)
            # this condition utk pastikan jika terlajak yang tengah sensor 0 dan 1 masih ada utk stop
            if lt.data[2] > th_2:
                print(lt.data, "turn right")
                # check if the turn right a quite hard so need to decrease the duration[turn right sikit-sikit]
                mot.command("right", 8, 0.5)
                print(lt.data, 'find route and go straight')
                # append R
                actions.append("R")
                LHR(actions, checkpoints)
            else: 
                mot.command("forward", 8, 0.5)
                print(lt.data, 'junction at right and speed up')
                # append S
                actions.append("S")
                LHR(actions, checkpoints)


        # all black
        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            # forward and check if still black
            mot.command("forward", 5, 0.4)
            time.sleep(0.5)
            # if still black then reached END
            if lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                print(lt.data, 'Reach END')
                while lt.data[0] < th_0 and lt.data[4] < th_4:
                    mot.command("backward", 5, 0.4)
                    # at least 90 degree of robot will rotate to the right
                    mot.command("right", 10, 0.8)
            
            start = False
            end = True
            print(actions)
            print(checkpoints)
            time.sleep(1)

        time.sleep(0.2)
        print(actions)

    back_travel(actions)
    while end:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        # delay
        time.sleep(0.5)

        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 6, 0.5)

        elif lt.data[2] > th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            print(lt.data, 'slightly right')
            mot.command("right", 4, 0.3)

        elif lt.data[2] > th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
            print(lt.data, 'slightly left')
            mot.command("left", 4, 0.3)

        # when met a corner or T-junction
        elif (lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] > th_0) or (lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[4] > th_4):
            # take actions from checkpoints
            time.sleep(0.5)
            if actions[-1] == "L":
                print(lt.data, 'stop and turn left')
                mot.command("forward", 5, 0.4)
                mot.command("left", 8, 0.6)
                actions.pop()
            elif actions[-1] == "R":
                print(lt.data, 'stop and turn right')
                mot.command("forward", 5, 0.4)
                mot.command("right", 8, 0.6)
                actions.pop()
            elif actions[-1] == "S": 
                print(lt.data, 'stop and go straight')
                mot.command("forward", 7,0.4)
                actions.pop()

        # delay
        time.sleep(0.5)

        # all white
        if lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
            print(lt.data, 'Reach END')
            end = False


except KeyboardInterrupt:
    lt.stop()
    mot.stop()