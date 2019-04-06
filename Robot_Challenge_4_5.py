from line_tracker import line_tracker
from motor import motor
import time
from rules import checkPoint

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
# just added the checkpoint
new_checkpoints = ['S', 'R', 'L', 'L', 'R', 'R', 'L']
count = 0


# function to execute Left, Right or Straight action for turn back from the Last Checkpoint
def shortest(obj):
    # when shortest() function receive char 'R', so it will turn right
    if obj == 'R':
        print("Turn right")
        mot.command("right", 5, 0.5)
        mot.command("forward", 5, 0.5)
        while lt.data[0] > th_0 and lt.data[1] > th_1:
            print(lt.data, "turn right for Right-Junction")
            mot.command("right", 4, 0.2)
            time.sleep(0.5)
        print(lt.data, 'find route and go straight')

    # when shortest() function receive char 'L', so it will turn to left
    elif obj == 'L':
        print("Turn left")
        mot.command("left", 5, 0.5)
        mot.command("forward", 5, 0.5)
        while lt.data[4] > th_4 and lt.data[3] > th_3:
            print(lt.data, "turn left for the left junction")
            mot.command("left", 4, 0.2)
            time.sleep(0.5)
        print(lt.data, 'find route and go straight')

    # when shortest() function receive char 'S', so it will go straight
    else:
        print("Straight")
        mot.command("forward", 10, 0.5)


