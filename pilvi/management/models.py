# -*- coding: utf-8 -*-
import urllib.parse
import uuid

from django.core.exceptions import ValidationError
from django.db import models


class TimeTrackableModel(models.Model):
    """Abstract model which implements two fields to track timestamps """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Resource(TimeTrackableModel):
    name = models.CharField(max_length=256)

    class Meta:
        abstract = True


class Client(TimeTrackableModel):
    """Client application account"""

    name = models.CharField(unique=True, max_length=256)
    api_key = models.CharField(unique=True, max_length=256, editable=False)
    is_active = models.BooleanField(default=False)
    resources = models.ManyToManyField('management.ProxyResource')

    @staticmethod
    def generate_api_key():
        return 'api-{}'.format(str(uuid.uuid4()).replace('-', ''))

    def available_resources(self):
        return list(self.resources.all())

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.name)

    def cache_clients(self):
        pass


class HTTPMethod(models.Model):
    """Static list of HTTP methods"""

    name = models.CharField(max_length=10, unique=True,
                            choices=[('GET', 'GET'),
                                     ('POST', 'POST'),
                                     ('PUT', 'PUT'),
                                     ('DELETE', 'DELETE'),
                                     ('PATCH', 'PATCH'),
                                     ('OPTIONS', 'OPTIONS'),
                                     ('ANY', 'ANY'),
                                     ('HEAD', 'HEAD')])

    def __str__(self):
        return self.name


class ProxyResource(Resource):
    """Proxy resource. It indicates"""

    endpoint_url = models.URLField(help_text='For example: http(s)://myservice:8001')
    methods = models.ManyToManyField(HTTPMethod)
    api = models.ForeignKey('management.Api',
                            on_delete=models.CASCADE,
                            help_text='API entrypoint')
    protected = models.BooleanField(default=True,
                                    help_text='Indicates that resource is '
                                              'protected with token')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_methods(self):
        """Django admin helper to display m2m field

        :return: str
        """
        return ', '.join([method.name for method in self.methods.all()])

    display_methods.short_description = 'Allowed methods'

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.name)


def validate_api_path(value):
    url = urllib.parse.urlparse(value)
    if not url.path.startswith('/'):
        raise ValidationError('URL path must start with /')


# TODO: make this as a proxy resource abstract model
class Api(TimeTrackableModel):
    """API Resource model"""

    path = models.CharField(max_length=2083,  # max url length
                            unique=True,
                            validators=[validate_api_path],
                            help_text='For example: /api/v1 .This endpoint will be available as http(s)://0.0.0.0/api/v1')

    def __str__(self):
        return self.path


class HandlersRegistry(TimeTrackableModel):
    """Registry for aiohandlers"""

    name = models.CharField(max_length=256, unique=True)
    hostname = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
