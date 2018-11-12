import io
import fcntl
import time

write = io.open("/dev/i2c-1", "wb", buffering=0)

# Set slave address to 0x66
fcntl.ioctl(write, 0x703, 0x66)
start = time.monotonic()
# Each packet is 255 bytes of color
# Teensy can receive a maximum packet of 259 bytes
# 225 is divisible by 3 so it makes a nice cut off for
# sending colors and divides 9000 making it a nice cut off for
# sending the whole update
length = 225 
# Frames to write
frames = 100
# Write 9000 values for each frame
iters = 9000//length * frames
for i in range(iters):
    write.write(bytes([255]*length))
write.write(bytes([0]*length))
end = time.monotonic()
print("Wrote {} packtes of {} bytes ({} frames) in {} seconds".format(iters, length, frames, end-start))
print("This is a framerate of {} fps".format(frames/(end-start)))
