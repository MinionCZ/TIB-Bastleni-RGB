from handlers.common_utils import get_user_selected_colors, NUMBER_OF_LEDS, leds


# Tento soubor představuje handler pro jednu barvu zadanou uživatelem pomocí potenciometrů

# Funkce pro obsluhu jedné barvy zadané od uživatele pomocí potenciometrů
def handle_single_color_mode() -> None:
    red, green, blue = get_user_selected_colors()
    for i in range(NUMBER_OF_LEDS):
        leds[i] = (green, red, blue)
    leds.write()
