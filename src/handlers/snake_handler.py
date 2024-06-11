from src.handlers.common_utils import get_user_selected_colors, leds, NUMBER_OF_LEDS

# Parametry pro nastavení chování hada
__SNAKE_LENGTH = 10  # Délka hada v počtu ledek na pásku
__SNAKE_SPEED_COEFFICIENT = 3  # Toto je zpomalovací konstanta, která se stará o změnu rychlosti hada. Tato konstanta nám říká, kolik tiků procesoru má had vynechat před tím, než se posune. Výchozí hodnota jsou 3. Čím vyšší hodnota, tím had pojede pomaleji
__snake_head_position: int = __SNAKE_LENGTH - 1
__snake_going_forward: bool = True
__snake_delay_counter: int = 0


# Tato funkce slouží jako hlavní obsluha hadího módu
def handle_snake_mode() -> None:
    global __snake_head_position, __snake_going_forward, __snake_delay_counter
    if __snake_delay_counter < __SNAKE_SPEED_COEFFICIENT:
        __snake_delay_counter += 1
        return
    __snake_delay_counter = 0
    __handle_snake_movement()
    __draw_snake()
    __snake_head_position = __snake_head_position + 1 if __snake_going_forward else __snake_head_position - 1


# Tato pomocná funkce se stará o správný pohyb hada. Tedy posouvá index hlavy
def __handle_snake_movement() -> None:
    global __snake_head_position, __snake_going_forward, __snake_delay_counter
    if __snake_head_position == NUMBER_OF_LEDS + __SNAKE_LENGTH - 1:
        __snake_head_position = NUMBER_OF_LEDS - 1
        __snake_going_forward = False
    elif __snake_head_position == - __SNAKE_LENGTH + 1:
        __snake_head_position = 0
        __snake_going_forward = True


# Tato pomocná funkce má za úkol vykreslit hada na pásku. Hada kreslí tak, že čím jsou ledky dál od hlavy k ocasu tak tím svítí méně, aby byl docílen efekt hada
def __draw_snake() -> None:
    red, green, blue = get_user_selected_colors()
    coefficient = 1 / __SNAKE_LENGTH

    def write_to_led(index: int, start_write_index: int, end_write_index: int) -> float:
        if start_write_index <= index <= end_write_index:
            leds[i] = (int(green * coefficient), int(red * coefficient), int(blue * coefficient))
            return 1 / __SNAKE_LENGTH
        else:
            leds[i] = (0, 0, 0)
        return 0

    if __snake_going_forward:
        start = __snake_head_position - __SNAKE_LENGTH + 1
        for i in range(NUMBER_OF_LEDS):
            coefficient += write_to_led(i, start, __snake_head_position)
    else:
        end = __snake_head_position + __SNAKE_LENGTH - 1
        for i in range(NUMBER_OF_LEDS - 1, -1, -1):
            coefficient += write_to_led(i, __snake_head_position, end)
    leds.write()


# Tato funkce slouží k nastavení stavu hada do výchozí polohy
def clear_snake_status() -> None:
    global __snake_head_position, __snake_going_forward
    __snake_head_position: int = __SNAKE_LENGTH - 1
    __snake_going_forward = True
