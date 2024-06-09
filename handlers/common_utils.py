from neopixel import NeoPixel
from machine import Pin, ADC

__RGB_LEDS_PIN: Pin = Pin(15, Pin.OUT)
NUMBER_OF_LEDS = 60
leds = NeoPixel(__RGB_LEDS_PIN, NUMBER_OF_LEDS)

HUE_PERIOD = 360
__MAX_COLOR_VALUE = 255

__red_potentiometer = ADC(Pin(26, Pin.IN))
__green_potentiometer = ADC(Pin(27, Pin.IN))
__blue_potentiometer = ADC(Pin(28, Pin.IN))


def __convert_potentiometer_reading_to_color(value: int) -> int:
    linear_value = 10 ** (value / 65535)
    percentage = (linear_value - 1) / 9
    return int(255 * percentage)


def get_user_selected_colors() -> (int, int, int):
    red_potentiometer_value = __red_potentiometer.read_u16()
    red = __convert_potentiometer_reading_to_color(red_potentiometer_value)
    green_potentiometer_value = __green_potentiometer.read_u16()
    green = __convert_potentiometer_reading_to_color(green_potentiometer_value)
    blue_potentiometer_value = __blue_potentiometer.read_u16()
    blue = __convert_potentiometer_reading_to_color(blue_potentiometer_value)
    return red, green, blue


def handle_pulsing_colors_mode() -> None:
    print("handling pulsing single color mode")


def hsv_to_rgb(h: float, s: float, v: float) -> (int, int, int):
    __validate_hsv_color(s, v)
    modulated_h = h % HUE_PERIOD
    c = v * s
    x = c * (1 - abs((modulated_h / 60) % 2 - 1))
    m = v - c
    r_coef, g_coef, b_coef = __calculate_rgb_coefficients(modulated_h, c, x)
    r = (r_coef + m) * __MAX_COLOR_VALUE
    g = (g_coef + m) * __MAX_COLOR_VALUE
    b = (b_coef + m) * __MAX_COLOR_VALUE
    return int(r), int(g), int(b)


def __calculate_rgb_coefficients(h: float, c: float, x: float) -> (float, float, float):
    if h < 60:
        return c, x, 0
    elif h < 120:
        return x, c, 0
    elif h < 180:
        return 0, c, x
    elif h < 240:
        return 0, x, c
    elif h < 300:
        return x, 0, c
    return c, 0, x


def __validate_hsv_color(s: float, v: float) -> None:
    if s > 1.0 or s < 0:
        raise ValueError(f"Saturation value ({s}) is not in range from 0 to 1")
    if v > 1.0 or v < 0:
        raise ValueError(f"Value value ({v}) is not in range from 0 to 1")
