#!/usr/bin/env python3
import inputs
import time
import threading
import sys
import fpstimer
from ctypes import *
libmario = CDLL("libmario.dll")

Vec3f = (c_float * 3)

libmario.init.restype = None
libmario.init.artypes = []

libmario.step.restype = None
libmario.step.artypes = [c_int32, c_float, c_float]

libmario.getMarioPosition.restype = None
libmario.getMarioPosition.artypes = [Vec3f]

libmario.getMarioVelocity.restype = None
libmario.getMarioVelocity.artypes = [Vec3f]

libmario.getMarioAnimFrame.restype = c_int32
libmario.getMarioAnimFrame.artypes = []

libmario.getMarioAnimIndex.restype = c_int32
libmario.getMarioAnimIndex.artypes = []

CONT_A      = 0x8000
CONT_B      = 0x4000
CONT_G      = 0x2000
CONT_START  = 0x1000
CONT_UP     = 0x0800
CONT_DOWN   = 0x0400
CONT_LEFT   = 0x0200
CONT_RIGHT  = 0x0100
CONT_L      = 0x0020
CONT_R      = 0x0010
CONT_E      = 0x0008
CONT_D      = 0x0004
CONT_C      = 0x0002
CONT_F      = 0x0001

A_BUTTON     = CONT_A
B_BUTTON     = CONT_B
L_TRIG       = CONT_L
R_TRIG       = CONT_R
Z_TRIG       = CONT_G
START_BUTTON = CONT_START
U_JPAD       = CONT_UP
L_JPAD       = CONT_LEFT
R_JPAD       = CONT_RIGHT
D_JPAD       = CONT_DOWN
U_CBUTTONS   = CONT_E
L_CBUTTONS   = CONT_C
R_CBUTTONS   = CONT_F
D_CBUTTONS   = CONT_D

events = []
_t = None
_handler = None

def worker():
    global events
    while True:
        events.append(inputs.get_gamepad())

def main():
    global _t
    global _handler
    global events
    if not _t :
        _t = threading.Thread(target=worker)
        _t.daemon = True
        _t.start()
    stick_x = 0.0
    stick_y = 0.0
    buttons = 0
    libmario.init()
    timer = fpstimer.FPSTimer(30)
    try:
        while True:
            while len(events) > 0 :
                for event in events[0]:
                    if event.code == "ABS_X":
                        stick_x = float(event.state) / 32768.0
                    elif event.code == "ABS_Y":
                        stick_y = float(event.state) / 32768.0
                    elif event.code == "ABS_RX":
                        gpd_input = "Right Stick X"
                    elif event.code == "ABS_RY":
                        gpd_input = "Right Stick Y"
                    elif event.code == "BTN_SOUTH":
                        if event.state == 1:
                            buttons |= A_BUTTON
                        else:
                            buttons &= ~A_BUTTON
                    elif event.code == "BTN_WEST":
                        if event.state == 1:
                            buttons |= B_BUTTON
                        else:
                            buttons &= ~B_BUTTON
                    elif event.code == "ABS_Z":
                        if event.state == 255:
                            buttons |= Z_TRIG
                        else:
                            buttons &= ~Z_TRIG
                    elif event.code != "SYN_REPORT":
                        print(event.code + ':' + str(event.state))
                events.pop(0)
            
            libmario.step(buttons, c_float(stick_x), c_float(stick_y))
            pos = Vec3f()
            vel = Vec3f()
            libmario.getMarioPosition(pos)
            libmario.getMarioVelocity(vel)
            
            print('Position: %8.2f %8.2f %8.2f  Velocity: %8.2f %8.2f %8.2f Buttons: 0x%08X Anim: 0x%02X AnimFrame: %d' % (pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], buttons, libmario.getMarioAnimIndex(), libmario.getMarioAnimFrame()))

            timer.sleep()
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        sys.exit(0)

if __name__ == '__main__':
    main()
