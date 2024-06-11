from handlers.common_utils import NUMBER_OF_LEDS, leds, hsv_to_rgb, HUE_PERIOD

# Tento soubor slouží pro obsluhu módu, který se stará o postupné zobrazení všech barev duhy na pásce (všech barev v HSV).
# Princip je takový, že se posuptně cyklicky příčítá konstanta k HUE a tím dochází k postupným změnám barev

# Konstanty pro nastavení chování změn barev na pásce
__HUE_STEP = 3.0  # Krok změny HUE, větší krok = rychlejší změna barev
__DEFAULT_SATURATION = 1.0  # Saturace odstínu barvy
__DEFAULT_VALUE = 1.0  # Jas barvy
__HSV_TRANSITION_DELAY_COEFFICIENT = 6  # Zpomalovací koeficient

__delay_counter = 0
__hue = 0


# Tato funkce se stará o handlování tiku procesoru
def handle_hsv_transition_mode() -> None:
    global __delay_counter
    if __delay_counter == 0:
        __make_transition_step()
    __delay_counter += 1
    __delay_counter %= __HSV_TRANSITION_DELAY_COEFFICIENT


# Tato pomocná funkce se stará o udělání kroku v H hodnotě v barvě HSV
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
