from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
)

import json

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .security import (
    check_password,
    hash_password
)

from .GameObjects import (
    dragon,
    mugloarGame
)

from .models import models


@view_defaults(renderer='Views/welcome_to_dragonia.pt')
class DragoniaViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='welcome_to_dragonia', renderer='Views/welcome_to_dragonia.pt')
    @forbidden_view_config(renderer='welcome_to_dragonia.pt')
    def welcome_to_dragonia(self):
        request = self.request
        login_url = request.route_url('welcome_to_dragonia')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = 'Enter your Pet credentials or summon a New Pet'
        login = ''
        password = ''
        # This is not particularly pretty - but it currently works. Do better later
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user = models.DBSession.query(models.User).filter_by(user_id=login).first()
            if user is not None:
                password_hash=user.password
                if check_password(password, password_hash):
                    main_url = request.route_url('dragonia_main')
                    headers = remember(request, login)
                    return HTTPFound(location=main_url,
                                     headers=headers)
                else:
                    message = 'Your secret word is not recognized by the dragons. They try to eat you.'
            else:
                message = 'No such Pet Found. Please use a real Pet Name ' \
                          '(i.e. one that has been summoned before via a button for creating Pets)'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='dragonia_main', renderer='Views/dragonia_main.pt')
    def dragonia_main(self):
        game = mugloarGame.MugloarGame(self.logged_in)
        game.get_knight()
        models.DBSession.add(models.MugloarGame(
            game_id=game.game_id,
            user_id=self.request.authenticated_userid,
            knight_agility=game.knight.agility,
            knight_endurance=game.knight.endurance,
            knight_armor=game.knight.armor,
            knight_attack=game.knight.attack,
            weather=game.weather
        ))
        return {'page_title': 'Dragonia',
                'user_id': self.logged_in,
                'game_id': game.game_id,
                'knight_name': game.knight.name,
                'knight': game.knight.description,
                'weather': game.weather}

    @view_config(route_name='battle', renderer='Views/battle.pt')
    def battle(self):
        mugloar_game_id = self.request.matchdict['game_id']
        selected_dragon = self.request.matchdict['dragon']

        mugloar_game = models.DBSession.query(models.MugloarGame).filter_by(game_id=mugloar_game_id).first()
        game_uid = mugloar_game.uid
        knight_dict = {
            'attack': mugloar_game.knight_attack,
            'agility': mugloar_game.knight_agility,
            'armor': mugloar_game.knight_armor,
            'endurance': mugloar_game.knight_endurance
        }
        dragon_dict = dict()
        if selected_dragon == 'Scaly':
            dragon_dict = {
                'scale_thickness': 10,
                'claw_sharpness': 5,
                'wing_strength': 4,
                'fire_breath': 1
            }
        elif selected_dragon == 'Wingy':
            dragon_dict = {
                'scale_thickness': 1,
                'claw_sharpness': 5,
                'wing_strength': 10,
                'fire_breath': 4
            }
        elif selected_dragon == 'Clawy':
            dragon_dict = {
                'scale_thickness': 2,
                'claw_sharpness': 10,
                'wing_strength': 3,
                'fire_breath': 5
            }
        elif selected_dragon == 'Flamy':
            dragon_dict = {
                'scale_thickness': 1,
                'claw_sharpness': 5,
                'wing_strength': 4,
                'fire_breath': 10
            }
        elif selected_dragon == 'Glaurung':
            dragon_dict = dragon.Dragon.get_glaurung_dict(knight_dict)
        my_dragon = dragon.Dragon(dragon_dict)
        battleresult_json = my_dragon.attack(mugloar_game_id).text
        battleresult_dict = json.loads(battleresult_json)
        models.DBSession.add(models.Battle(
            mugloar_games_uid=game_uid,
            result=battleresult_dict['status'],
            result_text=battleresult_dict['message'],
            dragon_name=selected_dragon,
            dragon_wing_strength=my_dragon.wing_strength,
            dragon_fire_breath=my_dragon.fire_breath,
            dragon_claw_sharpness=my_dragon.claw_sharpness,
            dragon_scale_thickness=my_dragon.scale_thickness
        ))
        return {'result': battleresult_dict['status'],
                'result_text':battleresult_dict['message']}

    @view_config(route_name='create_new_pet', renderer='Views/create_new_pet.pt')
    def create_new_pet(self):
        message = "Please select your Pet Name and Secret Word"
        request = self.request
        new_pet_name = ''
        secret_word = ''
        repeat_secret_word = ''
        if 'form.submitted' in request.params:
            request = self.request
            new_pet_name = request.params['new_pet_name']
            secret_word = request.params['secret_word']
            repeat_secret_word = request.params['repeat_secret_word']
            pet_name_found = models.DBSession.query(models.User).filter_by(user_id=new_pet_name).first()

            if new_pet_name == "":
                message = 'Your blankness regarding a name is disappointing. Please try again'
            elif len(secret_word) < 4:
                message = 'That''s an awesome secret word, but it''s lacking in length. Please use at least 4 runes.'
            elif pet_name_found is not None:
                message = 'Pet with name %s already exist. Please do not try to have two pets with the same name. ' \
                          'It confuses the dragons.' % new_pet_name
            elif secret_word != repeat_secret_word:
                message = 'Your secret word repeat typing skills are lacking. Please try again'
            else:
                hashed_password = hash_password(secret_word)
                models.DBSession.add(models.User(user_id=new_pet_name, password=hashed_password))
                return HTTPFound(location=self.request.route_url('welcome_to_dragonia'))
        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            new_pet_name=new_pet_name,
            secret_word=secret_word,
            repeat_secret_word=repeat_secret_word
        )

    @view_config(route_name='the_den_of_dragons', renderer='Views/the_den_of_dragons.pt')
    def the_den_of_dragons(self):
        dragons = dict()
        battle_results = models.DBSession.query(models.Battle).join(models.MugloarGame).\
            filter_by(user_id=self.request.matchdict['user_id']).all()
        for battle in battle_results:
            if battle.dragon_name not in dragons:
                dragons[battle.dragon_name] = self.init_battle_dict()
            dragons[battle.dragon_name]['battles'] += 1
            if battle.result == 'Victory':
                dragons[battle.dragon_name]['victories'] += 1
            else:
                dragons[battle.dragon_name]['defeats'] += 1
        dragon_stats = self.get_dragon_stats(dragons)
        favourite_dragon = self.get_favourite_dragon(dragon_stats)
        best_dragon = self.get_best_dragon(dragon_stats)
        return {'favourite_dragon': favourite_dragon,
                'best_dragon': best_dragon,
                'dragon_stats': dragon_stats.values()}

    @classmethod
    def get_dragon_stats(cls, dragons):
        dragon_stats = dict()
        for dragn in dragons:
            if dragn not in dragon_stats:
                dragon_stats[dragn] = cls.init_stats_dict(dragn)
            dragon_stats[dragn]['battles'] = dragons[dragn]['battles']
            dragon_stats[dragn]['victories'] = dragons[dragn]['victories']
            dragon_stats[dragn]['defeats'] = dragons[dragn]['defeats']
            success_rate = round((dragons[dragn]['victories'] / dragons[dragn]['battles']) * 100, 2)
            dragon_stats[dragn]['success_rate'] = success_rate
        return dragon_stats

    @staticmethod
    def init_battle_dict():
        return {'battles': 0,
                'victories': 0,
                'defeats': 0}

    @staticmethod
    def init_stats_dict(dragon_name):
        return {'name': dragon_name,
                'battles': 0,
                'victories': 0,
                'defeats': 0,
                'success_rate': 0}

    @staticmethod
    def get_favourite_dragon(dragon_stats):
        favourite_dragon = ''
        most_battles = 0
        for dragon_name in dragon_stats:
            if dragon_stats[dragon_name]['battles'] > most_battles:
                favourite_dragon = dragon_name
                most_battles = dragon_stats[dragon_name]['battles']
        return favourite_dragon

    @staticmethod
    def get_best_dragon(dragon_stats):
        best_dragon = ''
        best_successrate = 0
        for dragon_name in dragon_stats:
            if dragon_stats[dragon_name]['success_rate'] > best_successrate:
                best_dragon = dragon_name
                best_successrate = dragon_stats[dragon_name]['success_rate']
        return best_dragon
