from src.handlers.common_utils import NUMBER_OF_LEDS, leds, hsv_to_rgb, HUE_PERIOD

# Zde jsou nadefinovány konstanty ovlivňujicí duhu
__RAINBOW_DELAY_COEFFICIENT = 4  # Parametr duhy, který ovlivňuje kolik tiků procesoru bude duha stát. Tedy v základním nastavení 4 tiky stojí
__DEFAULT_SATURATION = 1.0  # Nastavení sytosti barev duhy
__DEFAULT_VALUE = 1.0  # Nastavení jasu barev duhy
__HUE_INCREMENT = HUE_PERIOD / NUMBER_OF_LEDS

__rainbow_start_index = 0
__delay_counter = 0


# Hlavní funkce dělajicí obsluhu duhového módu
def handle_rainbow_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __show_rainbow()
    __delay_counter += 1
    __delay_counter %= __RAINBOW_DELAY_COEFFICIENT


# Pomocná funkce pro zobrazení duhy na pásek. Duha funguje tak, že se zobrazuje celé spektru HSV formátu, akorát vždy spektrum začíná od jiné ledky, tím je zajištěn pohyb duhy
def __show_rainbow() -> None:
    global __rainbow_start_index
    for i in range(NUMBER_OF_LEDS):
        led_index = (i + __rainbow_start_index) % NUMBER_OF_LEDS
        r, g, b = hsv_to_rgb(i * __HUE_INCREMENT, __DEFAULT_SATURATION, __DEFAULT_VALUE)
        leds[led_index] = g, r, b
    leds.write()
    __rainbow_start_index += 1
    __rainbow_start_index %= NUMBER_OF_LEDS


# Funkce pro uvedení stavu handleru do výchozího
def clear_rainbow() -> None:
    global __rainbow_start_index, __delay_counter
    __rainbow_start_index = 0
    __delay_counter = 0
