# speed = 2343
# binspeed = bin(speed)
# print(binspeed)
# result = speed >> 8
# result2 = speed & 0xFF
# print(bin(result))
# print(bin(result2))

# res1 = [speed>>(8*(i-1)) & 0xFF for i in range(2,0,-1)]

# print(res1)

def sendmoveSpeed(dir,speed,acc):
    byte2 = (dir << 7) | (speed >> 8)
    byte3 = speed & 0xFF
    fullcommand = [246,byte2,byte3,acc]
    print(fullcommand)

sendmoveSpeed(0,3000,255)