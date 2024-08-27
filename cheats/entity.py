from .gdi import *
from .hacker import *


class Entity:
    def __init__(self, draw: GDI, hack: Hacker):
        self.entity_addr = None
        self.draw = draw
        self.hack = hack

    def __get_entity_name(self):
        base = self.hack.read_ulonglong(self.entity_addr + 0x10)
        base = self.hack.read_ulonglong(base + 0x20)
        name = self.hack.read_string(base, 128)
        if name.find('weapon') != -1 or name.find('projectile') != -1:
            self.entity_name = str(name).split('_')[1]
        else:
            raise

    def __get_entity_pos(self):
        scene_node = self.hack.read_ulonglong(self.entity_addr + ClientOffset('C_BaseEntity.m_pGameSceneNode'))
        x = self.hack.read_float(scene_node + ClientOffset('CGameSceneNode.m_vecAbsOrigin'))
        y = self.hack.read_float(scene_node + ClientOffset('CGameSceneNode.m_vecAbsOrigin') + 4)
        z = self.hack.read_float(scene_node + ClientOffset('CGameSceneNode.m_vecAbsOrigin') + 8)
        self.pos = (x, y, z)

    def update_entity(self, addr) -> bool:
        self.entity_addr = addr
        try:
            self.__get_entity_name()
            self.__get_entity_pos()
            return True
        except:
            return False

    @staticmethod
    def work(draw: GDI, hack: Hacker, self_player, player_list: list):
        for i in range(64, 1024 * 2):
            try:
                base = hack.read_ulonglong(hack.list_entity_addr + 0x8 * ((i & 0x7fff) >> 9) + 16)
                base = hack.read_ulonglong(base + 120 * (i & 0x1ff))
            except:
                break
            entity = Entity(draw, hack)
            if not entity.update_entity(base):
                continue
            if Hacker.Calc3dDistance(self_player.pos, entity.pos) < 15:
                continue

            is_break = False
            for player in player_list:
                if Hacker.Calc3dDistance(player.pos, entity.pos) < 15:
                    is_break = True
                    break
            if is_break:
                continue
            screen = hack.world_to_screen(entity.pos)
            if screen:
                draw.DrawText(entity.entity_name, screen[0], screen[1], False, g_color_red)
