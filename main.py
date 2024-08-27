import threading

from cheats.core import *
from cheats.entity import *
from cheats.myimgui import *

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
# ==========================================================
# 2024/2/21
# 增加了EspInfo(player_weapon,player_name,player_health)
# 增加了rcs抑制控制滑块
# 增加了trigger持续时间控制滑块
# 修复了trigger效率问题
# 一些bug修复和性能优化
# ps：感谢大家的使用,如果您需要自己修改偏移量，只需修改client.py内的内容 并将UPDATE_OFFSET设置为false，再修改offset_config文件内的偏移
# ==========================================================
# 2024/2/22
# Entity增加显示掉落物实体，穷举遍历非常影响性能
# 更好的连跳
# 性能优化
# ==========================================================
# 2024/8/27
# 大家过的还好吗，这个夏天非常热
# 由于这是外部，py也无法编译dll，所以我想加入些更变态的功能很困难，比如hook input内的函数...
# 更新了偏移量，优化了代码

# config
UPDATE_OFFSET = False
# 如果UPDATE_OFFSET==True 会动态获取偏移
# 否则不会动态获取偏移，而是读取本地存取的config文件
# config

if __name__ == '__main__':

    # print(ClientOffset('CBasePlayerController.m_bIsHLTV'))

    hack = Hacker()
    if not hack.init_data():
        set_error('pls run game!')

    if UPDATE_OFFSET:
        if not hack.update_offset():
            set_error('update offset failed...')
        else:
            Config.save_offset(Offset.dwEntityList,
                               Offset.dwLocalPlayerController, Offset.dwViewMatrix, Offset.dwViewAngles,
                               Offset.dwViewAngles_Add, Offset.dwForceAttack, Offset.dwForceJump)
    else:
        Config.read_offset()
    # cs2 被打开
    Log('create gdi context')
    draw = GDI(hwnd=hack.hwnd, hide=False)
    esp = ESP(hack, draw)
    aimbot = AimBot(hack, draw)

    threading.Thread(target=Trigger.loop, args=(hack,)).start()
    threading.Thread(target=Bhop.loop, args=(hack,)).start()


    def Menu():
        imgui.set_next_window_size(400, 350, imgui.FIRST_USE_EVER)
        imgui.begin('python cs2 cheats[lyx]', True)

        UI_MENU.esp_box = imgui.checkbox('EspBox', UI_MENU.esp_box)[1]
        imgui.same_line()
        UI_MENU.esp_bons = imgui.checkbox('EspBons', UI_MENU.esp_bons)[1]
        imgui.same_line()
        UI_MENU.esp_info = imgui.checkbox('EspInfo', UI_MENU.esp_info)[1]
        imgui.same_line()
        UI_MENU.esp_entity = imgui.checkbox('EspEntity', UI_MENU.esp_entity)[1]

        imgui.separator()
        UI_MENU.aim_bot = imgui.checkbox('AimBot', UI_MENU.aim_bot)[1]
        imgui.same_line()
        UI_MENU.aim_rcs = imgui.checkbox('Rcs', UI_MENU.aim_rcs)[1]
        imgui.same_line()
        UI_MENU.trigger = imgui.checkbox('Trigger', UI_MENU.trigger)[1]
        imgui.same_line()
        UI_MENU.bhop = imgui.checkbox('Bhop', UI_MENU.bhop)[1]

        imgui.separator()
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

        UI_MENU.rcs_inhibit = imgui.slider_float(
            'RCS Inhibit', UI_MENU.rcs_inhibit, 1.0, 4.0)[1]

        UI_MENU.trigger_time = imgui.slider_int(
            'TriggerTime', UI_MENU.trigger_time, 10, 500)[1]

        UI_MENU.bhop_delay = imgui.slider_int(
            'BhopDelay', UI_MENU.bhop_delay, 0, 50)[1]

        UI_MENU.bhop_press_delay = imgui.slider_int(
            'BhopPressDelay', UI_MENU.bhop_press_delay, 0, 1000)[1]

        imgui.separator()
        UI_MENU.team_check = imgui.checkbox(
            'team_check', UI_MENU.team_check)[1]

        draw.BeginGdi()
        status, self_player, player_list = esp.work()
        if status:
            if UI_MENU.aim_bot:
                aimbot.work(self_player, player_list)
            if UI_MENU.esp_entity:
                Entity.work(draw, hack, self_player, player_list)
        draw.EndGdi()
        imgui.end()
        time.sleep(0.001)


    MyImGui().set_draw_callback(Menu).run()
