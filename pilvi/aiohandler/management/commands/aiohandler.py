# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from pilvi.aiohandler.main import sslcontext, create_app
from aiohttp import web


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--port', default=8010)

    def handle(self, *args, **options):
        # TODO: override run_app
        # TODO: support optional ssl
        app = create_app()
        web.run_app(app, port=options['port'], ssl_context=sslcontext)
