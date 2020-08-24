import logging

from parsing.spiders import RobotstxtSpider, SitemapSpider, GoodSpiderChrome
from parsing.components.leafs import SitemapLeaf, GoodURLeaf, GoodLeaf
from coreapi.patterns.composites import Composite

logger = logging.getLogger(__name__)


class SiteComposite(Composite):
    def __init__(self, *args, **kwargs):
        super(SiteComposite, self).__init__(*args, **kwargs)
        self.URL = kwargs.get('url')
        if self.URL is None:
            raise KeyError('URL address is None')

    async def run(self):
        spider = RobotstxtSpider(self.URL)
        await spider.get_sitemap_list()
        for sitemap_data in spider.sitemap_list:
            self.add(SitemapLeaf(site=self.URL, **sitemap_data))
        return await super(SiteComposite, self).run()


class SitemapComposite(Composite):
    def __init__(self, *args, **kwargs):
        super(SitemapComposite, self).__init__(*args, **kwargs)
        self.URL = kwargs.get('url')
        if self.URL is None:
            raise KeyError('URL address is None')

    async def run(self):
        spider = SitemapSpider(self.URL)
        await spider.get_good_list()
        for good_data in spider.url_list:
            self.add(GoodURLeaf(sitemap=self.URL, **good_data))
        return await super(SitemapComposite, self).run()


class GoodComposite(Composite):
    def __init__(self, *args, **kwargs):
        super(GoodComposite, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.mapping = kwargs.get('mapping')
        
    async def run(self):
        spider = GoodSpiderChrome(self.url, self.mapping)
        result = await spider.get_result()
        self.add(GoodLeaf(url=self.url, **result))
        return await super(GoodComposite, self).run()
