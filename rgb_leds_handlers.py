from neopixel import NeoPixel
from machine import Pin, ADC

__RGB_LEDS_PIN: Pin = Pin(15, Pin.OUT)
__NUMBER_OF_LEDS = 60
__red_potentiometer = ADC(Pin(26, Pin.IN))
__green_potentiometer = ADC(Pin(27, Pin.IN))
__blue_potentiometer = ADC(Pin(28, Pin.IN))

__leds = NeoPixel(__RGB_LEDS_PIN, __NUMBER_OF_LEDS)

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
