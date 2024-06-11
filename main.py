from machine import Pin
import time
from device_mode import DeviceMode
import mode_peripherals
from handlers.hsv_transition_handler import handle_hsv_transition_mode
from handlers.pulsing_colors_handler import handle_pulsing_colors_mode
from handlers.rainbow_mode_handler import handle_rainbow_mode
from handlers.single_color_handler import handle_single_color_mode
from handlers.snake_handler import handle_snake_mode

__SLEEP_DURATION = 0.005  # Konstanta určujicí dobu spánku. Doba spánku nám zde vlastně pomáhá s časováním v různých efektech. Vzásadě nám to určuje jak často procesor kontroluje vstupy a výstupy. Dále by se to dalo představit jako tik procesoru

# Tento slovník (dict) funguje tak, že v sobě má vždy hodnotu klíč a odkaz na funkci. Tedy my jsme udělali slovník našich
# módů (klíč je mód) a funkcí, které se starají o daný mód (hodnota je odkaz na funkci).
__MODE_HANDLERS: dict = {
    DeviceMode.SINGLE_COLOR_MODE: handle_single_color_mode,
    DeviceMode.SNAKE_MODE: handle_snake_mode,
    DeviceMode.HSV_RAINBOW_MODE: handle_rainbow_mode,
    DeviceMode.PULSING_COLORS_MODE: handle_pulsing_colors_mode,
    DeviceMode.HSV_TRANSITION_MODE: handle_hsv_transition_mode,
}


# Tato funkce má za úkol se podívat do slovníku a najít nám podle klíče/módu příslušnou obslužnou funkci, která je potom zavolána
# Param mode příslušný mód zařízení ve kterém se zařízení právě nachází
def handle_rgb_mode(mode: DeviceMode) -> None:
    __MODE_HANDLERS[mode.mode]()


# Vstupní bod našeho programu. Odtud začíná hlavní (main) funkce
def main():
    mode = DeviceMode.read_mode()
    mode_peripherals.init_mode_peripherals()
    while True:
        handle_rgb_mode(mode)
        mode = DeviceMode.read_mode()
        time.sleep(__SLEEP_DURATION)


# Toto je zavolání naší funkce main. Tento if se stará o to, aby když je tento soubor spuštěný interpreterem, tak pokud je
# zvolen jako hlavní soubor (tedy není spuštěn jako modul), tak je tento if pravdivý a spustí nám hlavní funkci main
if __name__ == "__main__":
    main()
