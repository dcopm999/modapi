import logging

from django.utils import timezone

from goods import models
from parsing.models import (Site, Sitemap, GoodURL)
from coreapi.patterns.composites import Leaf

logger = logging.getLogger(__name__)


class SitemapLeaf(Leaf):

    def __init__(self, *args, **kwargs):
        super(SitemapLeaf, self).__init__(*args, **kwargs)
        self.site = kwargs.get('site')
        self.url = kwargs.get('url')
        self.lastmod = kwargs.get('lastmod')

    async def run(self):
        item = Sitemap.objects.filter(site__url=self.site, url=self.url)
        if item.exists():
            result = item.update(lastmod=self.lastmod)
        else:
            site = Site.objects.get(url=self.site)
            result = Sitemap.objects.create(site=site, url=self.url, lastmod=self.lastmod)
        return result


class GoodURLeaf(Leaf):
    def __init__(self, *args, **kwargs):
        super(GoodURLeaf, self).__init__(*args, **kwargs)
        self.sitemap = kwargs.get('sitemap')
        self.url = kwargs.get('url')
        self.lastmod = kwargs.get('lastmod', timezone.now())

    async def run(self):
        item = GoodURL.objects.filter(sitemap__url=self.sitemap, url=self.url)
        if item.exists():
            result = item.update(lastmod=self.lastmod)
        else:
            sitemap = Sitemap.objects.get(url=self.sitemap)
            result = GoodURL.objects.create(sitemap=sitemap, url=self.url, lastmod=self.lastmod)
        return result


class GoodLeaf(Leaf):
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('utl')
        self.mapping = kwargs.get('mapping')
        category, created = models.Category.objects.get_or_create(name=kwargs.get('category'))
        self.data = {
            'brand': models.Brand.objects.get(name=kwargs.get('brand')),
            'name': kwargs.get('name'),
            'description': kwargs.get('description'),
            'article': kwargs.get('article'),
            'category': category,
            'price': kwargs.get('price'),
            'discount': kwargs.get('discount'),
        }
        logger.debug('GoodLeaf: self.data=%s', self.data)

    async def run(self):
        models.Good.objects.update_or_create(**self.data)
