import os
from .offset import *


class Config:
    config_path = 'offset_config.txt'

    @staticmethod
    def save_offset(dwEntityList, dwLocalPlayerController, dwViewMatrix, dwViewAngles, dwViewAngles_Add, dwForceAttack, dwForceJump):
        with open(Config.config_path, 'w') as f:
            w_dict = {}
            w_dict.update({'dwEntityList': dwEntityList})
            w_dict.update({'dwLocalPlayerController': dwLocalPlayerController})
            w_dict.update({'dwViewMatrix': dwViewMatrix})
            w_dict.update({'dwViewAngles': dwViewAngles})
            w_dict.update({'dwViewAngles_Add': dwViewAngles_Add})
            w_dict.update({'dwForceAttack': dwForceAttack})
            w_dict.update({'dwForceJump': dwForceJump})
            f.write(str(w_dict))

    @staticmethod
    def read_offset():
        with open(Config.config_path, 'r') as f:

            r_dict = eval(f.read())
            print(r_dict)
            Offset.dwEntityList = r_dict.get('dwEntityList', 0)
            Offset.dwLocalPlayerController = r_dict.get(
                'dwLocalPlayerController', 0)
            Offset.dwViewMatrix = r_dict.get('dwViewMatrix', 0)
            Offset.dwViewAngles = r_dict.get('dwViewAngles', 0)
            Offset.dwViewAngles_Add = r_dict.get('dwViewAngles_Add', 0)
            Offset.dwForceAttack = r_dict.get('dwForceAttack', 0)
            Offset.dwForceJump = r_dict.get('dwForceJump', 0)
