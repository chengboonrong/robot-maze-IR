from line_tracker import line_tracker
from motor import motor
import time
from rules import LHR, back_travel

address = "192.168.0.100"  # Alphabot-PiZero-00
mot = motor(address)
lt = line_tracker(address)
lt.start()

th_0 = 200  # left most
th_1 = 400  # left
th_2 = 500  # middle
th_3 = 400  # right
th_4 = 300  # right most

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
        count = 0
        # P1 just straight if not detect junction on left of right (straight line)
        if lt.data[2] <= th_2 and lt.data[0] > th_0 and lt.data[4] > th_4:
            # Just Go Straight
            print(lt.data, 'P1: just go straight because there is no junction on left of right')
            mot.command("forward", 5, 0.2)

        # P2 slightly right (straight line)
        elif lt.data[2] > th_2 and lt.data[0] > th_0 and lt.data[1] > th_1 and (
                (lt.data[3] < th_3) != (lt.data[4] < th_4)):
            print(lt.data, 'slightly right')
            mot.command("right", 4, 0.1)
            if lt.data[4] < 200:
                print(lt.data, "backward lt[4] < 200")
                mot.command("backward", 4, 0.2)

        # P3 slightly left (straight line)
        elif lt.data[2] > th_2 and lt.data[4] > th_4 and lt.data[3] > th_3 and (
                (lt.data[1] < th_1) != (lt.data[0] < th_0)):
            print(lt.data, 'P2.2: slightly left')
            mot.command("left", 4, 0.1)
            if lt.data[0] < 200:
                print(lt.data, "P2.2: backward lt[0] < 200")
                mot.command("backward", 4, 0.2)

        # P4 if the line become all white. Check few step backward.
        elif lt.data[2] > th_2 and lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[3] > th_3 and lt.data[4] > th_4:
            while lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3:
                mot.command("backward", 4)
            time.sleep(1)
            if lt.data[2] < th_2 or lt.data[1] < th_1 or lt.data[3] < th_3 and lt.data[0] > th_0 and lt.data[4] > th_4:
                if lt.data[1] < th_1 and lt.data[2] > th_2 and lt.data[3] > th_3:
                    print(lt.data, "1 line detected it must be U-turn")
                    time.sleep(0.5)
                    while lt.data[3] > th_3 and lt.data[2] > th_2:
                        mot.command("right", 4)
                    actions.append("B")
                    LHR(actions, checkpoints)
                    time.sleep(1)
                elif lt.data[2] < th_2 and lt.data[1] > th_1 and lt.data[3] > th_3:
                    print(lt.data, "1 line detected it must be U-turn")
                    time.sleep(0.5)
                    while lt.data[3] > th_3 and lt.data[1] > th_1:
                        mot.command("right", 4)
                    actions.append("B")
                    LHR(actions, checkpoints)
                    time.sleep(1)
                elif lt.data[3] < th_3 and lt.data[2] > th_2 and lt.data[1] > th_1:
                    print(lt.data, "1 line detected it must be U-turn")
                    time.sleep(0.5)
                    while lt.data[2] > th_2 and lt.data[1] > th_1:
                        mot.command("right", 4)
                    actions.append("B")
                    LHR(actions, checkpoints)
                    time.sleep(1)
                else:
                    print(lt.data, "Paragraph 4.1")

            else:
                print(lt.data, "Paragraph 4")

        # P5 Right junction without left junction but check whether straight path exist or not.
        elif lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] > th_0 and lt.data[1] > th_1:
            mot.command("stop")
            while lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] > th_0 and lt.data[1] > th_1:
                mot.command("forward", 4)
            time.sleep(0.5)
            if lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[0] > th_0 and lt.data[4] > th_4:
                print(lt.data, "Junction at right without left junction and not T junction")
                while lt.data[3] > th_3 and lt.data[2] > th_2:
                    mot.command("right", 4)
                actions.append("R")
                LHR(actions, checkpoints)
                time.sleep(1)
            else:
                print(lt.data, "There have straight path after right junction")
                actions.append("S")
                LHR(actions, checkpoints)
                time.sleep(1)

        # P6 just check for left junction whether it become End or not
        elif lt.data[0] < th_0 and lt.data[1] < th_1:
            while lt.data[0] < th_0 and lt.data[1] < th_1:
                mot.command("forward", 4, 0.2)
                count += 1
            if lt.data[0] > th_0 and lt.data[1] > th_1 and count < 3:
                while lt.data[0] > th_0 and lt.data[1] > th_1:
                    mot.command("backward", 4)
                time.sleep(1)
                print(lt.data, "Junction at left and turn left")
                while lt.data[1] < th_1:
                    time.sleep(0.5)
                    mot.command("left", 4)
                actions.append("L")
                LHR(actions, checkpoints)
                time.sleep(1)

            elif lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 and count >= 3:
                print(lt.data, "Reach The End Successfully")
                while lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3:
                    time.sleep(0.5)
                    mot.command("backward", 4)
                time.sleep(1)
                if lt.data[0] > th_0 and lt.data[4] > th_4:
                    time.sleep(0.5)
                    while lt.data[0] > th_0:
                        mot.command("right", 4)
                    print(lt.data, "Ready to continue RH5")
                    start = False
                    end = True
            else:
                print(lt.data, "P6")
        else:
            print(lt.data, "Else for most out function!! Check for value that is not in condition")
            time.sleep(5)

    #########################################
    print(actions)
    print("FROM END TO START")
    back_travel(actions)
    print(actions)
    #########################################

    while end:
        if type(lt.data) == int:
                continue

        if lt.data[2] <= th_2 and lt.data[0] > th_0 and lt.data[4] > th_4:
            # Just Go Straight
            print(lt.data, 'P1: just go straight because there is no junction on left of right')
            mot.command("forward", 5, 0.2)

        # P2 slightly right (straight line)
        elif lt.data[2] > th_2 and lt.data[0] > th_0 and lt.data[1] > th_1 and (
                (lt.data[3] < th_3) != (lt.data[4] < th_4)):
            print(lt.data, 'slightly right')
            mot.command("right", 4, 0.1)
            if lt.data[4] < 200:
                print(lt.data, "backward lt[4] < 200")
                mot.command("backward", 4, 0.2)

        # P3 slightly left (straight line)
        elif lt.data[2] > th_2 and lt.data[4] > th_4 and lt.data[3] > th_3 and (
                (lt.data[1] < th_1) != (lt.data[0] < th_0)):
            print(lt.data, 'P2.2: slightly left')
            mot.command("left", 4, 0.1)
            if lt.data[0] < 200:
                print(lt.data, "P2.2: backward lt[0] < 200")
                mot.command("backward", 4, 0.2)

        # if meet left or right junction (mark as Checkpoint)
        elif (lt.data[0] < th_0 and lt.data[1] < th_1) or (lt.data[3] < th_3 and lt.data[4] < th_4):
            time.sleep(2)
            if actions[-1] == "L":
                print(lt.data, "stop and turn left")
                while lt.data[1] < th_1:
                    mot.command("left", 4, 0.2)
                actions.pop()

            elif actions[-1] == "R":
                print(lt.data, "stop and turn right")
                while lt.data[3] < th_3:
                    mot.command("right", 4, 0.2)
                actions.pop()

            elif actions[-1] == "S":
                print(lt.data, "stop and go straight")
                while (lt.data[0] < th_0 and lt.data[1] < th_1) or (lt.data[3] < th_3 and lt.data[4] < th_4):
                    mot.command("forward", 5, 0.2)
                actions.pop()


except KeyboardInterrupt:
    lt.stop()
    mot.stop()
