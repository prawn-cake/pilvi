# -*- coding: utf-8 -*-
import aioredis
import jwt
from django.conf import settings

from pilvi.aiohandler.exceptions import TokenError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class Cache(object, metaclass=Singleton):
    def __init__(self, address, **kwargs):
        self._cache = aioredis.create_reconnecting_redis(address=address,
                                                         **kwargs)

    async def get_user_data(self, user_id):
        return await self._cache.get('user:%s' % str(user_id))

    async def set_user_data(self, user_id, data, expire=0):
        await self._cache.set('user:%s' % str(user_id), data, expire=expire)

    async def set_client_data(self, api_key, data, expire=0):
        await self._cache.set('client:%s' % str(api_key), data, expire=expire)

    async def get_client_data(self, api_key):
        await self._cache.get('client:%s' % str(api_key))

    async def remove_client_data(self, api_key):
        await self._cache.delete('client:%s' % str(api_key))

    async def get(self, key):
        return await self._cache.get(key)

    async def set(self, key):
        return await self._cache.set(key)

    @staticmethod
    def get_cache(**kwargs):
        return Cache(address=settings.REDIS_SETTINGS, **kwargs)


class JWTManager(object):
    """JWT tokens manager helpers. It contains methods to work with jwt"""

    TOKEN_TYPE = 'Bearer'

    def __init__(self, cache):
        super(JWTManager, self).__init__()
        self.cache = cache

    @staticmethod
    def get_token(headers):
        """Extract token from HTTP headers

        :param headers: aiohttp.request.headers
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