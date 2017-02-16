from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import models

from .security import groupfinder


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings,
                          root_factory='.resources.Root')
    config.include('pyramid_chameleon')

    models.DBSession.configure(bind=engine)
    models.Base.metadata.bind = engine

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['dragonia.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('welcome_to_dragonia', '/')
    config.add_route('logout', '/logout')
    config.add_route('dragonia_main', '/dragonia_main')
    config.add_route('battle', '/battle/{dragon}/{game_id}')
    config.add_route('create_new_pet', '/create_new_pet')
    config.add_route('the_den_of_dragons', '/the_den_of_dragons/{user_id}')
    config.add_static_view(name='static', path='dragonia:static')
    config.scan('.views')
    return config.make_wsgi_app()