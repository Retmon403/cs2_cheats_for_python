import time
from cheats.gdi import *
from cheats.hacker import *
from cheats.player import *
from cheats.core import *
from cheats.myimgui import *
import threading


def set_error(str):
    print(str)
    exit()


hwnd = win32gui.FindWindowEx(0, 0, None, 'Counter-Strike 2')
print('hwnd:', hwnd)
draw = GDI(hwnd=hwnd, hide=False)
hack = Hacker()
if not hack.init_game_data(hwnd):
    set_error('init faild')
esp = ESP(hack, draw)


def Menu():
    imgui.set_next_window_size(300, 200, imgui.FIRST_USE_EVER)
    imgui.begin('python cs2 cheats[lyx]', True)

    esp.esp_box = imgui.checkbox('EspBox', esp.esp_box)[1]
    imgui.same_line()
    esp.esp_bons = imgui.checkbox('EspBons', esp.esp_bons)[1]

    if win32gui.PeekMessage(None, 0, 0, 0):
        win32gui.PumpWaitingMessages()

    draw.BeginGdi()
    esp.work()

    draw.EndGdi()
    imgui.end()
    time.sleep(0.002)


if __name__ == '__main__':
    MyImGui().set_draw_callback(Menu).run()
