# -*- coding: utf-8 -*-
import aiohttp
import time
import logging
from aiohttp import web
from aiohttp import client
from yarl import URL


logger = logging.getLogger(__name__)


class ProxyRoute(object):
    def __init__(self, url, protected=True):
        """
        :param url: yarl.URL instance
        :param protected: bool
        """
        self._url = url
        self.protected = protected

    @property
    def url(self):
        return str(self._url)

    def __str__(self):
        return "%s(url=%s)" % (self.__class__.__name__, self._url)


class ProxyRouter(web.UrlDispatcher):
    def __init__(self, app):
        super().__init__(app)
        self._proxy_table = {}

    def add_proxy_route(self, methods, path, proxy_pass, *, name=None,
                        expect_handler=None, protected=True):
        """
        :param methods: list of str
        :param proxy_pass: str: must be an URL like http://localhost:8000
        :return:

        NOTE: Check https://www.python.org/dev/peps/pep-3102/ about the '*' in
        the args
        """

        resource = self.add_resource(path, name=name)
        # if isinstance(resource, DynamicResource):
        #     info = resource.get_info()

        proxy_url = URL(proxy_pass)
        for method in methods:
            route = resource.add_route(method, proxy_handler,
                                       expect_handler=expect_handler)
            self.set_proxy_route(route, proxy_url, protected=protected)

    def set_proxy_route(self, route, proxy_url, protected):
        self._proxy_table[route] = ProxyRoute(url=proxy_url,
                                              protected=protected)

    def get_proxy_route(self, route):
        return self._proxy_table[route]


class ReversedProxyResponse(client.ClientResponse):
    """Raw response"""

    pass


async def proxy_handler(request):
    """Default reverse proxy handler

    :param request:
    """
    chunk_size = 32768
    route = request.match_info.route
    app = request.app
    start = time.time()
    proxy_route = app.router.get_proxy_route(route)
    logger.info('Proxy handler: %s -> %s', route, proxy_route.url)

    # TODO: add timeouts
    async with aiohttp.client.ClientSession(
            response_class=ReversedProxyResponse) as session:
        proxy_request_timeout = 5
        proxy_params = dict(method=request.method,
                            url=proxy_route.url,
                            headers=request.headers,
                            params=request.url.query,
                            chunked=chunk_size,
                            timeout=proxy_request_timeout)

        async with session.request(**proxy_params) as proxy_resp:
            response = aiohttp.web.StreamResponse(status=proxy_resp.status,
                                                  headers=proxy_resp.headers)
            await response.prepare(request)
            content = proxy_resp.content
            while True:
                chunk = await content.read(chunk_size)
                if not chunk:
                    break
                response.write(chunk)

            await response.write_eof()
            logger.info('elapsed %.2fs', time.time() - start)
            return response
