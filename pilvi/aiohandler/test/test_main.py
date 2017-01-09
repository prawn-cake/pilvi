# -*- coding: utf-8 -*-
import django
django.setup()

from django.conf import settings
from pilvi.management.models import Client
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from pilvi.aiohandler.main import create_app
from unittest import mock


class AioHandlerTestCase(AioHTTPTestCase):
    def get_app(self, loop):
        app = create_app(loop=loop)
        return app


class AsyncMock(mock.MagicMock):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return True


class HandlerTest(AioHandlerTestCase):
    @unittest_run_loop
    async def test_example(self):
        # TODO: create resources dynamically
        resp = await self.client.request("GET", "/api/test_service")
        self.assertEqual(resp.status, 200)
        json_data = await resp.json()
        self.assertEqual(json_data, {'service': 'test_service', 'status': 'OK'})

    @unittest_run_loop
    async def test_proxy(self):
        with mock.patch('aiohttp.client.ClientSession', new_callable=AsyncMock) as session:
            resp = await self.client.request("GET", "/some/path?a=1&b=2")
        self.assertEqual(resp.status, 200)
        json_data = await resp.json()
        self.assertEqual(json_data, {'service': 'test_service', 'status': 'OK'})


class AuthTest(AioHandlerTestCase):
    # def setUp(self):
    #     pass

    def tearDown(self):
        Client.objects.all().delete()

    @unittest_run_loop
    async def test_jwt_auth_handler_fail_on_no_api_key(self):
        resp = await self.client.request("POST", "/auth")
        self.assertEqual(resp.status, 400)
        self.assertEqual(await resp.text(), 'No api key is given')

    @unittest_run_loop
    async def test_jwt_auth_handler_fail_on_no_such_client(self):
        api_key = 'aaaa'
        resp = await self.client.request(
            "POST", "/auth",
            headers={settings.AIOHANDLER['auth.header']: api_key})
        self.assertEqual(resp.status, 400)
        self.assertEqual(await resp.text(), 'Such client does not exist')

    @unittest_run_loop
    async def test_jwt_auth_handler_fail_on_client_is_not_active(self):
        api_key = 'aaaa'
        Client.objects.create(name='test_client', api_key=api_key)
        resp = await self.client.request(
            "POST", "/auth",
            headers={settings.AIOHANDLER['auth.header']: api_key})
        self.assertEqual(resp.status, 403)
        self.assertEqual(await resp.text(), 'Client is not active')

    @unittest_run_loop
    async def test_jwt_auth_handler(self):
        from pilvi.aiohandler.helpers import JWTManager

        api_key = 'aaaa'
        client = Client.objects.create(name='test_client',
                                       api_key=api_key,
                                       is_active=True)
        resp = await self.client.request(
            "POST", "/auth",
            headers={settings.AIOHANDLER['auth.header']: api_key})
        self.assertEqual(resp.status, 200)
        json_data = await resp.json()
        self.assertTrue(json_data['token'])

        payload = JWTManager.decode_token(json_data['token'])
        self.assertEqual(payload['client_id'], client.pk)
