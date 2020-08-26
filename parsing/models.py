# -*- coding: utf-8 -*-
import logging
import json
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from config import celery_app

from goods import models as goods_models


logger = logging.getLogger(__name__)


class Site(models.Model):
    brand = models.ForeignKey(goods_models.Brand, on_delete=models.CASCADE, verbose_name=_('Brand'))
    url = models.URLField(db_index=True, verbose_name=_('Site url'))
    slug = models.SlugField(blank=True, verbose_name=_('Slug'))
    schedule = models.ForeignKey(IntervalSchedule, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, null=True, blank=True)
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
    
    def get_absolute_url(self):
        return reverse('parsing:site-detail', kwargs={'slug': self.slug})

    def task_create_or_update(self):
        if self.task is None:
            task = PeriodicTask(
                interval = self.schedule,
                name = f'{self.brand.name}.robots.txt',
                task = 'parsing.tasks.robots_txt',
                kwargs = json.dumps({'url': self.url}),
                enabled = self.enabled,
            )
        else:
            task = self.task
            task.interval = self.schedule
            task.kwargs = json.dumps({'url': self.url})
            task.enabled = self.enabled
        task.save()
        return task

    def task_now(self) -> str:
        return celery_app.send_task(self.task.task, kwargs=json.loads(self.task.kwargs))

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.brand.name)
        super(Site, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['brand', 'url']]
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')
        ordering = ['-created', 'url']


class Sitemap(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name=_('Site'))
    url = models.URLField(db_index=True, verbose_name=_('url'))
    lastmod = models.DateField(blank=True, null=True, verbose_name=_('Last modefication'))
    schedule = models.ForeignKey(IntervalSchedule, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, blank=True, null=True)
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('parsing:sitemap-detail', args=[self.pk])

    def task_create_or_update(self):
        if self.task is None:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )
            task = PeriodicTask(
                interval = schedule,
                name = f'{self.site.brand.name}.{self.url}.sitemap',
                task = 'parsing.tasks.sitemap',
                kwargs = json.dumps({'url': self.url}),
                enabled = self.enabled,
            )
        else:
            task = self.task
            task.interval = self.schedule
            task.kwargs = json.dumps({'url': self.url})
            task.enabled = self.enabled
        task.save()
        return task

    def task_now(self) -> str:
        return celery_app.send_task(self.task.task, kwargs=json.loads(self.task.kwargs))

    class Meta:
        verbose_name = _('Sitemap url')
        verbose_name_plural = _('Sitemap urls')
        unique_together = (('site', 'url'), )
        ordering = ['-created', 'url']


class GoodURL(models.Model):
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE, verbose_name=_('Sitemap'))
    url = models.URLField(db_index=True, max_length=300, verbose_name=_('Site url'))
    lastmod = models.DateField(blank=True, null=True, verbose_name=_('Last modefication'))
    schedule = models.ForeignKey(IntervalSchedule, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, null=True)
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url

    def mapping(self) -> dict:
        return self.sitemap.site.goodmapping_set.get().mapping()

    @property
    def brand(self):
        return self.sitemap.site.brand
    
    def task_create_or_update(self):
        if self.task is None:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )
            task = PeriodicTask(
                interval = schedule,
                name = f'{self.brand.name}.good.{self.url}',
                task = 'parsing.tasks.good',
                kwargs = json.dumps({'url': self.url, 'mapping': self.mapping()}),
                enabled = self.enabled,
            )
        else:
            task.interval = self.schedule
            task.kwargs = json.dumps({'url': self.url, 'mapping': self.mapping()})
            task.enabled = self.enabled
            task.save()
        return task

    def task_now(self) -> str:
        return celery_app.send_task(self.task.task, kwargs=json.loads(self.task.kwargs))

    class Meta:
        verbose_name = _('Good URL')
        verbose_name_plural = _('Goods URL')
        unique_together = (('sitemap', 'url'), )
        ordering = ['-edited', 'url']


class GoodMapping(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    image = models.CharField(max_length=250, verbose_name=_('Image'))
    description = models.CharField(max_length=250, verbose_name=_('Desciption'))
    article = models.CharField(max_length=50, verbose_name=_('Article'))
    category = models.CharField(blank=True, max_length=250, verbose_name=_('Category'))
    price = models.CharField(blank=True, max_length=250, verbose_name=_('Price'))
    discount = models.CharField(blank=True, max_length=250, verbose_name=_('discount'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)

    def __str__(self) -> str:
        return f'{self.site} good selectors'

    def mapping(self) -> dict:
        return {
            'brand': self.brand,
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'article': self.article,
            'category': self.category,
            'price': self.price,
            'discount': self.discount,
        }

    @property
    def brand(self):
        return self.site.brand.name

    class Meta:
        verbose_name = _('Good mapping')
        verbose_name_plural = _('Good mappings')
