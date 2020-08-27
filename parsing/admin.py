# -*- coding: utf-8 -*-
from django.contrib import admin

from parsing import models


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['brand', 'url', 'created', 'enabled']
    list_filter = ['enabled']


@admin.register(models.Sitemap)
class SitemapAdmin(admin.ModelAdmin):
    list_display = ['site', 'url', 'created', 'enabled']
    list_filter = ['site__url', 'enabled']
    date_hierarchy = 'lastmod'
    search_fields = ['site__url', 'url']


@admin.register(models.GoodURL)
class GoodURLAdmin(admin.ModelAdmin):
    list_display = ['sitemap', 'url', 'edited', 'created', 'enabled']
    list_filter = ['sitemap', 'enabled']
    date_hierarchy = 'edited'
    search_fields = ['sitemap__url', 'url']


@admin.register(models.GoodMapping)
class GoodMappigAdmin(admin.ModelAdmin):
    list_display = ['site', ]
