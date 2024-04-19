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
    fullcommand.append(calculate_crc(fullcommand))
    # print(fullcommand)
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)

    motorStart = False
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            received_data_bytes = ', '.join([f'0x{byte:02X}' for byte in received_msg.data])
            # print(f"Received: arbitration_id=0x{received_msg.arbitration_id:X}, data=[{received_data_bytes}], is_extended_id=False")
             # Check if the received message is from an expected motor and check if motor has started running
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                motorStart = True
            # Check if the received message is from an expected motor, check if motor has started running, and check if motor has finished running    
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 2) and motorStart:
                break
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0) and motorStart:
                print('home failed')
                break
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0) and motorStart:
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
            received_data_bytes = ', '.join([f'0x{byte:02X}' for byte in received_msg.data])
            # print(f"Received: arbitration_id=0x{received_msg.arbitration_id:X}, data=[{received_data_bytes}], is_extended_id=False")
             # Check if the received message is from an expected motor and check if motor has started running
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


bus = can.interface.Bus(bustype='slcan', channel='COM3', bitrate=500000)


# message = can.Message(arbitration_id=arbitration_id, data=fullcommand[1:], is_extended_id=False)
# message = genMove1Command(1, 10, 3000, 255)
# message = genMove2Command(1,-180, 600, 2)
sendhome(bus,1)
for i in range(20):
    genMove1Command(1, 100, 3000, 255)
    genMove1Command(1, 150, 3000, 255)
for i in range(20):
    genMove1Command(1, 50, 3000, 255)
    genMove1Command(1, 200, 3000, 255)
for i in range(20):
    genMove1Command(1, 10, 3000, 255)
    genMove1Command(1, 260, 3000, 255)


# genMove1Command(1, 10, 200, 255)
# genMove1Command(1, 200, 200, 255)

#bus.send(message)

