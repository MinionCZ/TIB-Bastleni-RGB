from handlers.common_utils import hsv_to_rgb, NUMBER_OF_LEDS, leds, HUE_PERIOD

__HUE_STEP = 20.0
__DEFAULT_SATURATION = 1.0
__VALUE_STEPS = 100
__MAX_VALUE = 1.0
__PULSING_COLORS_DELAY_COEFFICIENT = 5

__delay_counter: int = 0
__hue: float = 0
__value_step: int = 0
__incrementing: bool = True


def handle_pulsing_colors_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __make_pulse_step()
        __handle_value_changes()
    __delay_counter += 1
    __delay_counter %= __PULSING_COLORS_DELAY_COEFFICIENT


def __make_pulse_step() -> None:
    global __hue, __value_step, __incrementing
    value = float(__value_step * __MAX_VALUE / __VALUE_STEPS)
    r, g, b = hsv_to_rgb(__hue, __DEFAULT_SATURATION, value)
    for i in range(NUMBER_OF_LEDS):
        leds[i] = g, r, b
    leds.write()


def __handle_value_changes() -> None:
    global __value_step, __incrementing, __hue
    if __incrementing:
        if __value_step < __VALUE_STEPS:
            __value_step += 1
        else:
            __incrementing = False
    else:
        if __value_step > 0:
            __value_step -= 1
        else:
            __incrementing = True
            __hue += __HUE_STEP
            __hue %= HUE_PERIOD


def clear_pulsing() -> None:
    global __hue, __value_step, __incrementing, __delay_counter
    __hue = 0
    __value_step = 0
    __incrementing = True
    __delay_counter = 0
