import pyglet
import imgui
from imgui.integrations.pyglet import *


# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

class MyImGui:

    __new_draw_func = None

    def __init__(self, window_w: int = 500, window_h: int = 400, resizable: bool = True, create_ini_file: bool = False) -> None:
        self.window = pyglet.window.Window(
            width=window_w, height=window_h, resizable=resizable)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.ESCAPE:
                # 禁用esc关闭窗口
                return pyglet.event.EVENT_HANDLED

        imgui.create_context()
        if not create_ini_file:
            io = imgui.get_io()
            io.ini_file_name = ''
            io.log_file_name = ''
        self.impl = create_renderer(self.window)

        pyglet.clock.schedule_interval(self.__draw_loop, 1/120)

    def run(self):
        pyglet.app.run()
        self.impl.shutdown()

    def set_draw_callback(self, func):
        self.__new_draw_func = func
        return self

    def __draw_loop(self, dt):
        imgui.new_frame()
        if self.__new_draw_func == None:
            self.__menu()
        else:
            self.__new_draw_func()

        self.window.clear()
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def __menu(self):
        imgui.set_next_window_size(400, 300, imgui.FIRST_USE_EVER)
        imgui.begin('call [set_draw_callback]', True)
        imgui.end()

    def __del__(self) -> None:
        pass
