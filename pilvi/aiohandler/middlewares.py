# -*- coding: utf-8 -*-
"""aiohandler middlewares"""

import logging
import jwt
from aiohttp.web_exceptions import HTTPForbidden
from jwt import exceptions as jwt_exc
from pilvi.aiohandler import helpers
from pilvi.aiohandler.exceptions import TokenError, TokenExpired
from django.conf import settings


logger = logging.getLogger(__name__)


async def jwt_auth_middleware(app, handler):
    """JWT authentication middleware
    Docs: http://aiohttp.readthedocs.io/en/stable/web.html#middlewares

    :param app: application instance
    :param handler: handler returned by the next middleware factory
    """

    async def middleware_handler(request):
        cache = helpers.Cache.get_cache()
        token = JWTAuth.get_token(request.headers)
        try:
            payload = JWTAuth.decode_token(token)
        except jwt_exc.DecodeError as err:
            logger.error(err)
            raise HTTPForbidden(text=str(err))

        user_id = payload['user_id']
        user_data = await cache.get_user_data(user_id=user_id)
        return await handler(request)

    return middleware_handler


class JWTAuth(object):
    """Authentication based on JWT tokens"""

    TOKEN_TYPE = 'Bearer'

    def __init__(self, cache):
        super(JWTAuth, self).__init__()
        self.cache = cache

    def _authorize(self, headers):
        """Common authorization function

        :param headers: aiohttp headers
        :return:
        """
        # Token is not given case, may raises a TokenError
        token = JWTAuth.get_token(headers)

        # Wrong token is given case
        try:
            payload = JWTAuth.decode_token(token)
        except jwt_exc.DecodeError as err:
            raise TokenError(str(err))

        user_id = payload['user_id']
        # NOTE: if data still is in cache
        user_data = self.cache.get_user_data(user_id=user_id)
        if not user_data:
            raise TokenExpired(
                'User %d oauth token is expired (no data in cache). '
                'Need to login again' % user_id)
        return user_data

    def authorize(self):
        try:
            # TODO: implement this
            pass
        except TokenError as err:
            logger.error(err)
            return False

        return True

    @staticmethod
    def get_token(headers):
        """Extract token from HTTP headers

        :param headers: flask.request.headers
        """
        bearer = headers.get('Authorization')
        if bearer:
            try:
                token_type, token = bearer.rsplit(' ', 1)
            except ValueError:
                raise TokenError('Wrong bearer string: %s', bearer)

            if token_type != 'Bearer':
                raise TokenError('Wrong token type: %s, must be %s',
                                 token_type, 'Bearer')
            return token
        raise TokenError('No token is given in the Authorization header')

    @staticmethod
    def decode_token(token):
        """Get decoded payload from token

        :param token: str: token string
        :return: dict: payload
        :raise: jwt.exceptions.DecodeError
        """

        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])

    @staticmethod
    def encode_token(payload):
        """Encode token

        :param payload: dict: data payload
        :return: str: token string
        """
        return jwt.encode(payload=payload,
                          key=settings.JWT_SECRET,
                          algorithm=settings.JWT_ALGO)
