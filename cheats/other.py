import random
import win32gui
import win32con
import win32process


def set_error(str):
    print(str)
    exit()


def get_rand_str(size) -> str:
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    r = ''
    for i in range(size):
        r += s[random.randint(0, len(s)-1)]
    return r


def searh_bytes(b, find) -> int:
    for d1, i in enumerate(b):
        success = True
        for d2, j in enumerate(find):
            if find[d2] == 0:
                continue
            if find[d2] != b[d1+d2]:
                success = False
                break
        if success:
            return d1
    return 0


def GetHwndByPid(_pid):
    '''通过窗口获得进程id,对比获得进程主窗口'''
    hwnd = win32gui.GetTopWindow(0)
    while hwnd:
        t_id, pid = win32process.GetWindowThreadProcessId(hwnd)
        if t_id and pid == _pid and not win32gui.GetParent(hwnd):
            return hwnd
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return 0



