import time
from cheats.gdi import *
from cheats.hacker import *
from cheats.player import *
from cheats.core import *
from cheats.myimgui import *
from cheats.ui_menu import *
from cheats.offset import *
# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

# 2023/12/7
# 英语很烂，所以变量和函数命名比较随意，但代码逻辑还是很精简的
# 1.很努力的优化gdi让他可以流畅的绘图而不会出现闪框
# 2.加入了平滑自瞄，加入了自动更新offset
# 3.优化了运行效率，修了一些bug
# 还想加许多功能，但我担心Python跑起来太卡

# config
UPDATE_OFFSET = True
# config

if __name__ == '__main__':

    hack = Hacker()
    if not hack.init_data():
        set_error('pls run game!')

    if UPDATE_OFFSET:
        if not hack.update_offset():
            set_error('update offset failed...')
    # cs2 被打开
    print('create gdi context')
    draw = GDI(hwnd=hack.hwnd, hide=False)
    esp = ESP(hack, draw)
    aimbot = AimBot(hack, draw)

    def Menu():
        imgui.set_next_window_size(300, 200, imgui.FIRST_USE_EVER)
        imgui.begin('python cs2 cheats[lyx]', True)

        UI_MENU.esp_box = imgui.checkbox('EspBox', UI_MENU.esp_box)[1]
        imgui.same_line()
        UI_MENU.esp_bons = imgui.checkbox('EspBons', UI_MENU.esp_bons)[1]

        imgui.separator()
        UI_MENU.aim_bot = imgui.checkbox('AimBot', UI_MENU.aim_bot)[1]
        imgui.same_line()
        UI_MENU.aim_rcs = imgui.checkbox('Rcs', UI_MENU.aim_rcs)[1]

        items = ["Alt", "MouseLeft", "MouseRight"]

        with imgui.begin_combo("AimKey", items[UI_MENU.key_select]) as combo:
            if combo.opened:
                for i, item in enumerate(items):
                    is_selected = (i == UI_MENU.key_select)
                    if imgui.selectable(item, is_selected)[0]:
                        UI_MENU.key_select = i
                    if is_selected:
                        imgui.set_item_default_focus()
        UI_MENU.aim_key = UI_MENU.vk_items[UI_MENU.key_select]

        UI_MENU.aim_scope = imgui.slider_int(
            'AimScope', UI_MENU.aim_scope, 1, 500)[1]

        UI_MENU.aim_speed = imgui.slider_int(
            'AimSpeed', UI_MENU.aim_speed, 1, 300)[1]

        draw.BeginGdi()
        aimbot.work(esp.work())
        draw.EndGdi()
        imgui.end()
        time.sleep(0.002)

    MyImGui().set_draw_callback(Menu).run()
    '''if win32gui.PeekMessage(None, 0, 0, 0):
        win32gui.PumpWaitingMessages()'''
