import time
from cheats.gdi import *
from cheats.hacker import *
from cheats.player import *
from cheats.core import *
from cheats.myimgui import *
from cheats.ui_menu import *
from cheats.offset import *
import threading
# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main
# Cs2Dump https://github.com/a2x/cs2-dumper

# ==========================================================
# 2023/12/7
# 英语很烂，所以变量和函数命名比较随意，但代码逻辑还是很精简的
# 1.很努力的优化gdi让他可以流畅的绘图而不会出现闪框
# 2.加入了平滑自瞄，加入了自动更新offset
# 3.优化了运行效率，修了一些bug
# 还想加许多功能，但我担心Python跑起来太卡
# ==========================================================
# 2024/2/20
# 修复了偏移定位使用的特征码
# 使用了最新的cs2dump client偏移数据
# 增加了连跳和自动扳机
# 添加了瞄准部位选项
# offset在成功获取到后会被储存进文件
# 一些bug修复和性能优化

# config
UPDATE_OFFSET = True
# 如果UPDATE_OFFSET==True 会动态获取偏移
# 否则不会动态获取偏移，而是读取本地存取的config文件
# config

if __name__ == '__main__':

    hack = Hacker()
    if not hack.init_data():
        set_error('pls run game!')

    if UPDATE_OFFSET:
        if not hack.update_offset():
            set_error('update offset failed...')
        else:
            Config.save_offset(Offset.dwEntityList,
                               Offset.dwLocalPlayerController, Offset.dwViewMatrix, Offset.dwViewAngles, Offset.dwViewAngles_Add, Offset.dwForceAttack, Offset.dwForceJump)
    else:
        Config.read_offset()
    # cs2 被打开
    print('create gdi context')
    draw = GDI(hwnd=hack.hwnd, hide=False)
    esp = ESP(hack, draw)
    aimbot = AimBot(hack, draw)

    threading.Thread(target=Trigger.loop, args=(hack,)).start()
    threading.Thread(target=Bhop.loop, args=(hack,)).start()

    def Menu():
        imgui.set_next_window_size(400, 200, imgui.FIRST_USE_EVER)
        imgui.begin('python cs2 cheats[lyx]', True)

        UI_MENU.esp_box = imgui.checkbox('EspBox', UI_MENU.esp_box)[1]
        imgui.same_line()
        UI_MENU.esp_bons = imgui.checkbox('EspBons', UI_MENU.esp_bons)[1]

        imgui.separator()
        UI_MENU.aim_bot = imgui.checkbox('AimBot', UI_MENU.aim_bot)[1]
        imgui.same_line()
        UI_MENU.aim_rcs = imgui.checkbox('Rcs', UI_MENU.aim_rcs)[1]
        imgui.same_line()
        UI_MENU.trigger = imgui.checkbox('Trigger', UI_MENU.trigger)[1]
        imgui.same_line()
        UI_MENU.bhop = imgui.checkbox('Bhop[VK_CAPITAL]', UI_MENU.bhop)[1]

        vk_items = ["Alt", "MouseLeft", "MouseRight"]
        with imgui.begin_combo("AimKey", vk_items[UI_MENU.key_select]) as combo:
            if combo.opened:
                for i, item in enumerate(vk_items):
                    is_selected = (i == UI_MENU.key_select)
                    if imgui.selectable(item, is_selected)[0]:
                        UI_MENU.key_select = i
                    if is_selected:
                        imgui.set_item_default_focus()
        UI_MENU.aim_key = UI_MENU.vk_items[UI_MENU.key_select]

        aim_items = ["Head", "Nick", "Chest"]
        with imgui.begin_combo("AimBons", aim_items[UI_MENU.aim_select]) as combo:
            if combo.opened:
                for i, item in enumerate(aim_items):
                    is_selected = (i == UI_MENU.aim_select)
                    if imgui.selectable(item, is_selected)[0]:
                        UI_MENU.aim_select = i
                    if is_selected:
                        imgui.set_item_default_focus()
        UI_MENU.aim_bons = UI_MENU.aim_items[UI_MENU.aim_select]

        UI_MENU.aim_scope = imgui.slider_int(
            'AimScope', UI_MENU.aim_scope, 1, 500)[1]

        UI_MENU.aim_speed = imgui.slider_int(
            'AimSpeed', UI_MENU.aim_speed, 1, 300)[1]

        draw.BeginGdi()
        aimbot.work(esp.work())
        draw.EndGdi()
        imgui.end()
        time.sleep(0.001)

    MyImGui().set_draw_callback(Menu).run()
    '''if win32gui.PeekMessage(None, 0, 0, 0):
        win32gui.PumpWaitingMessages()'''
