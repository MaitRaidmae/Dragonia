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
    def get_glaurung_dict(cls, knight_dict, weather_str):
        weather_type = cls.get_weather_type(weather_str)
        if weather_type == 'Storm':
           glaurung_dict = {'scale_thickness': 3,
                            'claw_sharpness': 3,
                            'wing_strength': 10,
                            'fire_breath': 4
           }
        elif weather_type == 'Draught':
            glaurung_dict = {'scale_thickness': 5,
                             'claw_sharpness': 5,
                             'wing_strength': 5,
                             'fire_breath': 5
                             }
        elif weather_type == 'Rain':
            glaurung_dict = {'scale_thickness': 5,
                             'claw_sharpness': 10,
                             'wing_strength': 5,
                             'fire_breath': 0
                             }
        else:
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
                glaurung_dict = cls.get_glaurung_off_drugs(glaurung_dict)
        print(glaurung_dict)
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
        if knight_attr == highest_attr or knight_dict[highest_attr] == knight_dict[knight_attr]:
            dragon_attr = knight_dict[knight_attr] + 2
        elif knight_dict[knight_attr] < 2:
            dragon_attr = knight_dict[knight_attr]
        else:
            dragon_attr = knight_dict[knight_attr] - 1
        return dragon_attr

    @staticmethod
    def get_glaurung_off_drugs(glaurung_dict):
        max_attr = max(glaurung_dict.values())
        set_attr = 10 - max_attr
        modified_dict = dict()
        for attr in glaurung_dict:
            if glaurung_dict[attr] != max_attr:
                modified_dict[attr] = set_attr
            else:
                modified_dict[attr] = glaurung_dict[attr]
        print(modified_dict)
        return modified_dict

    @staticmethod
    def get_weather_type(weather_string):
        weather_type = 'Normal'
        if weather_string.find('fog') != -1:
            weather_type = 'Fog'
        elif weather_string.find('storm') != -1:
            weather_type = 'Storm'
        elif weather_string.find('The Long Dry') != -1:
            weather_type = 'Draught'
        elif weather_string.find('Aquarius') != -1:
            weather_type = 'Rain'

        print(weather_string)
        print(weather_type)
        return weather_type
