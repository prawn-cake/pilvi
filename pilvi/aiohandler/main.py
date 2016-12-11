# -*- coding: utf-8 -*-
import asyncio
import logging
import ssl
import os.path as op
from aiohttp import web
from pilvi.aiohandler.proxy import ProxyRouter
from pilvi.management.models import ProxyResource
from django.conf import settings


CUR_DIR = op.abspath(op.dirname(__file__))
logger = logging.getLogger(__name__)

# Create ssl context if enabled
sslcontext = None
if settings.AIOHANDLER['ssl.enabled']:
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.load_cert_chain(settings.AIOHANDLER['ssl.crt'],
                               settings.AIOHANDLER['ssl.key'])


class CustomRequestHandlerFactory(web.RequestHandlerFactory):
    def __init__(self, app, router, **kwargs):
        """

        :param app:
        :param router:
        :param kwargs: keepalive_timeout=75,  # NGINX default value is 75 secs
                       tcp_keepalive=True,
                       slow_request_timeout=0,
                       logger=server_logger,
                       access_log=access_logger,
                       access_log_format=helpers.AccessLogger.LOG_FORMAT,
                       debug=False,
                       max_line_size=8190,
                       max_headers=32768,
                       max_field_size=8190,
        """
        super().__init__(app, router, **kwargs)


def create_app():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop,
                          handler_factory=CustomRequestHandlerFactory)
    proxy_router = ProxyRouter(app=app)
    app._router = proxy_router

    resources = ProxyResource.objects.all()\
        .select_related('endpoint')\
        .prefetch_related('methods')

    for resource in resources:
        methods = [method.name for method in resource.methods.all()]
        path = '{endpoint}/{name}'.format(endpoint=resource.endpoint.path,
                                          name=resource.name)
        logger.info('Register {} --> {} [{}]'.format(path, resource.url, ','.join(methods)))
        app.router.add_proxy_route(methods=methods,
                                   path=path,
                                   proxy_pass=resource.url)
    return app
