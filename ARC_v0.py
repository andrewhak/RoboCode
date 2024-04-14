import can
import time


def getAxisPos(axis_id):
    print('n/a')

def genMove1Command(axis_id,pos, speed, acc):
    pos = int((pos*16384)/360)
    if pos < 0:
        pos = (abs(pos) ^ 0xFFFFFF) + 1

    cmd = 245

    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    res1 = [speed>>(8*(i-1)) & 0xFF for i in range(2,0,-1)]
    fullcommand += (res1)
    fullcommand.append(acc)
    res2 = [pos>>(8*(i-1)) & 0xFF for i in range(3,0,-1)]
    fullcommand += (res2)
    print(calculate_crc(fullcommand))
    fullcommand.append(calculate_crc(fullcommand))
    print(fullcommand)
    return can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)




def calculate_crc(data):
    crc = sum(data) & 0xFF
    return crc

bus = can.interface.Bus(bustype='slcan', channel='COM3', bitrate=500000)

arbitration_id = 1
cmd = 245
speed = 600
acc = 2
pos = -100

fullcommand = []
fullcommand.append(arbitration_id)
fullcommand.append(cmd)
res1 = [speed//2**(8*(i-1)) % 2**(8*(i)) for i in range(2,0,-1)]

fullcommand += (res1)
fullcommand.append(acc)

res2 = [pos//2**(8*(i-1)) % 2**(8*(i)) for i in range(3,0,-1)]
fullcommand += (res2)
fullcommand.append(calculate_crc(fullcommand))





# message = can.Message(arbitration_id=arbitration_id, data=fullcommand[1:], is_extended_id=False)
message = genMove1Command(1,-360, 600, 2)
# message = genMove2Command(1,-180, 600, 2)
bus.send(message)
