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


@view_defaults(renderer='Views\welcome_to_dragonia.pt')
class DragoniaViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='welcome_to_dragonia', renderer='Views\welcome_to_dragonia.pt')
    @forbidden_view_config(renderer='welcome_to_dragonia.pt')
    def welcome_to_dragonia(self):
        request = self.request
        login_url = request.route_url('welcome_to_dragonia')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user_password = models.DBSession.query(models.User).filter_by(user_id=login).first().password
            if check_password(password, user_password):
                main_url = request.route_url('dragonia_main')
                headers = remember(request, login)
                return HTTPFound(location=main_url,
                                 headers=headers)
            message = 'Failed login'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)

    @view_config(route_name='dragonia_main', renderer='Views\dragonia_main.pt')
    def dragonia_main(self):
        game = mugloarGame.MugloarGame(self.logged_in)
        game.get_knight()
        models.DBSession.add(models.MugloarGame(
            game_id=game.game_id,
            user_uid=self.request.authenticated_userid,
            knight_agility=game.knight.agility,
            knight_endurance=game.knight.endurance,
            knight_armor=game.knight.armor,
            knight_attack=game.knight.attack,
            weather=game.weather
        ))
        return {'page_title': 'Dragonia',
                'game_id': game.game_id,
                'knight_name': game.knight.name,
                'knight': game.knight.description,
                'weather': game.weather}

    @view_config(route_name='battle', renderer='Views\\battle.pt')
    def battle(self):
        selected_dragon = self.request.matchdict['dragon']
        if selected_dragon == 'scaly':
            dragon_dict = {
                'scale_thickness': 10,
                'claw_sharpness': 5,
                'wing_strength': 4,
                'fire_breath': 1
            }
        elif selected_dragon == 'wingy':
            dragon_dict = {
                'scale_thickness': 1,
                'claw_sharpness': 5,
                'wing_strength': 10,
                'fire_breath': 4
            }
        elif selected_dragon == 'clawy':
            dragon_dict = {
                'scale_thickness': 2,
                'claw_sharpness': 10,
                'wing_strength': 3,
                'fire_breath': 5
            }
        elif selected_dragon == 'flamy':
            dragon_dict = {
                'scale_thickness': 1,
                'claw_sharpness': 5,
                'wing_strength': 4,
                'fire_breath': 10
            }

        my_dragon = dragon.Dragon(dragon_dict)
        mugloar_game_id = self.request.matchdict['game_id']
        battleresult_json = my_dragon.attack(mugloar_game_id).text
        battleresult_dict = json.loads(battleresult_json)
        print(battleresult_dict)
        game_uid = models.DBSession.query(models.MugloarGame).filter_by(game_id=mugloar_game_id).first().uid
        print(game_uid)
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

    @view_config(route_name='create_new_pet', renderer='Views\create_new_pet.pt')
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
            elif len(secret_word) < 5:
                message = 'That''s a terrible secret word. Use at least 5 runes.'
            elif pet_name_found is not None:
                message = 'Pet with name %s already exist. Please do not try to have two pets with the same name. ' \
                          'It confuses the dragons.' % new_pet_name
            elif secret_word != repeat_secret_word:
                message = 'Your secret word repeat typing skills are lacking. Please try again'
            else:
                hashed_password = hash_password(secret_word)
                models.DBSession.add(models.User(user_id=new_pet_name,password=hashed_password))
                return HTTPFound(location=self.request.route_url('welcome_to_dragonia'))
        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            new_pet_name=new_pet_name,
            secret_word=secret_word,
            repeat_secret_word=repeat_secret_word
        )
