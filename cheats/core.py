from .gdi import *
from .hacker import *
from .player import *


class ESP:
    esp_box = True
    esp_bons = True

    def __init__(self, _hack: Hacker, _draw: GDI) -> None:
        self.hack = _hack
        self.draw = _draw

    def __del__(self) -> None:
        pass

    def __draw_ab(self, a, b, color, thickness):
        screen_a = self.hack.world_to_screen(a)
        screen_b = self.hack.world_to_screen(b)
        if len(screen_a) != 0 and len(screen_b) != 0:
            if (screen_a[0] != 0.0 and screen_a[1] != 0.0) and (screen_b[0] != 0.0 and screen_b[1] != 0.0):
                self.draw.DrawLine(screen_a, screen_b, color, thickness)

    def draw_bons(self, p: Player, color, thickness):
        self.__draw_ab(p.bons[6], p.bons[5], color, thickness)
        self.__draw_ab(p.bons[4], p.bons[5], color, thickness)
        self.__draw_ab(p.bons[4], p.bons[2], color, thickness)
        self.__draw_ab(p.bons[2], p.bons[0], color, thickness)

        self.__draw_ab(p.bons[13], p.bons[5], color, thickness)
        self.__draw_ab(p.bons[8], p.bons[5], color, thickness)
        self.__draw_ab(p.bons[13], p.bons[14], color, thickness)
        self.__draw_ab(p.bons[8], p.bons[9], color, thickness)
        self.__draw_ab(p.bons[9], p.bons[10], color, thickness)
        self.__draw_ab(p.bons[10], p.bons[11], color, thickness)
        self.__draw_ab(p.bons[14], p.bons[15], color, thickness)
        self.__draw_ab(p.bons[16], p.bons[15], color, thickness)

        self.__draw_ab(p.bons[0], p.bons[25], color, thickness)
        self.__draw_ab(p.bons[26], p.bons[25], color, thickness)
        self.__draw_ab(p.bons[26], p.bons[27], color, thickness)
        self.__draw_ab(p.bons[0], p.bons[22], color, thickness)
        self.__draw_ab(p.bons[23], p.bons[22], color, thickness)
        self.__draw_ab(p.bons[23], p.bons[24], color, thickness)

    def update_setup(self, _esp_box: bool, _esp_bons: bool):
        self.esp_box = _esp_box
        self.esp_bons = _esp_bons

    def work(self):
        for i in range(64):
            entity = self.hack.read_ulonglong(self.hack.get_entity_addr()+0x10)
            entity = self.hack.read_ulonglong(entity+(i+1)*0x78)
            if entity == 0:
                continue
            if entity == self.hack.get_local_player_controller():
                continue
            player = Player(self.hack)
            status = player.update_player(player.update_controller(entity))
            if not status:
                continue
            if (player.pos[0] == 0.0 and screen_bottom[1] == 0.0):
                continue
            screen_bottom = self.hack.world_to_screen(player.pos)
            if len(screen_bottom) == 0:
                continue

            if self.esp_bons:
                self.draw_bons(player, win32api.RGB(200, 200, 200), 2)

            if self.esp_box:
                head = player.bons[6]
                new_neck = head[2] + \
                    (player.bons[6][2]-player.bons[5][2])*2/1.2
                screen_top = self.hack.world_to_screen(
                    (head[0], head[1], new_neck))
                if len(screen_top) == 0:
                    break

                draw_h = screen_bottom[1]-screen_top[1]
                draw_w = draw_h/2
                box_x = screen_bottom[0]-draw_w/2
                box_y = screen_top[1]

                self.draw.DrawRect((box_x, box_y), (draw_w, draw_h),
                                   win32api.RGB(255, 0, 0), 2)
