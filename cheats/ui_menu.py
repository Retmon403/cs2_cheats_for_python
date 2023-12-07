from threading import Lock
import win32con


class UI_MENU:

    esp_box = True
    esp_bons = True
    aim_bot = True
    aim_scope = 180
    aim_rcs = True
    aim_speed = 150
    vk_items = [win32con.VK_MENU, win32con.VK_LBUTTON,
                win32con.VK_RBUTTON]
    aim_key = 0
    key_select = 0

    def __init__(self) -> None:
        self.lock = Lock()
