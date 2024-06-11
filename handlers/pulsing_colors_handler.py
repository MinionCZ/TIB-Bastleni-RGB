from handlers.common_utils import hsv_to_rgb, NUMBER_OF_LEDS, leds, HUE_PERIOD

# Tento soubor slouží jako implementace módu, který se stará o pulsování barev duhy.


# Konstanty definující chování handleru pulsujicích barev
__HUE_STEP = 20.0  # Parametr udávajicí jak moc se změní barva na paletě oproti minulé (jak moc se posune H složka HSV)
__DEFAULT_SATURATION = 1.0  # Saturace barvy
__VALUE_STEPS = 100  # Kolik kroků je mezi úplně shasnutou barvou a plným rozsvícením
__MAX_VALUE = 1.0  # Maximální hodnota jasu
__PULSING_COLORS_DELAY_COEFFICIENT = 5  # Kolik tiků procesoru proběhne mezi změnami jasu o 1 položku

__delay_counter: int = 0
__hue: float = 0
__value_step: int = 0
__incrementing: bool = True


# Funkce obsluhujicí mód pulsování barev
def handle_pulsing_colors_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __make_pulse_step()
        __handle_value_changes()
    __delay_counter += 1
    __delay_counter %= __PULSING_COLORS_DELAY_COEFFICIENT


# Tato pomocná funkce se stará o správné napočítání HSV barvy na RGB a jejich zapsání na LEDky
def __make_pulse_step() -> None:
    global __hue, __value_step, __incrementing
    value = float(__value_step * __MAX_VALUE / __VALUE_STEPS)
    r, g, b = hsv_to_rgb(__hue, __DEFAULT_SATURATION, value)
    for i in range(NUMBER_OF_LEDS):
        leds[i] = g, r, b
    leds.write()


# Tato pomocná funkce se stará o změnu hodnot po každém kroku
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


# Tato funkce se stará o nastavení stavu do výchozí polohy
def clear_pulsing() -> None:
    global __hue, __value_step, __incrementing, __delay_counter
    __hue = 0
    __value_step = 0
    __incrementing = True
    __delay_counter = 0
