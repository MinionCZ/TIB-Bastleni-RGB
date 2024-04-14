from neopixel import NeoPixel
from machine import Pin

__RGB_LEDS_PIN: Pin = Pin(15, Pin.OUT)
__NUMBER_OF_LEDS = 60
__leds = NeoPixel(__RGB_LEDS_PIN, __NUMBER_OF_LEDS)


def __convert_potentiometer_reading_to_color(value: int) -> int:
    value = value >> 8
    percentage = (10 ** (value / 256) - 1) / 9
    return int(255 * percentage)


def handle_single_color_mode() -> None:
    print("Handling single color mode")
    # TODO tady budeme programovat


def handle_snake_mode() -> None:
    print("handling snake mode")


def handle_rainbow_mode() -> None:
    print("handling rainbow mode")


def handle_pulsing_single_color_mode() -> None:
    print("handling pulsing single color mode")


def handle_hsv_transition_mode() -> None:
    print("handling hsv transition mode")
