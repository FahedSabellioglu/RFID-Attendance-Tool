import serial

def Read():
    ser = serial.Serial(timeout=10,
        port='COM3',
        baudrate=9600)
    if ser.readable():
        line = ser.readline()
        if len(line.split()) != 0 and "FF" not in line:
            return line.strip()


