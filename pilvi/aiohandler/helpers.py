# -*- coding: utf-8 -*-
from werkzeug.contrib import cache as caches


CACHE_MAP = {
    'simple': caches.SimpleCache,
    'redis': caches.RedisCache,
    'file': caches.FileSystemCache
}

cache = None


def get_cache(cache_type='simple', **kwargs):
    global cache
    if not cache:
        cache = CACHE_MAP[cache_type](**kwargs)
    return cache
