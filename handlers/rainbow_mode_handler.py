from handlers.common_utils import NUMBER_OF_LEDS, leds, hsv_to_rgb, HUE_PERIOD

__RAINBOW_DELAY_COEFFICIENT = 5
__DEFAULT_SATURATION = 1.0
__DEFAULT_VALUE = 1.0
__HUE_INCREMENT = HUE_PERIOD / NUMBER_OF_LEDS

__rainbow_start_index = 0
__delay_counter = 0


def handle_rainbow_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __show_rainbow()
    __delay_counter += 1
    __delay_counter %= __RAINBOW_DELAY_COEFFICIENT


def __show_rainbow() -> None:
    global __rainbow_start_index
    for i in range(NUMBER_OF_LEDS):
        led_index = (i + __rainbow_start_index) % NUMBER_OF_LEDS
        leds[led_index] = hsv_to_rgb(i * __HUE_INCREMENT, __DEFAULT_SATURATION, __DEFAULT_VALUE)
    leds.write()
    __rainbow_start_index += 1
    __rainbow_start_index %= NUMBER_OF_LEDS


def clear_rainbow() -> None:
    global __rainbow_start_index, __delay_counter
    __rainbow_start_index = 0
    __delay_counter = 0
