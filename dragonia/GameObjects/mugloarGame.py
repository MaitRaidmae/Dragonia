import requests
import json
from .knight import Knight
import xml.etree.ElementTree as elTree


class MugloarGame:

    def __init__(self, pet):
        self.pet   = pet
        self.mugolarGetUrl = 'http://www.dragonsofmugloar.com/api/game'
        self._game_id = 0
        self._knight       = None
        self._weather      = None


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

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, forecast):
        self._weather = forecast

    @staticmethod
    def get_solution_url(game_id):
        return 'http://www.dragonsofmugloar.com/api/game/%s/solution' % game_id

    def get_knight(self):
        game_json = requests.get(self.mugolarGetUrl).text
        game_dict = json.loads(game_json)
        self.knight = Knight(game_dict['knight'])
        self.game_id = game_dict['gameId']
        self.get_weather()

    def get_weather(self):
            weather_url = 'http://www.dragonsofmugloar.com/weather/api/report/%s' % self.game_id
            weather_xml = requests.get(weather_url).text
            element = elTree.fromstring(weather_xml)
            forecast = element.find('message').text
            print(forecast)
            self.weather = forecast



