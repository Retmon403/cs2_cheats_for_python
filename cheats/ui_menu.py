from threading import Lock
import win32con


class UI_MENU:

    esp_box = True
    esp_bons = True
    aim_bot = True

    aim_bons = 0
    aim_items = [6, 5, 4]
    aim_select = 0

    aim_scope = 180
    aim_rcs = True
    aim_speed = 150
    vk_items = [win32con.VK_MENU, win32con.VK_LBUTTON,
                win32con.VK_RBUTTON]
    aim_key = 0
    key_select = 0

    trigger = True

    bhop = True
    bhop_delay_start = 15
    bhop_delay_end = 18
