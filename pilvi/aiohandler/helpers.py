# -*- coding: utf-8 -*-
import aioredis
from django.conf import settings


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

    async def get(self, key):
        return await self._cache.get(key)

    async def set(self, key):
        return await self._cache.set(key)

    @staticmethod
    def get_cache(**kwargs):
        return Cache(address=settings.REDIS_SETTINGS, **kwargs)
