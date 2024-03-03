from machine import Pin
import time
from device_mode import DeviceMode
import mode_peripherals

p = Pin(25, Pin.OUT)


def main():
    mode = DeviceMode.read_mode()
    mode_peripherals.init_mode_peripherals()
    while True:
        p.high()
        time.sleep(1)
        p.low()
        time.sleep(1)


if __name__ == "__main__":
    print("Hello World!")
    main()
