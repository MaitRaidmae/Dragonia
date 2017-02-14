import json
import requests
from .mugloarGame import MugloarGame

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