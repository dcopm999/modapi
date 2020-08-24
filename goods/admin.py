'''
add: Goods
module: admin
'''
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import ugettext_lazy as _

from goods import models


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = models.Image


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    MPTT_ADMIN_LEVEL_INDENT = 20
    list_display = ['name', ]


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]
    list_display = ['article', 'name', 'description', 'category', 'brand', 'price', 'discount', 'created', 'updated']
    suit_form_tabs = (('general', _('General')), ('details', _('Details')), )

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['brand', 'name', 'category', 'article', 'description', 'price', 'discount']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-varieties',),
            'fields': []}),
    ]
