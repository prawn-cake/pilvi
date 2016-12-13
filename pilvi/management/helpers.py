# -*- coding: utf-8 -*-

HTTP_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH')


def create_http_methods(apps, schema_editor):
    """Migration method helper

    :param apps:
    :param schema_editor:
    """
    app_name, model_name = 'management', 'HTTPMethod'
    HTTPMethod = apps.get_model(app_name, model_name)
    for name in HTTP_METHODS + ('ANY', ):
        method = HTTPMethod(name=name)
        method.save()
