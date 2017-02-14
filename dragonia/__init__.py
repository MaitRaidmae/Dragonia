from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='.resources.Root')
    config.include('pyramid_chameleon')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['dragonia.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.add_route('create_user', '/create_pet')
    config.add_route('dragonia_main', '/dragonia_main')
    config.add_route('battle', '/battle/{dragon}/{game_id}')
    config.scan('.views')
    return config.make_wsgi_app()