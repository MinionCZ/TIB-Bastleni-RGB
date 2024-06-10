from neopixel import NeoPixel
from machine import Pin, ADC

__RGB_LEDS_PIN: Pin = Pin(15, Pin.OUT)
__NUMBER_OF_LEDS = 60
__red_potentiometer = ADC(Pin(26, Pin.IN))
__green_potentiometer = ADC(Pin(27, Pin.IN))
__blue_potentiometer = ADC(Pin(28, Pin.IN))

__leds = NeoPixel(__RGB_LEDS_PIN, __NUMBER_OF_LEDS)

__MAX_COLOR_VALUE = 255
HUE_PERIOD = 360.0

__SNAKE_LENGTH = 10
__SNAKE_SPEED_COEFFICIENT = 3
__snake_head_position: int = __SNAKE_LENGTH - 1
__snake_going_forward: bool = True
__snake_delay_counter: int = 0


def __convert_potentiometer_reading_to_color(value: int) -> int:
    linear_value = 10 ** (value / 65535)
    percentage = (linear_value - 1) / 9
    return int(255 * percentage)


def __get_user_selected_colors() -> (int, int, int):
    red_potentiometer_value = __red_potentiometer.read_u16()
    red = __convert_potentiometer_reading_to_color(red_potentiometer_value)
    green_potentiometer_value = __green_potentiometer.read_u16()
    green = __convert_potentiometer_reading_to_color(green_potentiometer_value)
    blue_potentiometer_value = __blue_potentiometer.read_u16()
    blue = __convert_potentiometer_reading_to_color(blue_potentiometer_value)
    return red, green, blue


def handle_single_color_mode() -> None:
    red, green, blue = __get_user_selected_colors()
    for i in range(__NUMBER_OF_LEDS):
        __leds[i] = (green, red, blue)
    __leds.write()


def handle_snake_mode() -> None:
    global __snake_head_position, __snake_going_forward, __snake_delay_counter
    if __snake_delay_counter < __SNAKE_SPEED_COEFFICIENT:
        __snake_delay_counter += 1
        return
    __snake_delay_counter = 0
    __handle_snake_movement()
    __draw_snake()
    __snake_head_position = __snake_head_position + 1 if __snake_going_forward else __snake_head_position - 1


def handle_rainbow_mode() -> None:
    print("handling rainbow mode")


def handle_pulsing_single_color_mode() -> None:
    print("handling pulsing single color mode")


def handle_hsv_transition_mode() -> None:
    print("handling hsv transition mode")


def clear_status() -> None:
    global __snake_head_position, __snake_going_forward
    __snake_head_position: int = __SNAKE_LENGTH - 1
    __snake_going_forward = True


def __handle_snake_movement() -> None:
    global __snake_head_position, __snake_going_forward, __snake_delay_counter
    if __snake_head_position == __NUMBER_OF_LEDS + __SNAKE_LENGTH - 1:
        __snake_head_position = __NUMBER_OF_LEDS - 1
        __snake_going_forward = False
    elif __snake_head_position == - __SNAKE_LENGTH + 1:
        __snake_head_position = 0
        __snake_going_forward = True


def __draw_snake() -> None:
    red, green, blue = __get_user_selected_colors()
    coefficient = 1 / __SNAKE_LENGTH

    def write_to_led(index: int, start_write_index: int, end_write_index: int) -> float:
        if start_write_index <= index <= end_write_index:
            __leds[i] = (int(green * coefficient), int(red * coefficient), int(blue * coefficient))
            return 1 / __SNAKE_LENGTH
        else:
            __leds[i] = (0, 0, 0)
        return 0

    if __snake_going_forward:
        start = __snake_head_position - __SNAKE_LENGTH + 1
        for i in range(__NUMBER_OF_LEDS):
            coefficient += write_to_led(i, start, __snake_head_position)
    else:
        end = __snake_head_position + __SNAKE_LENGTH - 1
        for i in range(__NUMBER_OF_LEDS - 1, -1, -1):
            coefficient += write_to_led(i, __snake_head_position, end)
    __leds.write()


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
