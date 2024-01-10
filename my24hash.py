import hashlib


"""
compute the first 24 bit of sha1hash to find a collision


"""


def my24hash(str, power):
    while power > 0:
        power -= 1
        hashStr = hashlib.sha1(str.encode("utf-8"))
        hexDig = hashStr.hexdigest()
        str = hexDig[:6]
    return str

my_dict = {}
resDict = {}

orgStr = "MANGO"
resDict[0] = orgStr
i = 0
while True:
    i += 1
    hashL = my24hash(resDict.get(i - 1, ""), 1)
    hashR = my24hash(resDict.get(2 * i - 2, ""), 2)
    resDict[i] = hashL
    resDict[2 * i] = hashR
    if hashR == hashL:
        print(f"Collision!  {resDict[i]} {resDict[2 * i]} {i}")
        j = 1
        odd = True
        while True:
            preL = resDict.get(i - j, "")
            if odd:
                preR = my24hash(resDict.get(2 * i - j - 1, ""), 1)
                resDict[2 * i - j] = preR
            else:
                preR = resDict.get(2 * i - j, "")
            print(f"previous values: power {i - j} {preL},power {2 * i - j} {preR}")
            if preL != preR:
                break
            j += 1
            odd = not odd

        break