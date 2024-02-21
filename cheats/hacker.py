import math

from pymem import *

from cheats.config import *
from .client import *
from .other import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

PI = 3.14159265358979323846


class Hacker(Pymem):
    hwnd = 0
    client = 0
    mex = []
    rect = ()
    process_handle = 0

    def __init__(self) -> None:
        self.list_entity_addr = None
        self.client_size = None
        self.mem = Pymem()
        self.mem.open_process_from_name(process_name='cs2.exe')
        self.hwnd = GetHwndByPid(self.mem.process_id)
        self.rect = win32gui.GetClientRect(self.hwnd)
        self.process_handle = self.mem.process_handle
        print('process_id', self.mem.process_id, 'process_handle:',
              self.mem.process_handle, 'hwnd:', self.hwnd)
        if not self.hwnd:
            raise

    def __del__(self) -> None:
        print('close process...')
        self.mem.close_process()

    def init_data(self) -> bool:
        try:

            module = process.module_from_name(
                self.mem.process_handle, 'client.dll')
            self.client_size = module.SizeOfImage
            self.client = module.lpBaseOfDll
            print('client base:', hex(self.client))
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
            addr = self.getrelative_addr(self.client + i, 3, 7)
            try:
                data = self.mem.read_string(addr, len(s))
                if data == s and self.mem.read_bytes(addr + len(s), 1) == b'\x00':
                    addr = self.getrelative_addr(
                        self.client + i + 0x21, 3, 7)
                    result = self.mem.read_ulonglong(addr) + 0xc0
                    break
            except:
                continue
            # print(hex(self.client+i))
        return result

    def update_offset(self) -> bool:
        print('update offset...')

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
                self.client + searh_bytes(b, [0x48, 0x8D, 0x0D, 0x0, 0x0, 0x0, 0x0, 0x48, 0xC1, 0xE0, 0x06, 0x48]), 3,
                7) - self.client

            '''client.dll+71507E - CC                    - int 3 
            client.dll+71507F - CC                    - int 3 
            client.dll+715080 - 48 8B 0D D1360201     - mov rcx,[client.dll+1738758]
            client.dll+715087 - E9 B4D20200           - jmp client.dll+742340
            client.dll+71508C - CC                    - int 3 
            client.dll+71508D - CC                    - int 3 
            client.dll+71508E - CC                    - int 3 
            client.dll+71508F - CC                    - int 3 
            client.dll+715090 - 48 C7 02 00000000     - mov qword ptr [rdx],00000000
            '''
            view_a = [0x48, 0x8B, 0x0D, 0x0, 0x0, 0x0, 0x0, 0xE9, 0x0,
                      0x0, 0x0, 0x0, 0xCC, 0xCC, 0xCC, 0xCC, 0x48, 0xC7, 0x02]
            '''client.dll+741947 - F3 41 0F10 85 90530000  - movss xmm0,[r13+00005390]
            client.dll+741950 - 83 49 10 01           - or dword ptr [rcx+10],01
            client.dll+741954 - 8B 41 10              - mov eax,[rcx+10]
            client.dll+741957 - F3 0F11 41 18         - movss [rcx+18],xmm0
            client.dll+74195C - 83 C8 02              - or eax,02
            '''
            view_b = [0xF3, 0x41, 0x0F, 0x10, 0x00, 0x00, 0x00,
                      0x00, 0x00, 0x83, 0x49, 0x00, 0x00, 0x8B, 0x41, 0x00]
            Offset.dwViewAngles = self.getrelative_addr(
                self.client + searh_bytes(b, view_a), 3, 7) - self.client

            Offset.dwViewAngles_Add = self.mem.read_long(
                self.client + searh_bytes(b, view_b) + 5)

            print('attack:', hex(Offset.dwForceAttack),
                  'jump:', hex(Offset.dwForceJump))
            print('dwEntityList:', hex(Offset.dwEntityList), 'dwLocalPlayerController:', hex(
                Offset.dwLocalPlayerController), 'dwViewMatrix:', hex(Offset.dwViewMatrix), 'dwViewAngles:',
                  hex(Offset.dwViewAngles), 'dwViewAngles_Add:', hex(Offset.dwViewAngles_Add))
            print('update successful')

            return True
        except:
            return False

    def get_entity_addr(self) -> int:
        self.list_entity_addr = self.mem.read_ulonglong(
            self.client + Offset.dwEntityList)
        return self.list_entity_addr

    def get_local_player_controller(self) -> int:
        return self.mem.read_ulonglong(self.client + Offset.dwLocalPlayerController)

    def get_self_view_angle(self) -> tuple:
        view = self.mem.read_ulonglong(self.client + Offset.dwViewAngles)
        x = self.mem.read_float(view + Offset.dwViewAngles_Add)
        y = self.mem.read_float(view + Offset.dwViewAngles_Add + 4)
        return x, y

    def set_self_view_angle(self, x: float, y: float):
        view = self.mem.read_ulonglong(self.client + Offset.dwViewAngles)
        self.mem.write_float(view + Offset.dwViewAngles_Add, x)
        self.mem.write_float(view + Offset.dwViewAngles_Add + 4, y)

    def get_self_shotfire_rcs(self, local_addr):
        count = self.mem.read_ulonglong(
            local_addr + C_CSPlayerPawn.m_aimPunchCache)
        data = self.mem.read_ulonglong(
            local_addr + C_CSPlayerPawn.m_aimPunchCache + 8)

        if 0xFFFF < count <= 0:
            return 0, 0

        x = self.mem.read_float(data + (count - 1) * (4 * 3))
        y = self.mem.read_float(data + (count - 1) * (4 * 3) + 4)
        return x, y

    def set_jump_status(self, is_jump: bool):
        value = 256
        if is_jump:
            value = 65537
        self.mem.write_ulong(self.client + Offset.dwForceJump, value)

    def get_attack_status(self) -> bool:
        return self.mem.read_ulong(self.client + Offset.dwForceAttack) == 65537

    def set_attack_status(self, is_attack: bool):
        value = 256
        if is_attack:
            value = 65537
        self.mem.write_ulong(self.client + Offset.dwForceAttack, value)

    def __update_mex(self):
        self.mex = []
        addr = self.client + Offset.dwViewMatrix
        for i in range(4):
            x = self.mem.read_float(addr)
            y = self.mem.read_float(addr + 4)
            z = self.mem.read_float(addr + 4 * 2)
            a = self.mem.read_float(addr + 4 * 3)
            addr += 4 * 4
            self.mex.append((x, y, z, a))

    def world_to_screen(self, pos, update_mex: bool = True) -> list:
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
