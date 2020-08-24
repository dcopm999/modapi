
'''
app: goods
module: models
TODO: description
'''
from django.db import models
from sorl.thumbnail import ImageField
from mptt.models import MPTTModel, TreeForeignKey

from django.utils.translation import ugettext_lazy as _


class Category(MPTTModel):
    name = models.CharField(max_length=250, db_index=True, unique=True)
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


class Good(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('Brand'))
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    article = models.CharField(max_length=250, null=True, verbose_name=_('Article'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Price'))
    discount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Discount'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Good')
        verbose_name_plural = _('Goods')


class Image(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name=_('Good'))
    image = ImageField(upload_to='goods', verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
