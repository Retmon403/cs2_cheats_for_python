from threading import Lock
import win32con


class UI_MENU:

    esp_box = True
    esp_info = True
    esp_bons = False
    aim_bot = True

    rcs_inhibit = 2.1
    aim_bons = 0
    aim_items = [6, 5, 4]
    aim_select = 0

    aim_scope = 150
    aim_rcs = True
    aim_speed = 150
    vk_items = [win32con.VK_MENU, win32con.VK_LBUTTON,
                win32con.VK_RBUTTON]
    aim_key = 0
    key_select = 0

    trigger = True
    trigger_time = 120

    bhop = True
    bhop_delay_start = 15
    bhop_delay_end = 18
