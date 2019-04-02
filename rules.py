# arr = ["L", "R", "B", "L", "B" , "L"]

# right-hand rule
def checkPoint(arr):
	str1 = ''.join(arr[-3:])
	if str1 == "LBL":
		del arr[-3:]
		arr.append("S")
	elif str1 == "LBR", "RBL", "SBS":
		del arr[-3:]
		arr.append("B")
	elif str1 == "LBS" , "SBL":
		del arr[-3:]
		arr.append("R")

# shortened(arr)
# arr.reverse()
# print(arr)