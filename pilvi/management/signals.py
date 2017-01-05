# -*- coding: utf-8 -*-
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict

from pilvi.aiohandler import helpers
from pilvi.management.models import ProxyResource, Client


logger = logging.getLogger(__name__)


@receiver(signal=post_save, sender=ProxyResource)
def save_proxy_resource(sender, **kwargs):
    """ProxyResource was created/updated. Notify aiohandlers about the change.

    :param sender: ProxyResource
    :param kwargs:
    """
    pass


@receiver(signal=post_delete, sender=ProxyResource)
def delete_proxy_resource(sender, **kwargs):
    """ProxyResource was deleted. Notify aiohandlers about the change.

    :param sender: ProxyResource
    :param kwargs:

    """
    pass


@receiver(signal=post_save, sender=Client)
def save_client(sender, **kwargs):
    """Update client info when a client has been created or updated.

    :param sender: Client
    :param kwargs:
    """
    cache = helpers.Cache.get_cache()
    client = kwargs['instance']
    cache.set_client_data(api_key=client.api_key, data=model_to_dict(client))


@receiver(signal=post_delete, sender=Client)
def delete_client(sender, **kwargs):
    """Remove api key when client has been deleted.

    :param sender: Client
    :param kwargs:

    """
    cache = helpers.Cache.get_cache()
    client = kwargs['instance']
    cache.remove_client_data(api_key=client.api_key)
