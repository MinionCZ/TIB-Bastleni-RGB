from neopixel import NeoPixel
from machine import Pin, ADC

__RGB_LEDS_PIN: Pin = Pin(15, Pin.OUT)
__NUMBER_OF_LEDS = 60
__red_potentiometer = ADC(Pin(26, Pin.IN))
__green_potentiometer = ADC(Pin(27, Pin.IN))
__blue_potentiometer = ADC(Pin(28, Pin.IN))

__leds = NeoPixel(__RGB_LEDS_PIN, __NUMBER_OF_LEDS)


def __convert_potentiometer_reading_to_color(value: int) -> int:
    linear_value = 10 ** (value / 65535)
    percentage = (linear_value - 1) / 9
    return int(255 * percentage)


def handle_single_color_mode() -> None:
    red_potentiometer_value = __red_potentiometer.read_u16()
    red = __convert_potentiometer_reading_to_color(red_potentiometer_value)
    green_potentiometer_value = __green_potentiometer.read_u16()
    green = __convert_potentiometer_reading_to_color(green_potentiometer_value)
    blue_potentiometer_value = __blue_potentiometer.read_u16()
    blue = __convert_potentiometer_reading_to_color(blue_potentiometer_value)
    for i in range(__NUMBER_OF_LEDS):
        __leds[i] = (green, red, blue)
    __leds.write()


def handle_snake_mode() -> None:
    print("handling snake mode")


def handle_rainbow_mode() -> None:
    print("handling rainbow mode")


def handle_pulsing_single_color_mode() -> None:
    print("handling pulsing single color mode")


def handle_hsv_transition_mode() -> None:
    print("handling hsv transition mode")
