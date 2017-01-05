# -*- coding: utf-8 -*-
"""aiohandler middlewares"""

import logging

from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest
from django.conf import settings
from jwt import exceptions as jwt_exc

from pilvi.aiohandler import helpers
from pilvi.aiohandler.exceptions import TokenError
from pilvi.aiohandler.helpers import JWTManager

logger = logging.getLogger(__name__)


async def jwt_auth_middleware(app, handler):
    """JWT authentication middleware
    Docs: http://aiohttp.readthedocs.io/en/stable/web.html#middlewares

    :param app: application instance
    :param handler: handler returned by the next middleware factory
    """

    async def middleware_handler(request):
        cache = helpers.Cache.get_cache()
        try:
            token = JWTManager.get_token(request.headers)
        except TokenError as err:
            logger.error(err)
            raise HTTPForbidden(text=str(err))

        try:
            payload = JWTManager.decode_token(token)
        except jwt_exc.DecodeError as err:
            # Wrong token is given case
            logger.error(err)
            raise HTTPForbidden(text=str(err))

        user_id = payload['user_id']
        user_data = await cache.get_user_data(user_id=user_id)
        if not user_data:
            msg = 'User %d oauth token is expired (no data in cache). ' \
                  'Need to login again' % user_id
            raise HTTPForbidden(text=msg)
        return await handler(request)

    return middleware_handler


async def token_auth_middleware(app, handler):
    """Simple token auth middleware to check the token on every request

    :param app: application instance
    :param handler: handler returned by the next middleware factory
    """
    async def middleware_handler(request):
        cache = helpers.Cache.get_cache()
        api_key = request.headers.get(settings.AIOHANDLER['auth.header'])
        if not api_key:
            msg = 'No api key is given'
            logger.warning('Bad request: %s', msg)
            raise HTTPBadRequest(text=msg)

        payload = await cache.get_client_data(api_key=api_key)
        if not payload:
            logger.warning("API key '%s' is invalid or expired" % api_key)
            raise HTTPForbidden()

        request['client'] = payload
        logger.info('%s is authenticated', api_key)
        return await handler(request)

    return middleware_handler


async def check_route_middleware(app, handler):
    """This middleware checks client routes

    :param app: application instance
    :param handler: handler returned by the next middleware factory
    :return:
    """

    async def middleware_handler(request):
        # NOTE: this should come from the token_auth_middleware
        client = request['client']
        cache = helpers.Cache.get_cache()
        route = request.match_info.route
        proxy_route = app.router.get_proxy_route(route)

        # TODO: implement this
        client_routes = await cache.get('routes:%d' % client['id'])

        if proxy_route.url not in client_routes:
            raise HTTPForbidden(text='Forbidden route')
        return await handler(request)

    return middleware_handler
