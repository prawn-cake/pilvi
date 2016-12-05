# -*- coding: utf-8 -*-


class HandlerError(Exception):
    """ Custom exception class"""

    pass


class AuthError(HandlerError):
    pass


class TokenError(AuthError):
    pass


class TokenExpired(AuthError):
    pass