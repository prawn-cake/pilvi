# -*- coding: utf-8 -*-
import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from pilvi.management.models import ProxyResource, Client
from pilvi.management.helpers import generate_api_key


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
