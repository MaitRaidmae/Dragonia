import json
import requests
from .mugloarGame import MugloarGame

from ..models import models

class Dragon:

    # This dict mess should be rewritten to make naming convention mapping prettier
    def __init__(self, dragon_dict):
        self.dragon_dict     = dragon_dict

    @property
    def scale_thickness(self):
        return self.dragon_dict['scale_thickness']

    @property
    def claw_sharpness(self):
        return self.dragon_dict['claw_sharpness']

    @property
    def wing_strength(self):
        return self.dragon_dict['wing_strength']

    @property
    def fire_breath(self):
        return self.dragon_dict['fire_breath']

    @property
    def dragon_json(self):
        dragon_jsondict = {
            'scaleThickness': self.dragon_dict['scale_thickness'],
            'clawSharpness': self.dragon_dict['claw_sharpness'],
            'wingStrength': self.dragon_dict['wing_strength'],
            'fireBreath':   self.dragon_dict['fire_breath']
        }
        dragon_jsonobj = {'dragon': dragon_jsondict}
        return json.dumps(dragon_jsonobj)

    def attack(self, game_id):
        solution_url = MugloarGame.get_solution_url(game_id)
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        }
        return requests.put(solution_url, data=self.dragon_json, headers=headers)

    @classmethod
    def get_glaurung_dict(cls, knight_dict):
        best_attr = cls.get_highest_attribute(knight_dict)
        glaurung_dict = dict()
        glaurung_dict['scale_thickness'] = cls.get_glaurung_attribute('scale_thickness', knight_dict, best_attr)
        glaurung_dict['claw_sharpness'] = cls.get_glaurung_attribute('claw_sharpness', knight_dict, best_attr)
        glaurung_dict['wing_strength'] = cls.get_glaurung_attribute('wing_strength', knight_dict, best_attr)
        glaurung_dict['fire_breath'] = cls.get_glaurung_attribute('fire_breath', knight_dict, best_attr)

        if sum(glaurung_dict.values()) < 20:
            if glaurung_dict['fire_breath'] != 10:
                glaurung_dict['fire_breath'] += 1
            else:
                glaurung_dict['claw_sharpness'] += 1
        elif sum(glaurung_dict.values()) > 20:
            cls.get_glaurung_off_drugs(glaurung_dict)
        print(glaurung_dict)
        print(knight_dict)
        return glaurung_dict

    @staticmethod
    def get_highest_attribute(knight_dict):
        highest_value = 0
        best_attr = ''
        for attr in knight_dict:
            if knight_dict[attr] > highest_value:
                highest_value = knight_dict[attr]
                best_attr = attr
        return best_attr

    @staticmethod
    def get_glaurung_attribute(attr, knight_dict, highest_attr):
        attr_map = {'scale_thickness': 'attack',
                    'claw_sharpness': 'armor',
                    'wing_strength': 'agility',
                    'fire_breath': 'endurance'}
        knight_attr = attr_map[attr]
        print(knight_attr)
        if knight_attr == highest_attr or knight_dict[highest_attr] == knight_dict[knight_attr]:
            dragon_attr = knight_dict[knight_attr] + 2
        elif knight_dict[knight_attr] < 2:
            dragon_attr = knight_dict[knight_attr]
        else:
            dragon_attr = knight_dict[knight_attr] - 1
        return dragon_attr

    @staticmethod
    def get_glaurung_off_drugs(glaurung_dict):
        a = 1

