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

            while lt.data[2] > th_2 and condition_2:

                if lt.data[2] > th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                    print(lt.data, 'slightly right')
                    mot.command("right", 4, 0.3)

                elif lt.data[2] > th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
                    print(lt.data, 'slightly left')
                    mot.command("left", 4, 0.3)


        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 5, 0.4)

        # delay
        time.sleep(0.5)

        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2:
            print(lt.data, 'stop and turn left')
            mot.command("left", 8, 0.6)
            mot.command("forward", 5, 0.4)
            time.sleep(0.5)
            print(lt.data, 'find route and go straight')
            # append L
            actions.append("L")
            checkPoint(actions, checkpoints)

        # when met a right corner or T-junction at right
        elif (lt.data[3] < th_3 and lt.data[4] < th_4) and (lt.data[0] > th_0 and lt.data[1] > th_1):
            mot.command("forward", 5, 0.4)
            # a right corner, turn right
            if lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                mot.command("right", 8, 0.7)
                mot.command("forward", 5, 0.4)
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
            print(lt.data, 'find route and go straight')
            # append B
            actions.append("B")
            checkPoint(actions, checkpoints)

        # all black
<<<<<<< HEAD
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
                    print(lt.data, 'find route and go straight')
            
            time.sleep(1)
            start = False
            end = True
            print(actions)
            print(checkpoints)
=======
                elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            mot.command("forward", 2, 0.2)
            # checking if it is still black at the front
            if lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                mot.command("forward", 2, 0.2)
                # last check if it is still black at the front
                if lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                    print(lt.data, 'Reach END')
                    time.sleep(1)
                    start = False
                    end = True
                    # make a U-turn
                    mot.command("backward", 6, 0.4) # can change this part ikut kesesuaian
                    mot.command("right", 5, 0.5) # can change this part ikut kesesuaian
>>>>>>> 862a4c10d041ddfb7b3b6f30617f999582c475dc

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
                mot.command("left", 8, 0.6)
                time.sleep(0.5)
                mot.command("forward", 5, 0.4)
                actions.pop()
            elif checkpoints[-1] == "R":
                print(lt.data, 'stop and turn right')
                mot.command("right", 8, 0.6)
                time.sleep(0.5)
                mot.command("forward", 5, 0.4)
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
            time.sleep(1)
            end = False


except KeyboardInterrupt:
    lt.stop()
    mot.stop()
