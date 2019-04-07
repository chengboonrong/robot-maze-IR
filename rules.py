def LHR(arr, ckp):
	str1 = ''.join(arr[-3:])
	if str1 == "LBL":
		del arr[-3:]
		arr.append("S")
		ckp.append("S")
	elif str1 == "LBR" or str1 == "RBL" or str1 == "SBS":
		del arr[-3:]
		arr.append("B")
		ckp.append("B")
	elif str1 == "LBS" or str1 == "SBL":
		del arr[-3:]
		arr.append("R")
		ckp.append("R")

def back_travel(arr):
	for i in range(len(arr)):
		if arr[i] == "L":
			arr[i] = "R"
		elif arr[i] == "R":
			arr[i] = "L"	
	arr.reverse()
	return arr


# def RHR(arr, ckp):
# 	str1 = ''.join(arr[-3:])
# 	if str1 == "RBR":
# 		del arr[-3:]
# 		arr.append("S")
# 		ckp.append("S")
# 	elif str1 == "RBL" or str1 == "LBR" or str1 == "SBS":
# 		del arr[-3:]
# 		arr.append("B")
# 	elif str1 == "RBS" or str1 == "SBR":
# 		del arr[-3:]
# 		arr.append("L")
# 		ckp.append("L")