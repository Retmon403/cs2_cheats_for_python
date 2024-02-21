import ctypes

import win32api

from .other import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

g_color_red = win32api.RGB(220, 0, 0)
g_color_white = win32api.RGB(200, 200, 200)
g_color_blue = win32api.RGB(63, 187, 238)
g_color_green = win32api.RGB(102, 247, 62)
g_color_orange = win32api.RGB(249, 142, 67)


class GDI:

    def __init__(self, hwnd, hide: bool = True) -> None:
        self.bitmap = None
        self.mem_hdc = None
        self.hdc = None
        self.begin = None
        self.hwnd = hwnd
        self.game_rect = win32gui.GetClientRect(self.hwnd)
        self.__create_gdi_window()
        if hide:
            ctypes.windll.user32.SetWindowDisplayAffinity(self.gdi_hwnd, 17)
        old_style = win32api.GetWindowLong(
            self.gdi_hwnd, win32con.GWL_EXSTYLE)

    def __create_gdi_window(self):
        n_class = get_rand_str(10)
        n_title = get_rand_str(10)

        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH + 1)
        wc.lpszClassName = n_class
        self.class_id = win32gui.RegisterClass(wc)

        dwexstyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW
        style = win32con.WS_POPUP | win32con.WS_OVERLAPPED | win32con.WS_SYSMENU | win32con.WS_TABSTOP | win32con.WS_GROUP | win32con.WS_CLIPCHILDREN

        self.gdi_hwnd = win32gui.CreateWindowEx(
            dwexstyle, n_class, n_title, style, 0, 0, 0, 0, None, None, None, None)
        win32gui.ShowWindow(self.gdi_hwnd, win32con.SW_SHOW)

        dc = win32gui.GetDC(self.gdi_hwnd)
        win32gui.SetLayeredWindowAttributes(
            self.gdi_hwnd, win32gui.GetBkColor(dc), 0, win32con.LWA_COLORKEY)
        win32gui.ReleaseDC(self.gdi_hwnd, dc)

    def __update_window_pos(self):
        try:
            self.game_rect = win32gui.GetClientRect(self.hwnd)
            self.x, self.y = win32gui.ClientToScreen(self.hwnd, (0, 0))
            win32gui.SetWindowPos(self.gdi_hwnd, win32con.HWND_TOP, self.x, self.y, self.game_rect[2],
                                  self.game_rect[3], win32con.SWP_NOACTIVATE)

            return True
        except:
            return False

    def BeginGdi(self):
        self.begin = self.__update_window_pos()
        if not self.begin:
            return

        self.hdc = win32gui.GetDC(self.gdi_hwnd)
        self.mem_hdc = win32gui.CreateCompatibleDC(self.hdc)
        win32gui.SetBkMode(self.mem_hdc, win32con.TRANSPARENT)
        self.bitmap = win32gui.CreateCompatibleBitmap(self.hdc, self.game_rect[2], self.game_rect[3])
        win32gui.SelectObject(self.mem_hdc, self.bitmap)
        win32gui.BitBlt(self.mem_hdc, 0, 0, self.game_rect[2], self.game_rect[3],
                        self.hdc, 0, 0, win32con.WHITENESS)

    def EndGdi(self):
        if not self.begin:
            return
        win32gui.BitBlt(self.hdc, 0, 0, self.game_rect[2], self.game_rect[3],
                        self.mem_hdc, 0, 0, win32con.SRCCOPY)
        win32gui.DeleteObject(self.mem_hdc)
        win32gui.DeleteObject(self.bitmap)
        win32gui.ReleaseDC(self.gdi_hwnd, self.hdc)

    def __create_pen(self, color, thickness):
        pen = win32gui.CreatePen(
            win32con.PS_SOLID, thickness, color)
        return pen, win32gui.SelectObject(self.mem_hdc, pen)

    def __destroy_pen(self, pen, old_obj):
        win32gui.SelectObject(self.mem_hdc, old_obj)
        win32gui.DeleteObject(pen)

    def __move_pen(self, x, y, x1, y1):
        try:
            win32gui.MoveToEx(self.mem_hdc, x, y)
            win32gui.LineTo(self.mem_hdc, x1, y1)
        except:
            pass

    def DrawText(self, s: str, x: int, y: int, upward=False, color=None) -> tuple:
        if not self.begin:
            return ()
        x = int(x)
        y = int(y)
        if color:
            win32gui.SetTextColor(self.mem_hdc, color)
        xx, rect = win32gui.DrawText(self.mem_hdc, s, len(s),
                                     (0, 0, 0, 0), win32con.DT_CALCRECT)
        if upward:
            y = y - rect[3]

        r = (x, y, x + rect[2], y + rect[3])
        win32gui.DrawText(self.mem_hdc, s, -1, r,
                          win32con.DT_CENTER | win32con.DT_VCENTER)
        return r

    def DrawLine(self, a, b, color, thickness: int = 1):
        if not self.begin:
            return
        if len(a) != len(b):
            raise
        pen, old_obj = self.__create_pen(color, thickness)
        for i in range(len(a)):
            x, y, x1, y1 = int(a[i][0]), int(
                a[i][1]), int(b[i][0]), int(b[i][1])
            self.__move_pen(x, y, x1, y1)
        self.__destroy_pen(pen, old_obj)

    def DrawRect(self, a: list, b: list, color, thickness: int = 1):
        if not self.begin:
            return
        if len(a) != len(b):
            raise
        pen, old_obj = self.__create_pen(color, thickness)
        for i in range(len(a)):
            x, y, x1, y1 = int(a[i][0]), int(
                a[i][1]), int(b[i][0]), int(b[i][1])
            self.__move_pen(x, y, x + x1, y)
            self.__move_pen(x, y, x, y + y1)
            self.__move_pen(x, y + y1, x + x1, y + y1)
            self.__move_pen(x + x1, y, x + x1, y + y1)
        self.__destroy_pen(pen, old_obj)

    def DrawRound(self, x, y, radius, color, thickness: int = 1):
        if not self.begin:
            return
        x = int(x)
        y = int(y)
        left = x - radius
        top = y - radius
        right = x + radius
        bottom = y + radius
        rect = (left, top, right, bottom)
        pen, old_obj = self.__create_pen(color, thickness)
        win32gui.Arc(self.mem_hdc, rect[0], rect[1],
                     rect[2], rect[3], 0, 0, 0, 0)
        self.__destroy_pen(pen, old_obj)


if __name__ == '__main__':
    pass
