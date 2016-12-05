# -*- coding: utf-8 -*-
import aiohttp
import time
import logging
from aiohttp import web
from aiohttp import client
from yarl import URL


logger = logging.getLogger(__name__)


class ProxyRouter(web.UrlDispatcher):
    def __init__(self, app):
        super().__init__(app)
        self._proxy_table = {}

    def add_proxy_route(self, methods, path, proxy_pass, *, name=None,
                        expect_handler=None):
        """
        :param methods: list of str
        :param proxy_pass: str: must be an URL like http://localhost:8000
        :return:
        """
        resource = self.add_resource(path, name=name)
        # if isinstance(resource, DynamicResource):
        #     info = resource.get_info()

        proxy_url = URL(proxy_pass)
        for method in methods:
            route = resource.add_route(method, proxy_handler,
                                       expect_handler=expect_handler)
            self.set_proxy(route, proxy_url)

    def set_proxy(self, route, proxy_url):
        self._proxy_table[route] = proxy_url

    def get_proxy(self, route):
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
    proxy_url = app.router.get_proxy(route)
    logger.info('Proxy handler: %s -> %s', route, str(proxy_url))

    # TODO: add timeouts
    async with aiohttp.client.ClientSession(
            response_class=ReversedProxyResponse) as session:
        proxy_request_timeout = 5
        proxy_params = dict(method=request.method,
                            url=str(proxy_url),
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
