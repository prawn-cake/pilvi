# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Client, ProxyResource, HTTPMethod, Api


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', )
    readonly_fields = ('api_key', )

    def save_model(self, request, obj, form, change):
        if not obj.api_key:
            obj.api_key = Client.generate_api_key()
        return super(ClientAdmin, self).save_model(request, obj, form, change)


class ProxyHttpMethodsInline(admin.TabularInline):
    model = ProxyResource.methods.through


@admin.register(ProxyResource)
class ProxyResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'api', 'display_methods', 'endpoint_url')
    list_filter = ('api', )
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


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', )


# Customize admin titles
admin.site.site_header = ugettext_lazy('Pilvi management')
admin.site.site_title = ugettext_lazy('Pilvi management')
