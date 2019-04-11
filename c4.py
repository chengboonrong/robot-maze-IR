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

actions = []

try: 
  print("FROM START TO END")
	while start:
		if type(lt.data) == int:
            continue

    if lt.data[2] < th_2:
    	while lt.data[4] > th_4 and lt.data[0] > th_0:
        print(lt.data, 'go straight')
        mot.command("forward", 5, 0.4)
        time.sleep(0.2)

      # cross / T-junction / left corner / straight or left
      if lt.data[0] < th_0 and lt.data[1] < th_1:
      	mot.command("stop")
        mot.forward("forward", 5, 0.2)
      	mot.command("left", 8, 0.5)
      	mot.forward("forward", 5, 0.2)
      	# append L
        actions.append("L")
        LHR(actions, checkpoints)

      # right corner, straight or right
    	elif (lt.data[3] < th_3 and lt.data[4] < th_4) and (lt.data[0] > th_0 and lt.data[1] > th_1):
    		mot.command("stop")
    		mot.command("forward", 5, 0.2)
    		if lt.data[2] > th_2:
      		print("turn right at right corner")
      		mot.command("right", 8, 0.5)
    			# append R
          actions.append("R")
          LHR(actions, checkpoints)

      	else:
      		mot.command("forward", 8, 0.5)
          print("junction at right, speed up")
      		# append S
          actions.append("S")
          LHR(actions, checkpoints)

      elif lt.data[0] < th_0 and lt.data[1] < th_1 and lt.data[3] < th_3 and lt.data[4] < th_4:
        print(lt.data, 'Reach END')
        start = False
        end = True

    		time.sleep(0.2)


   	elif lt.data[2] > th_2:
   		if lt.data[3] < th_3:
      	print(lt.data, 'slightly right')
      	mot.command("right", 4, 0.3)

      elif lt.data[1] < th_1:
        print(lt.data, 'slightly left')
        mot.command("left", 4, 0.3)

      elif lt.data[0] > th_0 and lt.data[1] > th_1 and lt.data[3] > th_3 and lt.data[4] > th_4:
      	print(lt.data, "dead end, uturn")
      	mot.command("stop")
      	mot.command("right", 10, 0.6)
      	# append B
        actions.append("B")
        LHR(actions, checkpoints)

      time.sleep(0.2)

  print("FROM END TO START")
  while end:
    if type(lt.data) == int:
            continue

    if lt.data[2] < th_2:
      while lt.data[4] > th_4 and lt.data[0] > th_0:
        print(lt.data, 'go straight')
        mot.command("forward", 5, 0.4)
        time.sleep(0.2)

      if lt.data[0] < th_0 or lt.data[4] < th_4:
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

    elif lt.data[2] > th_2:
      if lt.data[3] < th_3:
        print(lt.data, 'slightly right')
        mot.command("right", 4, 0.3)

      elif lt.data[1] < th_1:
        print(lt.data, 'slightly left')
        mot.command("left", 4, 0.3)
    

except KeyboardInterrupt:
    lt.stop()
    mot.stop()