try:
    while start:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        # delay
        time.sleep(0.5)

        # when there is no T-junction
        condition_2 = True

        if lt.data[2] > th_2:
            # it will 2 possibility, 1. adjust right and left position 2. totally lost (end route or right junction)
            while lt.data[2] > th_2 and condition_2:

                # slightly right till it find line detected by lt_2 or lt_1 or lt_0
                if lt.data[2] > th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                    while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2:
                        print(lt.data, 'slightly right')
                        mot.command("right", 4, 0.1)

                # slightly left till it find line detected by lt_2 or lt_3 or lt_4
                elif lt.data[2] > th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
                    while lt.data[4] > th_0 and lt.data[3] > th_1 and lt.data[2] > th_2:
                        print(lt.data, 'slightly left')
                        mot.command("left", 4, 0.1)

                # when it totally lost from the line then take action to backward till find line.
                elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                    while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                        print(lt.data, 'backward till find at least 1 line tracker detect line')
                        mot.command("backward", 4, 0.2)

                else:
                    # this make condition_2 become false and exit from the while loop
                    condition_2 = False

        # It will decide to turn left, right or U-turn if the robot on the straight line.
        if lt.data[2] < th_2:
            # while condition lt 2 < th_2 and there is no junction at left and right, Just Go Straight
            while lt.data[2] < th_2 and lt.data[0] > th_0 and lt.data[4] > th_4:
                print(lt.data, 'just go straight because there is no junction on left of right')
                mot.command("forward", 5, 1)

            # when it detect left junction, so it will take action to turn left
            if lt.data[2] < th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
                print(lt.data, 'stop and turn left')
                time.sleep(0.5)
                # this mot.command to make sure it pass line and make at least 45 degree of left rotation
                mot.command("left", 8, 0.5)
                mot.command("forward", 5, 0.5)
                # it will proceed with turn to left bit by bit till the 3rd or 4th detect the line
                while lt.data[3] > th_3 and lt.data[4] > th_4:
                    print(lt.data, "turn left for Left-Junction")
                    mot.command("left", 4, 0.2)
                    time.sleep(0.5)
                print(lt.data, 'find route and go straight')
                # append L into the checkpoint function
                actions.append("L")
                checkPoint(actions, checkpoints)

            # After meet right junction with no left junction,it will check the straight path
            elif lt.data[2] < th_2 and lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] > th_0:
                print(lt.data, 'junction at the right and there is no left junction')
                time.sleep(0.5)
                # to get know whether it had a straight path or not
                mot.command("forward", 4, 0.2)
                print("check whether can go straight or turn right")
                time.sleep(0.2)

                # when the state from line change to all white. It assume that no straight path
                if lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[
                    4] > th_4:

                    # this loop to make sure it turn back till found line at least 1 sensor will detected
                    while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                        print(lt.data, 'backward till find at least 1 line tracker detect line')
                        mot.command("backward", 4, 0.2)

                    # turn right when meet right junction without left junction and straight path.
                    if lt.data[2] < th_2 or lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] < th_0:
                        time.sleep(0.5)
                        print(lt.data, 'right junction without left and straight path')
                        # it will continue looping turn right till 0 or 1 sensor meet the line.
                        while lt.data[0] > th_0 and lt.data[1] > th_1:
                            print(lt.data, "turn right for Right-Junction")
                            mot.command("right", 4, 0.2)
                            time.sleep(0.5)
                        print(lt.data, 'find route and go straight')
                        # append R into the checkpoint function
                        actions.append("R")
                        checkPoint(actions, checkpoints)
                    else:
                        # just put this if the data that we not expected
                        print(lt.data, "Maybe not turn right that we don't know DANGER ")

                else:
                    # it mean if have a line after go straight just now, so just go straight
                    print("junction at right and there is straight path")
                    actions.append("S")
                    checkPoint(actions, checkpoints)

            # All white, backward till meet a single line, then make U- turn while lt.data[0] > th_0 & lt.data[1] > th_1
            elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[
                4] > th_4:
                print(lt.data, 'Dead End')
                # it will turn back turn back till at least 1 of the sensor find the line.
                while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[
                    4] > th_4:
                    mot.command("backward", 4, 0.1)
                # this condition is to make sure there is no right and left junction
                if lt.data[0] > th_0 and lt.data[4] > th_4:
                    # it will turn right till 1st and 0 sensor detect a line
                    while lt.data[1] > th_1 and lt.data[0] > th_0:
                        print(lt.data, "U-Turn")
                        # check if the turn right a quite hard so need to decrease the duration[turn right bit-by-bit]
                        mot.command("right", 4, 0.2)
                        time.sleep(0.5)
                    print(lt.data, 'find route and go straight')
                    # append B to the checkpoint function
                    actions.append("B")
                    checkPoint(actions, checkpoints)
                else:
                    # just be aware and get know maybe there is an expected input to the system
                    print(lt.data, "Maybe not U-Turn That We Don't Know DANGER")

            # 6 all black, backward to find 1 line, then make a U-turn without append "B" value to the checkPoint
            elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                # go forward to check the line thick or not
                mot.command("forward", 4, 0.2)
                # if the line thick, it will proceed with this condition
                if lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[
                    4] < th_4:
                    print(lt.data, 'Reach END')
                    # it will backward till it exit from the END line and meet a single line
                    while lt.data[0] < th_0 and lt.data[4] < th_4:
                        mot.command("backward", 5, 0.5)
                    # this to make sure that it exit the thick line an make U-Turn without append 'B'
                    if lt.data[0] < th_0 and lt.data[4] < th_4:
                        # at least 90 degree of robot will rotate to the right
                        mot.command("right", 10, 0.8)
                        # turn right bit by bit till sensor 0 or 1 detect a single line
                        while lt.data[1] > th_1 and lt.data[0] > th_0:
                            print(lt.data, "U-Turn")
                            mot.command("right", 4, 0.2)
                            time.sleep(0.5)
                        print(lt.data, 'find route and go straight')

                    time.sleep(1)
                    # finish loop for start and start with end which turn back of the shortest path
                    start = False
                    end = True

    while end:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        # delay
        time.sleep(0.5)

        # when there is no T-junction
        condition_2 = True

        if lt.data[2] > th_2:
            # it will 2 possibility, 1. adjust right and left position 2. totally lost (end route or right junction)
            while lt.data[2] > th_2 and condition_2:

                # slightly right till it find line detected by lt_2 or lt_1 or lt_0
                if lt.data[2] > th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                    while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2:
                        print(lt.data, 'slightly right')
                        mot.command("right", 4, 0.1)

                # slightly left till it find line detected by lt_2 or lt_3 or lt_4
                elif lt.data[2] > th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
                    while lt.data[4] > th_0 and lt.data[3] > th_1 and lt.data[2] > th_2:
                        print(lt.data, 'slightly left')
                        mot.command("left", 4, 0.1)

                # when it totally lost from the line then take action to backward till find line.
                elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[
                    4] > th_4:
                    while lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                        print(lt.data, 'backward till find at least 1 line tracker detect line')
                        mot.command("backward", 4, 0.3)

                else:
                    condition_2 = False

        if lt.data[2] < th_2:
            while lt.data[2] < th_2 and lt.data[0] > th_0 and lt.data[4] > th_4:
                print(lt.data, 'just go straight because there is no junction on left of right')
                mot.command("forward", 5, 1)

            if lt.data[0] < th_0 and lt.data[1] < th_1 or lt.data[3] < th_3 and lt.data[4] < th_4:
                time.sleep(0.5)
                print(lt.data, "Junction on right or left")
                if count < len(new_checkpoints):
                    obj = new_checkpoints[count]
                    shortest(obj)
                    count += 1
                else:
                    print("Check value of count")

            else:
                print(lt.data, "Maybe there have other line tracker reading")
        else:
            end = False


except KeyboardInterrupt:
    lt.stop()
    mot.stop()
