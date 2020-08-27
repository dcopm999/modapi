import logging

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from parsing import models

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=models.Site)
def site_update_or_create(sender, instance, using, **kwargs):
    logger.debug('Signal models.Site pre_save: %s', instance)
    instance.task = instance.task_create_or_update()
    instance.schedule=instance.task.interval


@receiver(pre_delete, sender=models.Site)
def site_delete(sender, instance, using, **kwargs):
    logger.debug('Signal models.Site pre_delete: %s', instance)
    if instance.task:
        instance.task.delete()


@receiver(pre_save, sender=models.Sitemap)
def sitemap_update_or_create(sender, instance, using, **kwargs):
    logger.debug('Signal models.sitemap pre_save: %s', instance)
    instance.task = instance.task_create_or_update()
    instance.schedule=instance.task.interval


@receiver(pre_delete, sender=models.Sitemap)
def sitemap_delete(sender, instance, using, **kwargs):
    logger.debug('Signal models.Sitemap pre_delete: %s', instance)
    if instance.task:
        instance.task.delete()


@receiver(pre_save, sender=models.GoodURL)
def goodurl_update_or_create(sender, instance, using, **kwargs):
    logger.debug('Signal model.GoodURL pre_save: %s', instance)
    instance.task = instance.task_create_or_update()
    instance.schedule=instance.task.interval


@receiver(pre_delete, sender=models.GoodURL)
def goodurl_delete(sender, instance, using, **kwargs):
    logger.debug('Signal model.GoodURL pre_delete: %s', instance)
    if instance.task:
        instance.task.delete()
