# http://pythonhosted.org/pyserial/

from collections import namedtuple
import serial

frame = namedtuple('frame', ['src', 'dest', 'payload'])


def get_int(ser):
    b = ser.read()
    return int.from_bytes(b, byteorder='big')


def get_frame(ser):
    s = get_int(ser)
    d = get_int(ser)
    l = get_int(ser)
    p = list()
    while l > 0:
        i = get_int(ser)
        p.append(i)
        l -= 1
    return frame(s, d, p)


# Open serial port to XBee module
ser = serial.Serial('/dev/ttyUSB0')
print(ser.name)

# ser.write(b'hello this is python speaking\n')

# Read incoming data
f = get_frame(ser)
print(f)

f = get_frame(ser)
print(f)

# Close connection
ser.close()
