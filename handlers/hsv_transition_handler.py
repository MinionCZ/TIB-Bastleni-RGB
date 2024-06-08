from handlers.common_utils import NUMBER_OF_LEDS, leds, hsv_to_rgb, HUE_PERIOD

__HUE_STEP = 3.0
__DEFAULT_SATURATION = 1.0
__DEFAULT_VALUE = 1.0
__HSV_TRANSITION_DELAY_COEFFICIENT = 5

__delay_counter = 0
__hue = 0


def handle_hsv_transition_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __make_transition_step()
    __delay_counter += 1
    __delay_counter %= __HSV_TRANSITION_DELAY_COEFFICIENT


def __make_transition_step() -> None:
    global __hue
    r, g, b = hsv_to_rgb(__hue, __DEFAULT_SATURATION, __DEFAULT_VALUE)
    for i in range(NUMBER_OF_LEDS):
        leds[i] = g, r, b
    leds.write()
    __hue += __HUE_STEP
    __hue %= HUE_PERIOD


def clear_transition() -> None:
    global __delay_counter, __hue
    __delay_counter = 0
    __hue = 0
