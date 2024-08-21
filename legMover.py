#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from dynamixel_sdk import *                     # import Dynamixel SDK library

# Control table address for Dynamixel PRO
torqueAddress = 64
goalPosAddress = 116
currentPosAddress = 132

# Default setting
baudrate = 1000000
devicename = '/dev/ttyUSB0'    # Check which port is being used on your controller
                               # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PortHandler instance
# Set the port path
portHandler = PortHandler(devicename)

# Initialize PacketHandler instance
packetHandler = Protocol2PacketHandler()

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(baudrate):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

legs = ((1,  3,  5),        #one line is one leg
        (2,  4,  6),        #one column in one set of servos
        (7,  9,  11),
        (8,  10, 12),
        (13, 15, 17),
        (14, 16, 18))


def resetServos(servos):
    for i in servos:
        if packetHandler.write1ByteTxOnly(portHandler, i, torqueAddress, 1) == COMM_SUCCESS:
            if packetHandler.write4ByteTxOnly(portHandler, i, goalPosAddress, 2048) == COMM_SUCCESS:
                print('servo ID#%03d sucessfuly rotated' % i)
                time.sleep(0.1)

while True:
    print('which servo group to reset? (ESC to quit)')
    match getch():
        case ch(0x1b):
            break
        case 'l':
            resetServos(legs[int(input('which leg to reset? 1-6')) - 1])
        case 'j':
            resetServos(i[int(input('which joint servos to reset? 1-3')) - 1] for i in legs)
        case 's':
            resetServos([int(i.strip()) for i in input('which servos to reset? 1-18 (divided by ,)').split(',')])

for i in range(18):
    packetHandler.write1ByteTxOnly(portHandler, i+1, torqueAddress, 0)
    time.sleep(1)


# Close port
portHandler.closePort()