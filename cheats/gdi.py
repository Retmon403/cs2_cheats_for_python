import win32api
import win32gui
import win32con
import ctypes
import random


def get_rand_str(size) -> str:
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    r = ''
    for i in range(size):
        r += s[random.randint(0, len(s)-1)]
    return r


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

    def DrawLine(self, a, b, color, thickness: int = 1):
        if not self.begin:
            return
        x, y, x1, y1 = int(a[0]), int(a[1]), int(b[0]), int(b[1])
        pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, color)
        old_pen = win32gui.SelectObject(self.memhdc, pen)
        win32gui.MoveToEx(self.memhdc, x, y)
        win32gui.LineTo(self.memhdc, x1, y1)
        win32gui.SelectObject(self.memhdc, old_pen)
        win32gui.DeleteObject(pen)

    def DrawRect(self, a, b, color, thickness: int = 1):
        if not self.begin:
            return
        x, y, x1, y1 = int(a[0]), int(a[1]), int(b[0]), int(b[1])
        self.DrawLine((x, y), (x+x1, y), color, thickness)
        self.DrawLine((x, y), (x, y+y1), color, thickness)
        self.DrawLine((x, y+y1), (x+x1, y+y1), color, thickness)
        self.DrawLine((x+x1, y), (x+x1, y+y1), color, thickness)

    def __del__(self) -> None:
        win32gui.DestroyWindow(self.gdi_hwnd)
        win32gui.UnregisterClass(self.class_id, 0)
        print('del')


if __name__ == '__main__':
    pass
