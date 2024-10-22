import can
import time
import pygame
import time
import can.interface

def get_joystick_values():
    pygame.event.pump()
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)
    z_axis = joystick.get_axis(2)
    return x_axis, y_axis, z_axis

# Function to get button inputs
def get_button_inputs():
    pygame.event.pump()
    buttons = {}
    dpad = joystick.get_hat(0)
    for i in range(joystick.get_numbuttons()):
        buttons[i] = joystick.get_button(i)
    return buttons, dpad

def readEncoderValueCarry(axis_id):
    cmd = 48
    fullcommand = [axis_id,cmd]
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            Carry = int.from_bytes(received_msg.data[1:5], 'big', signed=True)
            Value = int.from_bytes(received_msg.data[5:7], 'big', signed=False)
            Result = (Carry*16384) + Value
            print(round(((Result*360)/16384), 2))
            break

def readEncoderValueAdd(axis_id):
    cmd = 49
    fullcommand = [axis_id,cmd]
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            Value = int.from_bytes(received_msg.data[1:7], 'big',signed=True)
            print('Axis' + str(axis_id) + ' Encoder Value: ' + str(round(((Value*360)/16384), 2)))
            break

def readPulses(axis_id):
    cmd = 51
    fullcommand = [axis_id,cmd]
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            Value = int.from_bytes(received_msg.data[1:5], 'big',signed=True)
            print(Value)
            break

def readIO(axis_id):
    cmd = 52
    fullcommand = [axis_id,cmd]
    fullcommand.append(calculate_crc(fullcommand))
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            Value = bin(received_msg.data[1])[2:].zfill(8)
            print(Value)
            print("IN_1:  " + str(bool(int(Value[7]))))
            print("IN_2:  " + str(bool(int(Value[6]))))
            print("OUT_1: " + str(bool(int(Value[5]))))
            print("OUT_2: " + str(bool(int(Value[4]))))
            break

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
    print(fullcommand)
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
                print('FAULT: Axis' + str(axis_id) + ' limit reached')
                break


def sendmoveSpeed(axis_id,dir,speed,acc):
    byte2 = (dir << 7) | (speed >> 8)
    byte3 = speed & 0xFF
    fullcommand = [axis_id,246,byte2,byte3,acc]
    fullcommand.append(calculate_crc(fullcommand))
    # print(fullcommand)
    message = can.Message(arbitration_id=axis_id, data=fullcommand[1:], is_extended_id=False)
    bus.send(message)
    while True:
        received_msg = bus.recv(timeout=3) 
        if received_msg is not None:
            # print(received_msg)
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 0):
                # print("Run fail")
                break
            # Check if the received message is from an expected motor, check if motor has started running    
            if (received_msg.arbitration_id == axis_id) and (received_msg.data[1] == 1):
                # print("Run sucess")
                break
 


def sendMove3Command(axis_id,pos, speed, acc):
    pos = int((pos*16384)/360)
    if pos < 0:
        pos = (abs(pos) ^ 0xFFFFFF) + 1

    cmd = 244

    fullcommand = []
    fullcommand.append(axis_id)
    fullcommand.append(cmd)
    res1 = [speed>>(8*(i-1)) & 0xFF for i in range(2,0,-1)]
    fullcommand += (res1)
    fullcommand.append(acc)
    res2 = [pos>>(8*(i-1)) & 0xFF for i in range(3,0,-1)]
    fullcommand += (res2)
    fullcommand.append(calculate_crc(fullcommand))
    print(fullcommand)
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
                print('FAULT: Axis' + str(axis_id) + ' limit reached')
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

# Start can bus
bus = can.interface.Bus(interface='slcan', channel='COM3', bitrate=500000)

# Initialize variables
speed = 0
Acceleration = 0
elapsed_time = 0.1
ArmMaxSpeed = 5.0
GearRatios = [1.0,13.5,150.0,150.0,48.0,67.82,67.82]
axisSel = 1
joysel = 0
ons = [False]*10
prevJ = 0.0
dpad = 0


# Initialize pygame
pygame.init()

# Set up the Xbox controller
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Main Loop
try:
    while True:
        # Recieve Inputs
        x, y, z = get_joystick_values()
        buttons, dpad = get_button_inputs()

        # select Joystick axis
        if axisSel == 1:
            joysel = x
        elif axisSel == 2 or 3:
            joysel = y


        speed = int(((abs(joysel)-.01)/0.99)*ArmMaxSpeed*GearRatios[axisSel])
        Acceleration = abs(x)*10

        if prevJ != joysel:
            if 0.01 < joysel:

                sendmoveSpeed(axisSel,1,speed,0)
            elif -0.01 > joysel:
                sendmoveSpeed(axisSel,0,speed,0)
            else:
                sendmoveSpeed(1,0,0,0)
                sendmoveSpeed(2,0,0,0)
                sendmoveSpeed(3,0,0,0)
        
        # Sel
        if buttons[1] == False and ons[1] ==True:
            ons[1] = False
        if buttons[2] == False and ons[2] ==True:
            ons[2] = False
        if dpad[1] == 0 and ons[3] ==True:
            ons[3] = False
        if dpad[1] == 0 and ons[4] ==True:
            ons[4] = False
        
        # print(buttons)

        if buttons[1] and not buttons[2]and ons[1] == False:
            # sendMove3Command(1, 100, 100, 5)
            if axisSel < 3:
                axisSel += 1
            ons[1] = True
            print(axisSel)

        elif buttons[2]and not buttons[1] and ons[2] == False:
            # sendMove3Command(1, -100, 100, 5)
            if axisSel > 1:
                axisSel -= 1
            ons[2] = True
            print(axisSel)

        if dpad[1] == 1 and ons[3] == False:
            if ArmMaxSpeed < 15:
                ArmMaxSpeed += 1
            ons[3] = True
            print(ArmMaxSpeed)
            print(int(ArmMaxSpeed*GearRatios[axisSel]))
        elif dpad[1] == -1 and ons[4] == False:
            if ArmMaxSpeed > 0:
                ArmMaxSpeed -= 1
            ons[4] = True
            print(int(ArmMaxSpeed*GearRatios[axisSel]))


        if not (buttons[1] or buttons[2] or 0.1 < x or -0.1 > x):
            time.sleep(0.1)

        prevJ = joysel

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    pygame.quit()
    bus.shutdown()



