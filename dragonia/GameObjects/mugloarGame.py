import requests
import json


class MugloarGame:

    def __init__(self, dragon, pet):
        self.dragon = dragon
        self.pet   = pet
        self.mugolarGetUrl = 'http://www.dragonsofmugloar.com/api/game'

    @staticmethod
    def get_solution_url(game_id):
        return 'http://www.dragonsofmugloar.com/api/game/%s/solution' % game_id

    def run_game(self):
        game_json = requests.get(self.mugolarGetUrl).text
        print(game_json)
        game_dict = json.loads(game_json)
        game_id   = game_dict['gameId']
        solution_url = self.get_solution_url(game_id)
        print(solution_url)
        print(self.dragon.dragon_json)
        battle_result = requests.put(solution_url, self.dragon.dragon_json)
        print(battle_result.text)






