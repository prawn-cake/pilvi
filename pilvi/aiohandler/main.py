# -*- coding: utf-8 -*-
import asyncio
import logging
import ssl
import os.path as op
from aiohttp import web
from pilvi.aiohandler.proxy import ProxyRouter
from pilvi.management.models import ProxyResource


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
# )
logger = logging.getLogger(__name__)


SERVICES = ['sysdev', 'smapp']
CUR_DIR = op.abspath(op.dirname(__file__))


async def service_handler(request):
    # NOTE: stub method
    service_name = request.match_info.get('service')
    if service_name not in SERVICES:
        return web.HTTPBadRequest(reason="Service %s is not registered" %
                                         service_name)
    logger.info(request)
    return web.json_response(data={'service': service_name,
                                   'status': 'OK',
                                   'proxy_url': str(request.url)})


async def api(request):
    service_name = request.match_info.get('service')
    if not service_name:
        return web.HTTPBadRequest(
            reason="Service is not set. Query /api/{service_name}")
    if service_name not in SERVICES:
        return web.HTTPBadRequest(reason="Service %s is not registered" %
                                         service_name)

    return web.HTTPFound(str(request.url) + '/handler')


sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.load_cert_chain(CUR_DIR + '/ssl/domain.crt',
                           CUR_DIR + '/ssl/domain.key')


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


loop = asyncio.get_event_loop()
app = web.Application(loop=loop, handler_factory=CustomRequestHandlerFactory)
proxy_router = ProxyRouter(app=app)
app._router = proxy_router

resources = ProxyResource.objects.all().select_related('endpoint').prefetch_related('methods')
for resource in resources:
    methods = [method.name for method in resource.methods.all()]
    path = '{endpoint}/{name}'.format(endpoint=resource.endpoint.path,
                                      name=resource.name)
    logger.info('Register {} --> {} [{}]'.format(path, resource.url, ','.join(methods)))
    app.router.add_proxy_route(methods=methods,
                               path=path,
                               proxy_pass=resource.url)
