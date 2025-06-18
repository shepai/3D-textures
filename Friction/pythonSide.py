import serial
import keyboard  # pip install keyboard

ser = serial.Serial('COM3', 9600)  # Adjust to your Arduino port

while True:
    if keyboard.is_pressed('up'):
        ser.write(b'w')
    elif keyboard.is_pressed('down'):
        ser.write(b's')
    elif keyboard.is_pressed('left'):
        ser.write(b'a')
    elif keyboard.is_pressed('right'):
        ser.write(b'd')
