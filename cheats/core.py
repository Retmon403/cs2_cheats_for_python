import time
from .gdi import *
from .hacker import *
from .player import *
from .other import *
import win32api
from .ui_menu import *

# 已开源到同性交友网站 https://github.com/Retmon403/cs2_cheats_python/tree/main


class ESP:

    __draw_bons_a_list = []
    __draw_bons_b_list = []

    def __init__(self, _hack: Hacker, _draw: GDI) -> None:
        self.hack = _hack
        self.draw = _draw

    def __del__(self) -> None:
        pass

    def __push_draw_ab(self, a, b, update_mex: bool = False):
        screen_a = self.hack.world_to_screen(a, update_mex)
        screen_b = self.hack.world_to_screen(b, update_mex)
        if len(screen_a) != 0 and len(screen_b) != 0:
            if (screen_a[0] != 0.0 and screen_a[1] != 0.0) and (screen_b[0] != 0.0 and screen_b[1] != 0.0):
                self.__draw_bons_a_list.append(screen_a)
                self.__draw_bons_b_list.append(screen_b)

    def draw_bons(self, p: Player, color, thickness):
        self.__draw_bons_a_list.clear()
        self.__draw_bons_b_list.clear()

        self.__push_draw_ab(p.bons[6], p.bons[5], True)
        self.__push_draw_ab(p.bons[4], p.bons[5])
        self.__push_draw_ab(p.bons[4], p.bons[2])
        self.__push_draw_ab(p.bons[2], p.bons[0])

        self.__push_draw_ab(p.bons[13], p.bons[5])
        self.__push_draw_ab(p.bons[8], p.bons[5])
        self.__push_draw_ab(p.bons[13], p.bons[14])
        self.__push_draw_ab(p.bons[8], p.bons[9])
        self.__push_draw_ab(p.bons[9], p.bons[10])
        self.__push_draw_ab(p.bons[10], p.bons[11])
        self.__push_draw_ab(p.bons[14], p.bons[15])
        self.__push_draw_ab(p.bons[16], p.bons[15])

        self.__push_draw_ab(p.bons[0], p.bons[25])
        self.__push_draw_ab(p.bons[26], p.bons[25])
        self.__push_draw_ab(p.bons[26], p.bons[27])
        self.__push_draw_ab(p.bons[0], p.bons[22])
        self.__push_draw_ab(p.bons[23], p.bons[22])
        self.__push_draw_ab(p.bons[23], p.bons[24])

        self.draw.DrawLine(self.__draw_bons_a_list,
                           self.__draw_bons_b_list, color, thickness)

    def update_setup(self, _esp_box: bool, _esp_bons: bool):
        self.esp_box = _esp_box
        self.esp_bons = _esp_bons

    def work(self) -> list:
        result = []
        for i in range(64):
            entity = self.hack.read_ulonglong(self.hack.get_entity_addr()+0x10)
            entity = self.hack.read_ulonglong(entity+(i+1)*0x78)
            if entity == 0:
                continue
            if entity == self.hack.get_local_player_controller():
                continue
            player = Player(self.hack)
            status = player.update_player(player.update_controller(entity))
            if not status or not player.alive:
                continue
            if (player.pos[0] == 0.0 and player.pos[1] == 0.0):
                continue
            screen_bottom = self.hack.world_to_screen(player.pos)
            if not screen_bottom:
                continue

            # insert list
            result.append(player)
            # draw

            if UI_MENU.esp_bons:
                self.draw_bons(player, win32api.RGB(200, 200, 200), 2)

            if UI_MENU.esp_box:
                head = player.bons[6]
                new_neck = head[2] + \
                    (player.bons[6][2]-player.bons[5][2])*2/1.2
                screen_top = self.hack.world_to_screen(
                    (head[0], head[1], new_neck))
                if not screen_top:
                    continue

                draw_h = screen_bottom[1]-screen_top[1]
                draw_w = draw_h/2
                box_x = screen_bottom[0]-draw_w/2
                box_y = screen_top[1]
                self.draw.DrawRect([(box_x, box_y)], [
                                   (draw_w, draw_h)], win32api.RGB(220, 0, 0), 2)
        return result


