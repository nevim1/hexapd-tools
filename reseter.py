#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import signal

def stopHandler(signum, frame):
    print("lad")
    scanner()

signal.signal(signal.SIGTSTP, stopHandler)

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

def scanner():
    print('scan continuosly? (y/n) ')
    ch = getch()
    if ch == 'y':
        scanCont = True 
    elif ch == chr(0x1b):
        return
    else:
        scanCont = False
 
    while True:
        if not scanCont:
            print('waiting for input (ESC for quit)')
            if getch() == chr(0x1b):
                scanner()
        for i in range(1, 19):
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
            
            time.sleep(1)
scanner()

'''
# Enable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler2.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler2.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL2_ID)

print("torque enabled")

print(packetHandler2.write1ByteTxRx(portHandler, DXL2_ID, 65, 1))

time.sleep(1)

while True:
    print("Press any key to continue! (or press ESC to quit!)")
    time.sleep(0.5)
    if getch() == chr(0x1b):
        break

    # Write Dynamixel#2 goal position
    dxl_comm_result, dxl_error = packetHandler2.write4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_GOAL_POSITION, dxl2_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler2.getRxPacketError(dxl_error))


    while True:
        # Read Dynamixel#2 present position
        print('bro why not work')
        dxl2_present_position, dxl_comm_result, dxl_error = packetHandler2.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
        print(dxl_comm_result, dxl_error, dxl2_goal_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler2.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL2_ID, dxl2_goal_position[index], dxl2_present_position))
        time.sleep(0.5)

        if not (abs(dxl2_goal_position[index] - dxl2_present_position) > DXL2_MOVING_STATUS_THRESHOLD):
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0    

# Disable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler2.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler2.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler2.getRxPacketError(dxl_error))
'''
# Close port
portHandler.closePort()
