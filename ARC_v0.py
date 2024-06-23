import can
import time

import can.interface


def getAxisPos(axis_id):
    print('n/a')

def confMotorCurrent(bus,axis_id,current):
    # Set motor Current
    cmd = 131
    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    fullcommand += [current>>(8*(i-1)) & 0xFF for i in range(2,0,-1)]
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                print('Current on motor', axis_id, 'set to', current)
                break

            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0):
                print('Set current failed')
                break

def confMotorDir(bus,axis_id,dir):
    # dir = 00 CW 
    # dir = 01 CCW
    # Set Motor Direction
    cmd = 134
    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    fullcommand.append(dir)
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                if(dir == 0):
                    direction = 'CW'
                else:
                    direction = 'CCW'

                print('Motor',axis_id, 'set to', direction)
                break

            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0):
                print('Limit remap failed!')
                break

def confMotorEnLimRemp(bus,axis_id,enable):
    # Remap motor limits
    cmd = 158
    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    fullcommand.append(enable)
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                print('Limit remap success!')
                break

            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0):
                print('Limit remap failed!')
                break

def confMotorHomeSeq(bus,axis_id,homeTrig,homeDir,homeSpd,endLimitEN):
    # Remap motor limits
    cmd = 144
    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    fullcommand.append(homeTrig)
    fullcommand.append(homeDir)
    res1 = [homeSpd>>(8*(i-1)) & 0xFF for i in range(2,0,-1)]
    fullcommand += res1
    fullcommand.append(endLimitEN)
    print(fullcommand)
    fullcommand.append(calculate_crc(fullcommand))
    
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                print('Home config success!')
                break

            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0):
                print('Home config failed!')
                break

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
    fullcommand.append(calculate_crc(fullcommand))
    # print(fullcommand)
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    motorStart = False
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                motorStart = True
            # Check if the received message is from an expected motor, check if motor has started running, and check if motor has finished running    
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 2) and motorStart:
                break
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0) and motorStart:
                print('home failed')
                break
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 3) and motorStart:
                print('FAULT: limit reached')
                break

def sendhome(bus,axis_id):
    
    cmd = 145
    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    fullcommand.append(calculate_crc(fullcommand))
    # print(fullcommand)
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    motorStart = False
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:

            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                motorStart = True
            # Check if the received message is from an expected motor, check if motor has started running, and check if motor has finished running    
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 2) and motorStart:
                break
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0) and motorStart:
                print('home failed')
                break

def calculate_crc(data):
    crc = sum(data) & 0xFF
    return crc


bus = can.interface.Bus(interface='slcan', channel='COM3', bitrate=500000)


# message = can.Message(arbitration_id=arbitration_id, data=fullcommand[1:], is_extended_id=False)
# message = genMove1Command(4, 1, 3000, 255)
# message = genMove2Command(1,-180, 600, 2)

""" sendhome(bus,1)
for i in range(20):
    genMove1Command(1, 100, 3000, 255)
    genMove1Command(1, 150, 3000, 255)
for i in range(20):
    genMove1Command(1, 50, 3000, 255)
    genMove1Command(1, 200, 3000, 255)
for i in range(20):
    genMove1Command(1, 10, 3000, 255)
    genMove1Command(1, 260, 3000, 255) """

# confMotorHomeSeq(bus,2,0,0,200,1)
# confMotorDir(bus,2,0)
# sendhome(bus,1)
# sendhome(bus,2)
genMove1Command(1, 1000, 200, 240)
for i in range(10):
    genMove1Command(2, -18000, 2000, 240)
    genMove1Command(2, -20000, 2000, 255)



# genMove1Command(1, 10, 200, 255)
# genMove1Command(1, 3000, 200, 255)


# confMotorCurrent(bus,1,3200)
# confMotorDir(bus, 1,0)

bus.shutdown()
# confMotorEnLimRemp(bus,4,1)

# genMove1Command(1, 10, 200, 255)
# genMove1Command(1, 200, 200, 255)

#bus.send(message)

