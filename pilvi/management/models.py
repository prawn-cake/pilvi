# -*- coding: utf-8 -*-
import urllib.parse

from django.core.exceptions import ValidationError
from django.db import models


class Client(models.Model):
    """Client application account"""

    name = models.CharField(unique=True, max_length=256)
    api_key = models.CharField(unique=True, max_length=256)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.name)


#TODO: added default data migration to prefill the values
class HTTPMethod(models.Model):
    """Static list of HTTP methods"""

    name = models.CharField(max_length=10, unique=True,
                            choices=[('GET', 'GET'),
                                     ('POST', 'POST'),
                                     ('PUT', 'PUT'),
                                     ('DELETE', 'DELETE'),
                                     ('PATCH', 'PATCH'),
                                     ('HEAD', 'HEAD')])

    def __str__(self):
        return self.name


class ProxyResource(models.Model):
    """Proxy resource. It indicates"""

    name = models.CharField(max_length=256)
    url = models.URLField()
    methods = models.ManyToManyField(HTTPMethod)
    endpoint = models.ForeignKey('ApiEndpoint',
                                 on_delete=models.CASCADE,
                                 help_text='API endpoint')
    protected = models.BooleanField(default=True,
                                    help_text='Indicates that resource is '
                                              'protected with JWT token')

    def display_methods(self):
        """Django admin helper to display m2m field

        :return: str
        """
        return ', '.join([method.name for method in self.methods.all()])

    display_methods.short_description = 'Allowed methods'

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.name)


def validate_endpoint(value):
    url = urllib.parse.urlparse(value)
    if not url.path.startswith('/'):
        raise ValidationError('URL path must start with /')


class ApiEndpoint(models.Model):
    path = models.CharField(max_length=2083,
                            unique=True,
                            validators=[validate_endpoint],
                            help_text='For example: /api/v1 .This endpoint will be available as http(s)://0.0.0.0/api/v1')

    def __str__(self):
        return self.path


class HandlersRegistry(models.Model):
    """Registry for aiohandlers"""

    name = models.CharField(max_length=256, unique=True)
    hostname = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
