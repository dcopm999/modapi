'''
add: Goods
module: admin
'''
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import ugettext_lazy as _

from goods import models


class GalleryInline(AdminImageMixin, admin.TabularInline):
    model = models.Gallery


class VarietyInline(AdminImageMixin, admin.TabularInline):
    inlines = [GalleryInline, ]
    model = models.Variety
    suit_classes = 'suit-tab suit-tab-varieties'


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    MPTT_ADMIN_LEVEL_INDENT = 20
    list_display = ['name', ]


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    inlines = [VarietyInline, ]
    list_display = ['article', 'name', 'desc', 'category',
                    'brand', 'price', 'discount', 'collection', 'created', 'updated']
    suit_form_tabs = (('general', _('General')), ('details', _('Details')), ('varieties', _('Varieties')))

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['brand', 'collection', 'article', 'category', 'name', 'desc', 'price', 'discount']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-details',),
            'fields': [('info', 'composition'), 'care_type'], }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-varieties',),
            'fields': []}),
    ]


@admin.register(models.Variety)
class VarietyAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [GalleryInline, ]
    list_display = ['good', 'color', 'price', 'in_stock']
    list_filter = ['in_stock', ]


@admin.register(models.CareType)
class CareTypeAdmin(admin.ModelAdmin):
    list_display = ['name', ]
