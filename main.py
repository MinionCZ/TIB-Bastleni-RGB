from machine import Pin
import time
from device_mode import DeviceMode
import mode_peripherals
from handlers.hsv_transition_handler import handle_hsv_transition_mode
from handlers.pulsing_colors_handler import handle_pulsing_colors_mode
from handlers.rainbow_mode_handler import handle_rainbow_mode
from handlers.single_color_handler import handle_single_color_mode
from handlers.snake_handler import handle_snake_mode

p = Pin(25, Pin.OUT)

__MODE_HANDLERS: dict = {
    DeviceMode.SINGLE_COLOR_MODE: handle_single_color_mode,
    DeviceMode.SNAKE_MODE: handle_snake_mode,
    DeviceMode.HSV_RAINBOW_MODE: handle_rainbow_mode,
    DeviceMode.PULSING_COLORS_MODE: handle_pulsing_colors_mode,
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
        time.sleep(0.005)


if __name__ == "__main__":
    main()
