import json


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
        dragon_jsondict = dict()
        dragon_jsondict['scaleThickness'] = self.dragon_dict['scale_thickness']
        dragon_jsondict['clawSharpness']  = self.dragon_dict['claw_sharpness']
        dragon_jsondict['wingStrength']   = self.dragon_dict['wing_strength']
        dragon_jsondict['fireBreath']     = self.dragon_dict['fire_breath']
        dragon_jsonobj = {'dragon': dragon_jsondict}
        return json.dumps(dragon_jsonobj)

    def attack(self):
        battle_result = 1
        return battle_result
