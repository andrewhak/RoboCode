import can
import time


def getAxisPos(axis_id):
    print('n/a')

def genMove1Command(axis_id, speed, acceleration):
    can_id = format(axis_id, '02X')
    speed_hex = format(speed, '04X')
    accel_hex = format(acceleration, '02X')
    print('move command')

    parts = line.split(' ')
    arbitration_id = int(parts[0][:2], 16)
    data = [int(parts[0][i:i+2], 16) for i in range(2, len(parts[0]), 2)] + [int(byte, 16) for byte in parts[1:]]
    return can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)

def calculate_crc(data):
    crc = sum(data) & 0xFF
    return crc

bus = can.interface.Bus(bustype='slcan', channel='COM3', bitrate=500000)

speed = 600
acc = 2
pos = 16384
spdhex = hex(600)
spdform = format(speed, '04X')
poshex = format(pos, '06X')
arbitration_id = 1
cmd = format(245, '02X')

data = [arbitration_id,cmd,int(spdform[-4:-2]),int(spdform[-2:]),hex(acc),hex(poshex[-6:-4]),poshex[-4:-2],poshex[-2:]]

print(poshex)
print(poshex[-2:])
print(poshex[-4:-2])
print(spdhex)
print(spdform)
print(data)


data2int = [arbitration_id,245,2,58,2,0,64,0]



data2 = bytearray(data2int)
print(data2)
CRCs = calculate_crc(data2)
data2int.append(CRCs)

print(data2int)


message = can.Message(arbitration_id=arbitration_id, data=data2int[1:], is_extended_id=False)
print(message)
bus.send(message)
