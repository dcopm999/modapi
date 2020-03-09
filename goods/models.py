'''
app: goods
module: models
TODO: description
'''
from django.db import models
from sorl.thumbnail import ImageField
from mptt.models import MPTTModel, TreeForeignKey

from django.utils.translation import ugettext_lazy as _


class Collection(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class Color(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')


class Size(models.Model):
    name = models.CharField(max_length=4, verbose_name=_('Size'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')


class CareType(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Care Type')
        verbose_name_plural = _('Care Types')


class Good(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    desc = models.CharField(max_length=200, blank=True, verbose_name=_('Description'))
    article = models.CharField(max_length=50, null=True, verbose_name=_('Article'))
    info = models.TextField(blank=True, verbose_name=_('Model info'))
    composition = models.TextField(blank=True, verbose_name=('Composition'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('Brand'))
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Price'))
    discount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Discount'))
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,
                                   null=True, blank=True, verbose_name=_('Collection'))
    care_type = models.ManyToManyField(CareType, verbose_name=_('Care'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Good')
        verbose_name_plural = _('Goods')


class Variety(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name=_('Good'))
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_('Color'))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_('Size'))
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Prices'))
    image = ImageField(upload_to='goods', blank=True, verbose_name=_('Image'))
    in_stock = models.BooleanField(default=False, verbose_name=_('In stock'))

    def __str__(self):
        return f'{self.good}: color:{self.color}, size:{self.size}, in_stock:{self.in_stock}'

    class Meta:
        verbose_name = _('Variety')
        verbose_name_plural = _('Varieties')


class Gallery(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, verbose_name=_('Variety'))
    image = ImageField(upload_to='goods', verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
