#!/usr/bin/env python

import os
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                     # Uses Dynamixel SDK library
#import dynamixel_sdk

# Control table address for Dynamixel PRO
ADDR_PRO_TORQUE_ENABLE      = 64
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION2           = 2.0

# Default setting
DXL2_ID                     = 8                 # Dynamixel#2 ID : 2
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL2_MINIMUM_POSITION_VALUE = 100 
DXL2_MAXIMUM_POSITION_VALUE = 4000
DXL2_MOVING_STATUS_THRESHOLD = 20                # Dynamixel PRO moving status threshold

index = 0
dxl2_goal_position = [DXL2_MINIMUM_POSITION_VALUE, DXL2_MAXIMUM_POSITION_VALUE]         # Goal position of Dynamixel PRO

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler2 = Protocol2PacketHandler()


# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

while True:
    print('waiting for input (ESC for quit)')
    if getch() == chr(0x1b):
        break

    for i in range(0, 253):
        data, result, error = packetHandler2.read1ByteTxRx(portHandler, i, 7) #read from id byte
        if result == -3001:
            continue

        print(result, error)
        
        if result != COMM_SUCCESS:
            print("%s" % packetHandler2.getTxRxResult(result))
        elif error != 0:
            print('%s' % packetHandler2.getRxPacketError(error))
        else:
            print('id of this servo is #%03d' % data)

              




        '''
        result, error = packetHandler2.write1ByteTxRx(portHandler, i, ADDR_PRO_TORQUE_ENABLE, 1)
        if result == COMM_SUCCESS:
            print("torque enabled for ID:%03d" % i)
            dxl_comm_result, dxl_error = packetHandler2.write4ByteTxRx(portHandler, i, ADDR_PRO_GOAL_POSITION, 2048)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:           
                print("%s" % packetHandler2.getRxPacketError(dxl_error))
            else:
                print("Dynamixel#%03d has been successfully rotated" % i)
                '''
