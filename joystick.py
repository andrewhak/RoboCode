import pygame
import joystick

# Initialize pygame
pygame.init()

# Set up the Xbox controller
pygame.joystick.init

joysticks = []
# event handler
for event in pygame.event.get():
    if event.type == pygame.JOYDEVICEADDED:
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks.append(joy)
    if event.type == pygame.JOYAXISMOTION:
        print(event)
for joystick in joysticks:
    print(joystick.get_numaxes())

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis in [0,1] :
                x = joystick.get_axis(0)
                y = joystick.get_axis(1)

                print( "J1", round(x,2) , round(y,2) )
            if event.axis in [2,3] :
                x = joystick.get_axis(2)
                y = joystick.get_axis(3)

                print( "J2", round(x,2) , round(y,2) )
            