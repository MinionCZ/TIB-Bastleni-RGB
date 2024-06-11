import os


# Tato třída má v sobě zadefinované jednotlivé módy a stará se o držení stavu v jakém módu se zařízení nachází.
# Data si drží tak, že si vytvoří (pokud neexistuje) adresář data a v něm soubor mode.txt do kterého si uloží aktuální mód
class DeviceMode:
    SINGLE_COLOR_MODE: int = 0
    PULSING_COLORS_MODE: int = 1
    HSV_RAINBOW_MODE: int = 2
    HSV_TRANSITION_MODE: int = 3
    SNAKE_MODE: int = 4
    __MODE_SAVING_FILE_NAME: str = "mode.txt"
    __MODE_SAVING_DIRECTORY: str = "data"
    __MODE_SAVING_PATH = f"/{__MODE_SAVING_DIRECTORY}/{__MODE_SAVING_FILE_NAME}"
    __AVAILABLE_MODES: frozenset[int] = frozenset([SINGLE_COLOR_MODE,
                                                   PULSING_COLORS_MODE,
                                                   HSV_RAINBOW_MODE,
                                                   HSV_TRANSITION_MODE,
                                                   SNAKE_MODE])

    __DEFAULT_MODE = SINGLE_COLOR_MODE

    def __init__(self, mode: int) -> None:
        if mode not in self.__AVAILABLE_MODES:
            raise ValueError(f"Mode passed as parameter {mode} is invalid and should be in {self.__AVAILABLE_MODES}")
        self.mode = mode

    # Tato metoda slouží k uložení aktuálního módu drženého touto třídou do flash paměti (na pevný disk)
    def save_mode(self) -> 'DeviceMode':
        if not self.__check_if_saving_file_exists():
            os.mkdir(DeviceMode.__MODE_SAVING_DIRECTORY)
        with open(DeviceMode.__MODE_SAVING_PATH, "w") as output:
            output.write(str(self.mode))
        return self

    # Tato metoda slouží k inkrementaci a následnému uložení aktuálního módu drženého touto třídou do flash paměti (na pevný disk)
    def increase_mode_and_save(self, allow_overflow: bool = True) -> 'DeviceMode':
        if allow_overflow:
            self.mode += 1
            self.mode %= len(DeviceMode.__AVAILABLE_MODES)
        else:
            self.mode += 1
            if self.mode not in DeviceMode.__AVAILABLE_MODES:
                raise ValueError(f"Error occurred during increasing of value of mode {self.mode}")
        self.save_mode()
        return self

    # Tato metoda slouží k dekrementaci a následnému uložení aktuálního módu drženého touto třídou do flash paměti (na pevný disk)
    def decrease_mode_and_save(self, allow_overflow: bool = True) -> 'DeviceMode':
        if allow_overflow:
            self.mode -= 1
            self.mode = len(DeviceMode.__AVAILABLE_MODES) - 1 if self.mode < 0 else self.mode
        else:
            self.mode -= 1
            if self.mode not in DeviceMode.__AVAILABLE_MODES:
                raise ValueError(f"Error occurred during decreasing of value of mode {self.mode}")
        self.save_mode()
        return self

    def __check_if_saving_file_exists(self) -> bool:
        try:
            os.stat(self.__MODE_SAVING_PATH)
            return True
        except OSError:
            return False

    def __str__(self) -> str:
        return f"Mode: {self.mode}"

    # Tato třídní metodu si přečte z flash paměti uloženou hodnotu a vrátí novou instanci této třídy
    @classmethod
    def read_mode(cls) -> 'DeviceMode':
        try:
            with open(DeviceMode.__MODE_SAVING_PATH, "r") as inpt:
                try:
                    return DeviceMode(int(inpt.read()))
                except RuntimeError as e:
                    print(
                        f"""Error occurred during parsing saved mode from file. Default value will be used instead. Here is
                        error: {e}""")
                    return DeviceMode(DeviceMode.__DEFAULT_MODE).save_mode()
        except OSError:
            print("File with mode is not yet prepared so it will be saved now with default values")
            return DeviceMode(DeviceMode.__DEFAULT_MODE).save_mode()
