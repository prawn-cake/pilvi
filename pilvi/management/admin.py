# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Client, ProxyResource, HTTPMethod, ApiEndpoint


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', )


class ProxyHttpMethodsInline(admin.TabularInline):
    model = ProxyResource.methods.through


@admin.register(ProxyResource)
class ProxyResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'display_methods', 'endpoint')
    list_filter = ('endpoint', )
    # inlines = [ProxyHttpMethodsInline]


@admin.register(HTTPMethod)
class HTTPMethodAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        """Restrict to remove HTTP methods from the admin"""
        return False

    # def get_actions(self, request):
    #     actions = super(HTTPMethodAdmin, self).get_actions(request)
    #
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions


@admin.register(ApiEndpoint)
class ApiEndpoinAdmin(admin.ModelAdmin):
    list_display = ('path', )
