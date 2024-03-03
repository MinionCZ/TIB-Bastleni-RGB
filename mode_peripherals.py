from machine import Pin

__LED_PIN_NUMBERS: list[int] = [5, 7, 8, 9, 13]
__LED_PINS: list[Pin] = [
    Pin(pin_number, Pin.OUT) for pin_number in __LED_PIN_NUMBERS
]

__INCREASE_MODE_PIN: Pin = Pin(21, Pin.IN, Pin.PULL_UP)
__DECREASE_MODE_PIN: Pin = Pin(20, Pin.IN, Pin.PULL_UP)


def init_mode_peripherals() -> None:
    # TODO Tady to musíme naprogramovat :)
    pass