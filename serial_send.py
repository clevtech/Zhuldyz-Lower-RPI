import sys
import serial

def main(command):
    if int(command / 10000) == 1:
        command = 'f_' + str(int(command % 10000))
    elif int(command / 10000) == 1:
        command = 'b_' + str(int(command % 10000))
    elif int(command / 10000) == 1:
        command = 'l_' + str(int(command % 10000))
    elif int(command / 10000) == 1:
        command = 'r_' + str(int(command % 10000))
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(command)
    return ser.readline()
