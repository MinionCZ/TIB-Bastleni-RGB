from machine import Pin
from device_mode import DeviceMode
import time

from handlers.hsv_transition_handler import clear_transition
from handlers.pulsing_colors_handler import clear_pulsing
from handlers.rainbow_mode_handler import clear_rainbow
from handlers.snake_handler import clear_snake_status

# Zde se nastavují periferie

__LED_PIN_NUMBERS: list[int] = [5, 7, 8, 9, 10]
__LED_PINS: list[Pin] = [
    Pin(pin_number, Pin.OUT) for pin_number in __LED_PIN_NUMBERS
]
__BUTTON_DEBOUNCE_TIME_MS: int = 250

__INCREASE_MODE_PIN: Pin = Pin(20, Pin.IN, Pin.PULL_UP)
__DECREASE_MODE_PIN: Pin = Pin(21, Pin.IN, Pin.PULL_UP)

# Zde se nachazí proměnné držící stav
# Tato proměnná slouží pro debouncing tlačítka co zvyšuje mód. Debouncing je to, že když zaznamenáme stisknutí tlačítka, tak kontakty uvnitř tlačítka vibrují a může se stát, že nám to mikrořadič zaznamená jako vícero stisknutí.
# Proto se dělá tzv debouncing, který si pamatuje kdy bylo zaznamenáno poslední kliknutí a pokud nynější kliknutí je blíže, než tzv debounce time, tak ho ignoruje
__increase_mode_last_debounce_time: int = 0
# Tato proměnná slouží pro debouncing tlačítka snižujicí mód
__decrease_mode_last_debounce_time: int = 0

__actual_mode = DeviceMode.read_mode()


# Funkce, která ma za úkol inicializovat periferie
def init_mode_peripherals() -> None:
    __turn_on_led_by_mode(__actual_mode)
    __DECREASE_MODE_PIN.irq(__handle_mode_decrease, trigger=Pin.IRQ_FALLING)
    __INCREASE_MODE_PIN.irq(__handle_mode_increase, trigger=Pin.IRQ_FALLING)


# Pomocná funkce pro vypnutí všech ledek značící mód
def __turn_off_leds() -> None:
    for led in __LED_PINS:
        led.off()


# Tato funkce projde všechny ledky a zapne tu správnou podle zvoleného módu
def __turn_on_led_by_mode(device_mode: DeviceMode) -> None:
    for index, led in enumerate(__LED_PINS):
        if device_mode.mode == index:
            led.on()
        else:
            led.off()


# Funkce vracejicí počet milisekund od startu zařízení
def __get_millis() -> int:
    return time.time_ns() // 1_000_000


# Tato funkce slouží jako takzvaný handler (obsluha) pinu. Funguje to tak, že když uživatel stlačí tlačítko, tak procesor dostane takzvané přerušení, že někdo stiskl tlačítko a měl by se tomu věnovat. On v odpovědi na tuto událost zavolá naši funkci, která se o to postará.
# Po stisknutí tlačítka funkce ověří, že se nejedná o stisk vyvolaný bouncingem tlačítka a pokud se nejedná tak sníží o 1 mód
def __handle_mode_decrease(pin: Pin) -> None:
    print("Decreasing mode")
    global __decrease_mode_last_debounce_time
    if __decrease_mode_last_debounce_time + __BUTTON_DEBOUNCE_TIME_MS > __get_millis():
        return
    __decrease_mode_last_debounce_time = __get_millis()
    global __actual_mode
    __actual_mode = __actual_mode.decrease_mode_and_save()
    __turn_on_led_by_mode(__actual_mode)
    # __clear_states()


# Tato funkce po stisknutí tlačítka zvýší mód o 1
def __handle_mode_increase(pin: Pin) -> None:
    print("Increasing mode")
    global __increase_mode_last_debounce_time
    if __increase_mode_last_debounce_time + __BUTTON_DEBOUNCE_TIME_MS > __get_millis():
        return
    __increase_mode_last_debounce_time = __get_millis()
    global __actual_mode
    __actual_mode = __actual_mode.increase_mode_and_save()
    __turn_on_led_by_mode(__actual_mode)
    # __clear_states()


# Tato pomocná funkce je volána při změně módu. Slouží k tomu, aby nám vynulovala stav jednotlivých handlerů pro módy. Tedy například u hada máme informaci o tom, kde má hlavu a kam jede a aby nám vždy had začínal od začátku tak je potřeba tyto informace ve správnou chvíli nastavit na výchozí hodnotu.
def __clear_states() -> None:
    clear_transition()
    clear_rainbow()
    clear_snake_status()
    clear_pulsing()
