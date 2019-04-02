from line_tracker import line_tracker
from motor import motor
import time
from rules import checkPoint

address = "192.168.0.100" # Alphabot-PiZero-00
mot = motor(address)
lt = line_tracker(address)
lt.start()

th_0 = 200  # left most
th_1 = 400  # left
th_2 = 500  # middle
th_3 = 400  # right
th_4 = 300  # right most

actions = []

while True:
    try:
        # to make sure the received data are all integer
        if type(lt.data) == int:
            continue
        # delay
        time.sleep(0.5)


        # to make sure there is no left or right junction
        condition_2 = True

        if lt.data[2] > th_2:
            # if
            while lt.data[2] > th_2 and condition_2:

                if lt.data[2] > th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
                    print(lt.data, 'slightly right')
                    mot.command("right", 4, 0.1)

                elif lt.data[2] > th_2 and lt.data[1] < th_1 or lt.data[0] < th_0:
                    print(lt.data, 'slightly left')
                    mot.command("left", 4, 0.1)

                # what is this for? 
                elif lt.data[3] < th_3 and lt.data[4] < th_4 and lt.data[0] > th_0: # black is detected on right sensors
                    if(lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2):
                        condition_2=False
                    else:
                        mot.command("forward", 4, 0.2)
                        print(lt.data, 'junction at right and speed up')
                        # append S
                        actions.append("S")
                        checkPoint(actions)

                else:
                    condition_2 = False
        
        # delay
        time.sleep(0.5)

        if lt.data[2] < th_2:
            print(lt.data, 'go straight')
            mot.command("forward", 5, 0.4)

        # all white
        elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
            print(lt.data, 'stop and U-Turn')
            time.sleep(1)
            # slowly adjust
            while lt.data[2] > th_2 and lt.data[1] > th_1 and lt.data[0] > th_0:
                print(lt.data, "U-Turn")
                # check if the turn right a quite hard so need to decrease the duration[turn right sikit-sikit]
                mot.command("right", 4, 0.2)
                time.sleep(0.5)
            print(lt.data, 'find route and go straight')
            # append B
            actions.append("B")
            checkPoint(actions)


        elif lt.data[0] < th_0 or lt.data[1] < th_1 and lt.data[2] < th_2:
            print(lt.data, 'stop and turn left')
            time.sleep(1)
            # this condition utk pastikan jika terlajak yang tengah sensor 0 dan 1 masih ada utk stop
            while lt.data[2] > th_2 and lt.data[3] > th_3 and lt.data[4] > th_4:
                print(lt.data, "turn left for T-Junction")
                # check if the turn right a quite hard so need to decrease the duration[turn right sikit-sikit]
                mot.command("left", 4, 0.2)
                time.sleep(0.5)
            print(lt.data, 'find route and go straight')
            # append L
            actions.append("L")
            checkPoint(actions)

        elif lt.data[3] < th_3 or lt.data[4] < th_4 and lt.data[2] < th_2:
            print(lt.data, 'stop and turn right')
            time.sleep(1)
            # this condition utk pastikan jika terlajak yang tengah sensor 0 dan 1 masih ada utk stop
            while lt.data[2] > th_2 and lt.data[0] > th_0 and lt.data[1] > th_1
                print(lt.data, "turn right for T-Junction")
                # check if the turn right a quite hard so need to decrease the duration[turn right sikit-sikit]
                mot.command("right", 4, 0.2)
                time.sleep(0.5)
            print(lt.data, 'find route and go straight')
            # append R
            actions.append("R")
            checkPoint(actions)

        # all black
        elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[2] < th_2 and lt.data[3] < th_3 or lt.data[4] < th_4:
            print(lt.data, 'Reach END')
            time.sleep(1)
            break


    except KeyboardInterrupt:
        lt.stop()
        mot.stop()
