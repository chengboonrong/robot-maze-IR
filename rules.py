def check(act):
    str2 = ''.join(act[-3:])
    if str2 == "LBR" or str2 == "LBS" or str2 == "LBL" or str2 == "SBL" or str2 == "SBS" or str2 == "RBL":
        LHR(act)

    else:
        return act


def LHR(act):
    str1 = ''.join(act[-3:])
    if str1 == "LBL":
        del act[-3:]
        act.append("S")
        check(act)
    if str1 == "LBR" or str1 == "RBL" or str1 == "SBS":
        del act[-3:]
        act.append("B")
        check(act)
    elif str1 == "LBS" or str1 == "SBL":
        del act[-3:]
        act.append("R")
        check(act)
    else:
        return act


def back_travel(arr):
    for i in range(len(arr)):
        if arr[i] == "L":
            arr[i] = "R"
        elif arr[i] == "R":
            arr[i] = "L"
    arr.reverse()
    return arr
