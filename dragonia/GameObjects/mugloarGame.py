import requests
import json
from .knight import Knight


class MugloarGame:

    def __init__(self, pet):
        self.pet   = pet
        self.mugolarGetUrl = 'http://www.dragonsofmugloar.com/api/game'
        self._game_id = 0
        self.battle_result = None
        self._knight        = None

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    @property
    def knight(self):
        return self._knight

    @knight.setter
    def knight(self, knight):
        self._knight = knight

    @staticmethod
    def get_solution_url(game_id):
        return 'http://www.dragonsofmugloar.com/api/game/%s/solution' % game_id

    def get_knight(self):
        game_json = requests.get(self.mugolarGetUrl).text
        print(game_json)
        game_dict = json.loads(game_json)
        print(game_dict)
        self.knight = Knight(game_dict['knight'])
        self.game_id = game_dict['gameId']

    def attack(self, dragon):
        solution_url = self.get_solution_url(self.game_id)
        print(solution_url)
        print(dragon.dragon_json)
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        }
        self.battle_result = requests.put(solution_url, data=dragon.dragon_json, headers=headers)


