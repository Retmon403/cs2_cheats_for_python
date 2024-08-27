import random
import win32gui
import win32con
import win32process
import json


class Offset:
    dwEntityList = 0
    dwLocalPlayerController = 0
    dwViewMatrix = 0
    dwViewAngles = 0
    dwViewAngles_Add = 0
    dwForceAttack = 0
    dwForceJump = 0


client_js = {}


def ClientOffset(s: str) -> int:
    global client_js
    if not client_js:
        with open('cheats\\client_dll.json', 'r') as f:
            client_js = json.loads(f.read())
    k = s.split('.')
    r = client_js["client.dll"]['classes'][k[0]]['fields'][k[1]]
    return int(r)


def Log(*args, **kwargs):
    print(*args, **kwargs)


def set_error(s):
    print(s)
    exit()


def get_rand_str(size) -> str:
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    r = ''
    for i in range(size):
        r += s[random.randint(0, len(s) - 1)]
    return r


def searh_bytes(b, find, r_list: bool = False):
    result = []
    for d1, i in enumerate(b):
        success = True
        for d2, j in enumerate(find):
            if find[d2] == 0:
                continue
            if find[d2] != b[d1 + d2]:
                success = False
                break
        if success:
            if not r_list:
                return d1
            else:
                result.append(d1)
    if r_list:
        return result
    else:
        return 0


def GetHwndByPid(_pid):
    """通过窗口获得进程id,对比获得进程主窗口"""
    hwnd = win32gui.GetTopWindow(0)
    while hwnd:
        t_id, pid = win32process.GetWindowThreadProcessId(hwnd)
        if t_id and pid == _pid and not win32gui.GetParent(hwnd):
            return hwnd
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return 0
