from pymem import *
import pymem.process as process
from .offset import *
import win32gui
import ctypes


class Hacker(Pymem):

    client = 0
    process_handle = 0
    mex = []

    rect = ()

    def __init__(self) -> None:
        self.mem = Pymem()

    def __del__(self) -> None:
        print('close process...')
        self.mem.close_process()

    def init_game_data(self, game_hwnd) -> bool:
        try:
            self.mem.open_process_from_name(process_name='cs2.exe')
            self.process_handle = self.mem.process_handle
            self.client = process.module_from_name(
                self.mem.process_handle, 'client.dll').lpBaseOfDll
            print('client base:', hex(self.client))

            self.rect = win32gui.GetClientRect(game_hwnd)
            return True
        except:
            return False

    def get_entity_addr(self) -> int:
        return self.mem.read_ulonglong(self.client+Offset.dwEntityList)

    def get_local_player_controller(self) -> int:
        return self.mem.read_ulonglong(self.client+Offset.dwLocalPlayerController)

    def __update_mex(self):
        self.mex = []
        addr = self.client+Offset.dwViewMatrix
        for i in range(4):
            x = self.mem.read_float(addr)
            y = self.mem.read_float(addr+4)
            z = self.mem.read_float(addr+4*2)
            a = self.mem.read_float(addr+4*3)
            addr += 4*4
            self.mex.append((x, y, z, a))

    def world_to_screen(self, pos) -> list:
        self.__update_mex()
        view = 0.0
        sightx, sighty = self.rect[2]/2, self.rect[3]/2
        view = self.mex[3][0]*pos[0]+self.mex[3][1] * \
            pos[1]+self.mex[3][2]*pos[2]+self.mex[3][3]

        if view <= 0.01:
            return []
        x = sightx + (self.mex[0][0] * pos[0] + self.mex[0][1] *
                      pos[1] + self.mex[0][2] * pos[2] + self.mex[0][3]) / view * sightx

        y = sighty - (self.mex[1][0] * pos[0] + self.mex[1][1] *
                      pos[1] + self.mex[1][2] * pos[2] + self.mex[1][3]) / view * sighty
        return [x, y]


if __name__ == '__main__':
    pass
