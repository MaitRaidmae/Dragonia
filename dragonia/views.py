from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
    )

from .security import (
    USERS,
    check_password
)

from .GameObjects import (
    dragon,
    mugloarGame
)


@view_defaults(renderer='Views\home.pt')
class DragoniaViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home', renderer='Views\home.pt')
    @forbidden_view_config(renderer='home.pt')
    def home(self):
        request = self.request
        login_url = request.route_url('home')
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
            if check_password(password, USERS.get(login)):
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
        dragon_dict = {
            'scale_thickness': 10,
            'claw_sharpness': 5,
            'wing_strength': 4,
            'fire_breath': 1
        }
        my_dragon = dragon.Dragon(dragon_dict)
        game = mugloarGame.MugloarGame(self.logged_in)
        game.get_knight()
        return {'page_title': 'Dragonia',
                'game_id': game.game_id,
                'knight_name': game.knight.name,
                'knight': game.knight.description}
