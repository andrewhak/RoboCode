import can
import time

# Program to test sending commands
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

speed = 0x0258
acc = 0x02
arbitration_id = 1
print(arbitration_id)
# data = bytearray[0xF5,0x02,0x58,acc,0x40,0x00,0x92]
data = bytearray([245,2,58,2,0,0,40,92])
print(data)


message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
print(message)
bus.send(message)