class AimBot():

    def __init__(self, _hack: Hacker, _draw: GDI) -> None:
        self.hack = _hack
        self.draw = _draw
        pass

    def work(self, player: list):
        if not UI_MENU.aim_bot:
            return
        loacl = Player(self.hack)
        status = loacl.update_player(loacl.update_controller(
            self.hack.get_local_player_controller()))
        if not status:
            return

        screen_center = (self.hack.rect[2]/2, self.hack.rect[3]/2)
        m_aim_obj = 0
        m_c_dis = 0
        m_distance = 0
        m_obj_2d = ()
        m_obj_3d = ()
        m_up_obj = 0
        for i in player:
            if loacl.teamid == i.teamid:
                continue
            obj_screen = self.hack.world_to_screen(i.bons[6])
            if not obj_screen:
                continue

            c_dis = Hacker.Calc2dDistance(obj_screen, screen_center)
            distance = Hacker.Calc3dDistance(loacl.pos, i.pos)
            if c_dis < UI_MENU.aim_scope:

                if m_aim_obj and m_aim_obj != i.player_addr:
                    continue
                if m_aim_obj == i.player_addr:
                    # update
                    m_obj_2d, m_obj_3d, m_up_obj = obj_screen, i.bons[6], i.player_addr
                if not m_c_dis:
                    m_c_dis = c_dis
                    m_distance = distance
                    # update
                    m_obj_2d, m_obj_3d, m_up_obj = obj_screen, i.bons[6], i.player_addr
                elif c_dis <= m_c_dis:
                    m_c_dis = c_dis
                    # update
                    m_obj_2d, m_obj_3d, m_up_obj = obj_screen, i.bons[6], i.player_addr
        if m_up_obj:

            if m_obj_2d:
                self.draw.DrawLine(
                    [screen_center], [m_obj_2d], win32api.RGB(220, 0, 0), 1)
            update_obj = Player(self.hack)
            if update_obj.update_player(m_up_obj):
                if (win32api.GetAsyncKeyState(UI_MENU.aim_key) & 0x8000):
                    if not m_aim_obj:
                        m_aim_obj = m_up_obj
                        self.__aim(loacl.player_addr,
                                   loacl.bons[6], update_obj.bons[6])

                    elif m_aim_obj == m_up_obj:
                        self.__aim(loacl.player_addr,
                                   loacl.bonsp[6], update_obj.bons[6])
                else:
                    m_aim_obj = 0
        else:
            m_aim_obj = 0

    def __aim(self, local_addr, self_pos, obj_pos):
        self_angle_x, self_angle_y = self.hack.get_self_view_angle()
        aim_angle = Hacker.GetAimScreen(
            self_pos, obj_pos)

        if UI_MENU.aim_rcs:
            rcs = self.hack.get_self_shotfire_rcs(local_addr)
            if rcs:
                aim_angle = (aim_angle[0] - rcs[0]*2.1,
                             aim_angle[1] - rcs[1]*2.1)
        if aim_angle:
            new_angle = self.__get_aim_smooth_point(
                self_pos=self_pos, obj_pos=obj_pos, self_angle=(self_angle_x, self_angle_y), aim_angle=aim_angle, speed=UI_MENU.aim_speed)
            if new_angle:
                self.hack.set_self_view_angle(*new_angle)

    def __get_aim_smooth_point(self, self_pos, obj_pos, self_angle, aim_angle, speed):
        t = 0.001
        x, y = self_angle
        distan_x = abs(aim_angle[0]-self_angle[0])
        if distan_x > 0.1:
            if distan_x < 1.0:
                t = 0.001
            else:
                t = 0.008

            if self_angle[0] > aim_angle[0]:
                x -= speed*t
            else:
                x += speed*t

        distan_y = abs(aim_angle[1]-self_angle[1])
        if distan_y > 0.1:
            if distan_y < 1.0:
                t = 0.001
            else:
                t = 0.008

            if self_angle[1] > 0.0 and aim_angle[1] < 0.0:
                if self_pos[0] > obj_pos[0] and self_pos[1] > obj_pos[1]:
                    y += speed*t
                else:
                    y -= speed*t
            if self_angle[1] < 0.0 and aim_angle[1] < 0.0:
                if self_angle[1] > aim_angle[1]:
                    y -= speed*t
                else:
                    y += speed*t
            if self_angle[1] < 0.0 and aim_angle[1] > 0.0:
                if self_pos[0] < obj_pos[0] and self_pos[1] < obj_pos[1]:
                    y += speed*t
                else:
                    y -= speed*t
            if self_angle[1] > 0.0 and aim_angle[1] > 0.0:
                if self_angle[1] > aim_angle[1]:
                    y -= speed*t
                else:
                    y += speed*t

        return x, y


class Bhop():
    def __init__(self) -> None:
        pass

    @staticmethod
    def loop(hack: Hacker):
        while True:
            if UI_MENU.bhop and (win32api.GetAsyncKeyState(win32con.VK_CAPITAL) & 0x8000):
                if not hack.get_jump_status():
                    time.sleep(UI_MENU.bhop_delay_start/1000)
                    hack.set_jump_status(True)
                    time.sleep(UI_MENU.bhop_delay_end/1000)
                    hack.set_jump_status(False)
            time.sleep(2/1000)
