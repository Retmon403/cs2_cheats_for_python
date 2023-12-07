import win32api
import win32gui
import win32con
import ctypes
from .other import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main


class GDI():

    def __init__(self, hwnd, hide: bool = True) -> None:
        self.hwnd = hwnd
        self.__create_gdi_window()
        if hide:
            ctypes.windll.user32.SetWindowDisplayAffinity(self.gdi_hwnd, 17)
        old_style = win32api.GetWindowLong(
            self.gdi_hwnd, win32con.GWL_EXSTYLE)
        win32api.SetWindowLong(
            self.gdi_hwnd, win32con.GWL_EXSTYLE, old_style | win32con.WS_EX_TOOLWINDOW)

    def __create_gdi_window(self):
        n_class = get_rand_str(10)
        n_title = get_rand_str(10)

        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH+1)
        wc.lpszClassName = n_class
        self.class_id = win32gui.RegisterClass(wc)

        dwexstyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        style = win32con.WS_POPUP | win32con.WS_OVERLAPPED | win32con.WS_SYSMENU | win32con.WS_TABSTOP | win32con.WS_GROUP | win32con.WS_CLIPCHILDREN

        self.gdi_hwnd = win32gui.CreateWindowEx(
            dwexstyle, n_class, n_title, style, 0, 0, 0, 0, None, None, None, None)
        win32gui.ShowWindow(self.gdi_hwnd, win32con.SW_SHOW)
        win32gui.UpdateWindow(self.gdi_hwnd)
        dc = win32gui.GetDC(self.gdi_hwnd)
        win32gui.SetLayeredWindowAttributes(
            self.gdi_hwnd, win32gui.GetBkColor(dc), 0, win32con.LWA_COLORKEY)
        win32gui.ReleaseDC(self.gdi_hwnd, dc)

    def __update_window_pos(self):
        try:
            rect = win32gui.GetClientRect(self.hwnd)
            self.x, self.y = win32gui.ClientToScreen(self.hwnd, (0, 0))
            self.w = rect[2]-rect[0]
            self.h = rect[3]-rect[1]
            win32gui.SetWindowPos(self.gdi_hwnd, win32con.HWND_TOPMOST,
                                  self.x, self.y, self.w, self.h, win32con.SWP_NOACTIVATE)
            return True
        except:
            return False

    def BeginGdi(self):
        self.begin = self.__update_window_pos()
        if not self.begin:
            return

        self.hdc = win32gui.GetDC(self.gdi_hwnd)
        self.memhdc = win32gui.CreateCompatibleDC(self.hdc)
        self.bitmap = win32gui.CreateCompatibleBitmap(self.hdc, self.w, self.h)
        win32gui.SelectObject(self.memhdc, self.bitmap)
        win32gui.BitBlt(self.memhdc, 0, 0, self.w, self.h,
                        self.hdc, 0, 0, win32con.WHITENESS)

    def EndGdi(self):
        if not self.begin:
            return
        win32gui.BitBlt(self.hdc, 0, 0, self.w, self.h,
                        self.memhdc, 0, 0, win32con.SRCCOPY)
        win32gui.DeleteObject(self.memhdc)
        win32gui.DeleteObject(self.bitmap)
        win32gui.ReleaseDC(self.gdi_hwnd, self.hdc)

    def __create_pen(self, color, thickness):
        pen = win32gui.CreatePen(
            win32con.PS_SOLID, thickness, color)
        return pen, win32gui.SelectObject(self.memhdc, pen)

    def __destroy_pen(self, pen, old_obj):
        win32gui.SelectObject(self.memhdc, old_obj)
        win32gui.DeleteObject(pen)

    def __move_pen(self, x, y, x1, y1):
        win32gui.MoveToEx(self.memhdc, x, y)
        win32gui.LineTo(self.memhdc, x1, y1)

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
            self.__move_pen(x, y, x+x1, y)
            self.__move_pen(x, y, x, y+y1)
            self.__move_pen(x, y+y1, x+x1, y+y1)
            self.__move_pen(x+x1, y, x+x1, y+y1)
        self.__destroy_pen(pen, old_obj)


if __name__ == '__main__':
    pass
