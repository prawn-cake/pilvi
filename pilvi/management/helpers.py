# -*- coding: utf-8 -*-


def create_http_methods(apps, schema_editor):
    """Migration method helper

    :param apps:
    :param schema_editor:
    """
    app_name, model_name = 'management', 'HTTPMethod'
    HTTPMethod = apps.get_model(app_name, model_name)
    for name in 'GET', 'POST', 'PUT', 'DELETE':
        method = HTTPMethod(name=name)
        method.save()
