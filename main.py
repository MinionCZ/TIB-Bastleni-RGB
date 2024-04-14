import typing

from machine import Pin
import time
from device_mode import DeviceMode
import mode_peripherals
from rgb_leds_handlers import handle_single_color_mode, handle_snake_mode, handle_rainbow_mode, \
    handle_pulsing_single_color_mode

p = Pin(25, Pin.OUT)

__MODE_HANDLERS: typing.Dict[int, typing.Callable] = {
    DeviceMode.SINGLE_COLOR_MODE: handle_single_color_mode,
    DeviceMode.SNAKE_MODE: handle_snake_mode,
    DeviceMode.HSV_RAINBOW_MODE: handle_rainbow_mode,
    DeviceMode.PULSING_SINGLE_COLOR_MODE: handle_pulsing_single_color_mode,
    DeviceMode.HSV_TRANSITION_MODE: handle_hsv_transition_mode,
}


def handle_rgb_mode(mode: DeviceMode) -> None:
    __MODE_HANDLERS[mode.mode]()


def main():
    mode = DeviceMode.read_mode()
    mode_peripherals.init_mode_peripherals()
    while True:
        handle_rgb_mode(mode)
        mode = DeviceMode.read_mode()
        time.sleep(0.01)


if __name__ == "__main__":
    print("Hello World!")
    main()
