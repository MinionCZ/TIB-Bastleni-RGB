import os


class DeviceMode:
    SINGLE_COLOR_MODE: int = 0
    PULSING_SINGLE_COLOR_MODE: int = 1
    HSV_RAINBOW_MODE: int = 2
    HSV_TRANSITION_MODE: int = 3
    SNAKE_MODE: int = 4
    __MODE_SAVING_FILE_NAME: str = "mode.txt"
    __MODE_SAVING_DIRECTORY: str = "data"
    __MODE_SAVING_PATH = f"/{__MODE_SAVING_DIRECTORY}/{__MODE_SAVING_FILE_NAME}"
    __AVAILABLE_MODES: frozenset[int] = frozenset([SINGLE_COLOR_MODE,
                                                   PULSING_SINGLE_COLOR_MODE,
                                                   HSV_RAINBOW_MODE,
                                                   HSV_TRANSITION_MODE,
                                                   SNAKE_MODE])

    __DEFAULT_MODE = SINGLE_COLOR_MODE

    def __init__(self, mode: int) -> None:
        if mode not in self.__AVAILABLE_MODES:
            raise ValueError(f"Mode passed as parameter {mode} is invalid and should be in {self.__AVAILABLE_MODES}")
        self.mode = mode

    def save_mode(self) -> DeviceMode:
        if not self.__check_if_saving_file_exists():
            os.mkdir(DeviceMode.__MODE_SAVING_DIRECTORY)
        with open(DeviceMode.__MODE_SAVING_PATH, "w") as output:
            output.write(str(self.mode))
        return self

    def __check_if_saving_file_exists(self) -> bool:
        try:
            os.stat(self.__MODE_SAVING_PATH)
            return True
        except OSError:
            return False

    def __str__(self) -> str:
        return f"Mode: {self.mode}"

    @classmethod
    def read_mode(cls) -> DeviceMode:
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
