import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import IntervalSchedule

from parsing import models, tasks

logger = logging.getLogger(__name__)


@receiver(post_save, sender=models.Site)
def update_or_create_site_hook(sender, instance, using, **kwargs):
    logger.debug('Signal models.Site.save hook: %s', instance)
    #tasks.robots_txt.delay(instance.url)


@receiver(post_save, sender=models.Sitemap)
def update_or_create_sitemap_hook(sender, instance, using, **kwargs):
    logger.debug('Signal models.sitemap.save hook: %s', instance)
    #tasks.sitemap.delay(instance.url)


@receiver(post_save, sender=models.GoodURL)
def update_or_create_goodurl_hook(sender, instance, using, **kwargs):
    logger.debug('Signal model.GoodURL.save hook: %s', instance)
    #interval = IntervalSchedule.objects.get_or_create(
    #    every=1,
    #    period=IntervalSchedule.HOURS
    #)
    #PeriodicTask.objects.update_or_create(
    #    interval=interval, name=instance,
    #    task='parsing.tasks.good',
    #    args=f'["{instance.url}"]'
    #)


@receiver(post_delete, sender=models.GoodURL)
def delete_goodurl_hook(sender, instance, using, **kwargs):
    logger.debug('Signal model.GoodURL.delete hook: %s', instance)
    # try:
    #     task = PeriodicTask.objects.get(name=instance)
    #     task.delete()
    # except PeriodicTask.DoesNotExist:
    #     logger.debug('Entry for delition not foud: %s', instance)
