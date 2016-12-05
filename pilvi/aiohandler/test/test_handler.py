# -*- coding: utf-8 -*-
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from pilvi.aiohandler.main import app
from unittest import mock


class AsyncMock(mock.MagicMock):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return True


class HandlerTest(AioHTTPTestCase):
    def get_app(self, loop):
        app._loop = loop
        return app

    @unittest_run_loop
    async def test_example(self):
        resp = await self.client.request("GET", "/api/sysdev")
        self.assertEqual(resp.status, 200)
        json_data = await resp.json()
        self.assertEqual(json_data, {'service': 'sysdev', 'status': 'OK'})

    @unittest_run_loop
    async def test_proxy(self):
        with mock.patch('aiohttp.client.ClientSession', new_callable=AsyncMock) as session:
            resp = await self.client.request("GET", "/some/path?a=1&b=2")
        self.assertEqual(resp.status, 200)
        json_data = await resp.json()
        self.assertEqual(json_data, {'service': 'sysdev', 'status': 'OK'})

