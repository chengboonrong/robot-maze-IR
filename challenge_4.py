from line_tracker import line_tracker
from motor import motor
import time
from rules import LHR, back_travel

### Alphabot-PiZero-00  ###
address = "192.168.0.100" 
###########################
mot = motor(address)
lt = line_tracker(address)
lt.start()

############################
th_0 = 200  # left most
th_1 = 400  # left
th_2 = 500  # middle
th_3 = 400  # right
th_4 = 300  # right most
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

 
        if lt.data[2] > th_2:

                if lt.data[3] < th_3 or lt.data[4] < th_4:
                    print(lt.data, 'slightly right')
                    mot.command("right", 4, 0.3)

                elif lt.data[1] < th_1 or lt.data[0] < th_0:
                    print(lt.data, 'slightly left')
                    mot.command("left", 4, 0.3)


        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 5, 0.4)

        # delay
        time.sleep(0.5)

        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2:
            print(lt.data, 'stop and turn left')
            mot.command("forward", 5, 0.5)
            mot.command("left", 8, 0.6)
            time.sleep(0.5)
            # append L
            actions.append("L")
            checkPoint(actions, checkpoints)

        # when met a right corner or T-junction at right
        elif (lt.data[3] < th_3 and lt.data[4] < th_4) and (lt.data[0] > th_0 and lt.data[1] > th_1):
            mot.command("forward", 5, 0.5)
            # a right corner, turn right
            if lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                mot.command("right", 8, 0.6)
                actions.append("R")
                checkpoints(actions, checkpoints)
            # a T-junction
            else: 
                print(lt.data, 'junction at right and speed up')
                # append S
                actions.append("S")
                checkPoint(actions, checkpoints)

        # all white
        elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
            print(lt.data, 'stop and U-Turn')
            mot.command("right", 8, 0.6)
            time.sleep(0.5)
            # append B
            actions.append("B")
            checkPoint(actions, checkpoints)

        # all black
        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            # forward and check if still black
                mot.command("forward", 5, 0.4)
                # if still black then reached END
                if lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[
                    4] < th_4:
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

    while end:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        # delay
        time.sleep(0.5)

        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 5, 0.4)

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
            elif checkpoints[-1] == "R":
                print(lt.data, 'stop and turn right')
                mot.command("forward", 5, 0.4)
                mot.command("right", 8, 0.6)
                actions.pop()
            elif checkpoints[-1] == "S": 
                print(lt.data, 'stop and go straight')
                mot.command("forward", 7,0.4)
                actions.pop()

        # delay
        time.sleep(0.5)

        # all black
        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            print(lt.data, 'Reach END')
            end = False


except KeyboardInterrupt:
    lt.stop()
    mot.stop()