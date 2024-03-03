from machine import Pin
import time
from device_mode import DeviceMode


p = Pin(25, Pin.OUT)

    
def main():
    mode = DeviceMode.read_mode()
    print(mode)
    while True:
        mode = DeviceMode(mode.mode + 1).save_mode()
        p.high()
        time.sleep(1)
        p.low()
        time.sleep(1)
        print(DeviceMode.read_mode())

if __name__ == "__main__":
    print("Hello World!")
    main()