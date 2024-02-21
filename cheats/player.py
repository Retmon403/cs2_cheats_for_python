from .hacker import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main

BONS_SIZE = 30


class Player:
    health = 0
    teamid = 0
    bons = []
    pos = ()
    alive = False

    def __init__(self, hack: Hacker) -> None:
        self.player_addr = None
        self.controller_addr = None
        self.h = hack

    def __del__(self) -> None:
        pass

    def get_player_pawn_addr(self, addr) -> int:
        try:
            pawn = self.h.read_ulonglong(
                addr + CCSPlayerController.m_hPlayerPawn)
            entity_pawn = self.h.read_ulonglong(
                self.h.get_entity_addr() + 0x10 + 8 * ((pawn & 0x7fff) >> 9))
            entity_pawn = self.h.read_ulonglong(
                entity_pawn + 0x78 * (pawn & 0x1FF))
            return entity_pawn
        except:
            return 0

    def update_controller(self, addr) -> int:
        self.controller_addr = addr
        try:
            self.__get_player_name()
            return self.get_player_pawn_addr(addr)
        except:
            return 0

    def __get_player_name(self):
        self.player_name = self.h.read_string(
            self.controller_addr + CBasePlayerController.m_iszPlayerName, 260)

    def __get_player_weapon_name(self):
        try:
            base = self.h.read_ulonglong(
                self.player_addr + C_CSPlayerPawnBase.m_pClippingWeapon)
            data = self.h.read_ulonglong(base + 0x10)
            data = self.h.read_ulonglong(data + 0x20)
            s = self.h.read_string(data, 100)
            self.weapon_name = str(s).split('_')[1]
            if self.weapon_name.endswith(
                    ('knife', 'molotov', 'flashbang', 'smokegrenade', 'decoy', 'hegrenade', 'incgrenade',)):
                self.is_gun = False
            else:
                self.is_gun = True
        except:
            self.is_gun = False
            self.weapon_name = ''

    def __get_health(self):
        self.health = self.h.read_int(self.player_addr + C_BaseEntity.m_iHealth)
        self.alive = (self.health > 0 and self.health <= 100)

    def __get_teamid(self):
        self.teamid = self.h.read_int(self.player_addr + C_BaseEntity.m_iTeamNum)

    def __get_bons(self):
        self.bons = []
        scene = self.h.read_ulonglong(
            self.player_addr + C_BaseEntity.m_pGameSceneNode)
        bons_array = self.h.read_ulonglong(
            scene + CSkeletonInstance.m_modelState + CGameSceneNode.m_vecOrigin)
        for i in range(BONS_SIZE):
            x = self.h.read_float(bons_array)
            y = self.h.read_float(bons_array + 4)
            z = self.h.read_float(bons_array + 4 * 2)
            self.bons.append((x, y, z))
            bons_array += 0x20

    def __get_flags_status(self):
        self.flags = self.h.read_ulong(self.player_addr + C_BaseEntity.m_fFlags)

    def update_player(self, addr) -> bool:
        self.player_addr = addr
        if addr == 0:
            return False
        try:
            self.__get_flags_status()
            self.__get_health()
            self.__get_teamid()
            self.__get_player_weapon_name()
            # 骨骼点29的位置是对象的坐标
            self.__get_bons()
            self.pos = self.bons[29]

            return True
        except:
            return False


if __name__ == '__main__':
    pass
