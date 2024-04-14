from machine import Pin
from device_mode import DeviceMode
import time

__LED_PIN_NUMBERS: list[int] = [5, 7, 8, 9, 10]
__LED_PINS: list[Pin] = [
    Pin(pin_number, Pin.OUT) for pin_number in __LED_PIN_NUMBERS
]
__BUTTON_DEBOUNCE_TIME_MS: int = 250

__INCREASE_MODE_PIN: Pin = Pin(20, Pin.IN, Pin.PULL_UP)
__DECREASE_MODE_PIN: Pin = Pin(21, Pin.IN, Pin.PULL_UP)

__increase_mode_last_debounce_time: int = 0
__decrease_mode_last_debounce_time: int = 0

__actual_mode = DeviceMode.read_mode()


def init_mode_peripherals() -> None:
    __turn_on_led_by_mode(__actual_mode)
    __DECREASE_MODE_PIN.irq(__handle_mode_decrease, trigger=Pin.IRQ_FALLING)
    __INCREASE_MODE_PIN.irq(__handle_mode_increase, trigger=Pin.IRQ_FALLING)


def __turn_off_leds() -> None:
    for led in __LED_PINS:
        led.off()


def __turn_on_led_by_mode(device_mode: DeviceMode) -> None:
    for index, led in enumerate(__LED_PINS):
        if device_mode.mode == index:
            led.on()
        else:
            led.off()


def __get_millis() -> int:
    return time.time_ns() // 1_000_000


def __handle_mode_decrease(pin: Pin) -> None:
    print("Decreasing mode")
    global __decrease_mode_last_debounce_time
    if __decrease_mode_last_debounce_time + __BUTTON_DEBOUNCE_TIME_MS > __get_millis():
        return
    __decrease_mode_last_debounce_time = __get_millis()
    global __actual_mode
    __actual_mode = __actual_mode.decrease_mode_and_save()
    __turn_on_led_by_mode(__actual_mode)


def __handle_mode_increase(pin: Pin) -> None:
    print("Increasing mode")
    global __increase_mode_last_debounce_time
    if __increase_mode_last_debounce_time + __BUTTON_DEBOUNCE_TIME_MS > __get_millis():
        return
    __increase_mode_last_debounce_time = __get_millis()
    global __actual_mode
    __actual_mode = __actual_mode.increase_mode_and_save()
    __turn_on_led_by_mode(__actual_mode)
