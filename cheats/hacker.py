import math

import pymem

from cheats.config import *
from .other import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

PI = 3.14159265358979323846


class Hacker(pymem.Pymem):
    hwnd = 0
    client = 0
    mex = []
    rect = ()
    process_handle = 0

    def __init__(self) -> None:
        self.list_entity_addr = None
        self.client_size = None
        self.mem = pymem.Pymem()
        self.mem.open_process_from_name(process_name='cs2.exe')
        self.hwnd = GetHwndByPid(self.mem.process_id)
        self.rect = win32gui.GetClientRect(self.hwnd)
        self.process_handle = self.mem.process_handle
        Log('process_id', self.mem.process_id, 'process_handle:',
            self.mem.process_handle, 'hwnd:', self.hwnd)
        if not self.hwnd:
            raise

    def __del__(self) -> None:
        Log('close process...')
        self.mem.close_process()

    def init_data(self) -> bool:
        try:

            a = pymem.process.enum_process_module(self.process_handle)

            module = pymem.process.module_from_name(
                self.mem.process_handle, 'client.dll')
            self.client_size = module.SizeOfImage
            self.client = module.lpBaseOfDll
            Log('client base:', hex(self.client))
            return True
        except:
            return False

    def getrelative_addr(self, addr, offset, code_size) -> int:
        if not addr:
            raise
        offs = self.mem.read_long(addr + offset)
        return offs + addr + code_size

    def __find_enter_offset_by_string(self, byte: bytes, s: str) -> int:
        shell = [0x48, 0x8D, 0x15, 0x0, 0x0, 0x0, 0x0,
                 0x48, 0x8D, 0x0D, 0x0, 0x0, 0x0, 0x0, 0xE8]

        result = 0
        for i in searh_bytes(byte, shell, True):
            try:
                addr = self.getrelative_addr(self.client + i, 3, 7)
                data = self.mem.read_string(addr, len(s))
                if data == s and self.mem.read_bytes(addr + len(s), 1) == b'\x00':
                    addr = self.getrelative_addr(
                        self.client + i + 0x7, 3, 7)
                    result = addr + 0x2a
                    break
            except:
                continue
        return result

    def update_offset(self) -> bool:
        Log('update offset...')

        try:
            b = self.mem.read_bytes(self.client, self.client_size)

            Offset.dwForceAttack = self.__find_enter_offset_by_string(
                b, 'attack') - self.client
            Offset.dwForceJump = self.__find_enter_offset_by_string(
                b, 'jump') - self.client

            Offset.dwEntityList = self.getrelative_addr(
                self.client + searh_bytes(b, [0x48, 0x8b, 0x0, 0x0, 0x0, 0x0, 0x0,
                                              0x48, 0x89, 0x7c, 0x0, 0x0, 0x8b, 0x0, 0xc1]), 3, 7) - self.client

            Offset.dwLocalPlayerController = self.getrelative_addr(
                self.client + searh_bytes(b, [0xCC, 0xCC, 0x48, 0x8B, 0x05,
                                              0x0, 0x0, 0x0, 0x0, 0x48, 0x85, 0xC0, 0x74, 0x0, 0x8B]) + 2, 3,
                7) - self.client
            Offset.dwViewMatrix = self.getrelative_addr(
                self.client +
                searh_bytes(b, [0x48, 0x8D, 0x0D, 0x0, 0x0, 0x0,
                                0x0, 0x48, 0xC1, 0xE0, 0x06, 0x48]), 3,
                7) - self.client

            view_a = [0x48, 0x8B, 0x0D, 0x0, 0x0, 0x0, 0x0, 0x48, 0x8D, 0x54, 0x24, 0x0, 0x45, 0x33, 0xC0, 0xE8, 0x0,
                      0x0, 0x0, 0x0, 0xF2]

            view_b = [0xF2, 0x41, 0x0F, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xF2, 0x41, 0x0F, 0x11, 0x01, 0x41]
            Offset.dwViewAngles = self.getrelative_addr(
                self.client + searh_bytes(b, view_a), 3, 7) - self.client

            Offset.dwViewAngles_Add = self.mem.read_long(
                self.client + searh_bytes(b, view_b) + 6)

            Log('attack:', hex(Offset.dwForceAttack),
                'jump:', hex(Offset.dwForceJump))
            Log('dwEntityList:', hex(Offset.dwEntityList), 'dwLocalPlayerController:', hex(
                Offset.dwLocalPlayerController), 'dwViewMatrix:', hex(Offset.dwViewMatrix), 'dwViewAngles:',
                hex(Offset.dwViewAngles), 'dwViewAngles_Add:', hex(Offset.dwViewAngles_Add))
            Log('update successful')

            return True
        except:
            return False

    def get_entity_addr(self) -> int:
        try:
            self.list_entity_addr = self.mem.read_ulonglong(
                self.client + Offset.dwEntityList)
            return self.list_entity_addr
        except:
            return 0

    def get_local_player_controller(self) -> int:
        try:
            return self.mem.read_ulonglong(self.client + Offset.dwLocalPlayerController)
        except:
            return 0

    def get_self_view_angle(self) -> tuple:
        try:
            view = self.mem.read_ulonglong(self.client + Offset.dwViewAngles)
            x = self.mem.read_float(view + Offset.dwViewAngles_Add)
            y = self.mem.read_float(view + Offset.dwViewAngles_Add + 4)
            return x, y
        except:
            return 0, 0

    def set_self_view_angle(self, x: float, y: float):
        try:
            view = self.mem.read_ulonglong(self.client + Offset.dwViewAngles)
            self.mem.write_float(view + Offset.dwViewAngles_Add, x)
            self.mem.write_float(view + Offset.dwViewAngles_Add + 4, y)
        except:
            pass

    def get_self_shotfire_rcs(self, local_addr):
        try:
            count = self.mem.read_ulonglong(
                local_addr + ClientOffset('C_CSPlayerPawn.m_aimPunchCache'))
            data = self.mem.read_ulonglong(
                local_addr + ClientOffset('C_CSPlayerPawn.m_aimPunchCache') + 8)

            if count > 0xFFFF and count <= 0:
                return 0, 0

            x = self.mem.read_float(data + (count - 1) * (4 * 3))
            y = self.mem.read_float(data + (count - 1) * (4 * 3) + 4)
            return x, y
        except:
            return 0, 0

    def set_jump_status(self, is_jump: bool):
        try:
            value = 256
            if is_jump:
                value = 65537
            self.mem.write_ulong(self.client + Offset.dwForceJump, value)
        except:
            pass

    def get_attack_status(self) -> bool:
        try:
            return self.mem.read_ulong(self.client + Offset.dwForceAttack) == 65537
        except:
            pass

    def set_attack_status(self, is_attack: bool):
        try:
            value = 256
            if is_attack:
                value = 65537
            self.mem.write_ulong(self.client + Offset.dwForceAttack, value)
        except:
            pass

    def __update_mex(self):
        try:
            self.mex = []
            addr = self.client + Offset.dwViewMatrix
            for i in range(4):
                x = self.mem.read_float(addr)
                y = self.mem.read_float(addr + 4)
                z = self.mem.read_float(addr + 4 * 2)
                a = self.mem.read_float(addr + 4 * 3)
                addr += 4 * 4
                self.mex.append((x, y, z, a))
        except:
            pass

    def world_to_screen(self, pos, update_mex: bool = True) -> list:
        try:
            if update_mex:
                self.__update_mex()

            self.rect = win32gui.GetClientRect(self.hwnd)
            view = 0.0
            sightx, sighty = self.rect[2] / 2, self.rect[3] / 2
            view = self.mex[3][0] * pos[0] + self.mex[3][1] * \
                   pos[1] + self.mex[3][2] * pos[2] + self.mex[3][3]

            if view <= 0.01:
                return []
            x = sightx + (self.mex[0][0] * pos[0] + self.mex[0][1] *
                          pos[1] + self.mex[0][2] * pos[2] + self.mex[0][3]) / view * sightx

            y = sighty - (self.mex[1][0] * pos[0] + self.mex[1][1] *
                          pos[1] + self.mex[1][2] * pos[2] + self.mex[1][3]) / view * sighty
            return [x, y]
        except:
            return []

    @staticmethod
    def GetAimScreen(self_pos, obj_pos):
        if not self_pos or not obj_pos:
            return 0, 0
        x = self_pos[0] - obj_pos[0]
        y = self_pos[1] - obj_pos[1]
        z = self_pos[2] - obj_pos[2]
        r_x = math.atan(z / math.sqrt(x * x + y * y)) / PI * 180.0
        r_y = math.atan(y / x)

        if x >= 0.0 and y >= 0.0:
            r_y = r_y / PI * 180.0 - 180.0
        elif x < 0.0 and y >= 0.0:
            r_y = r_y / PI * 180.0
        elif x < 0.0 and y < 0.0:
            r_y = r_y / PI * 180.0
        elif x >= 0.0 and y < 0.0:
            r_y = r_y / PI * 180.0 + 180.0

        return r_x, r_y

    @staticmethod
    def Calc2dDistance(self_2d, obj_2d):
        return math.sqrt(
            (obj_2d[0] - self_2d[0]) * (obj_2d[0] - self_2d[0]) + (obj_2d[1] - self_2d[1]) * (obj_2d[1] - self_2d[1]))

    @staticmethod
    def Calc3dDistance(self_3d, obj_3d):
        return math.sqrt((obj_3d[0] - self_3d[0]) * (obj_3d[0] - self_3d[0]) + (obj_3d[1] - self_3d[1]) * (
                obj_3d[1] - self_3d[1]) + (obj_3d[2] - self_3d[2]) * (obj_3d[2] - self_3d[2]))


if __name__ == '__main__':
    pass
