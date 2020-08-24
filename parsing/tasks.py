import logging
import asyncio
from aiohttp.client_exceptions import ClientConnectorError
from selenium.common.exceptions import WebDriverException
from config.celery_app import app

from parsing.components.composites import SiteComposite, SitemapComposite, GoodComposite

logger = logging.getLogger(__name__)


@app.task(bind=True)
def sitemap(self, url):
    sitemap = SitemapComposite(url=url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sitemap.run())
    # sitemap = models.Sitemap.objects.get(url=url)
    # logger.info('Start parsing sitemap file: %s', sitemap)
    # spider = spiders.SitemapSpider(sitemap.url)
    # try:
    #     asyncio.run(spider.get_good_list())
    # except ClientConnectorError:
    #     self.retry()
    # else:
    #     logger.info('Write good  list to database')
    #     managers.manager_sitemap(sitemap.id, spider.url_list)
    #     del sitemap
    #     del spider


@app.task(bind=True)
def robots_txt(self, url):
    site = SiteComposite(url=url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(site.run())
    # site = models.Site.objects.get(id=data)
    # logger.info('Start parsing robots.txt for: %s', site)
    # spider = spiders.RobotstxtSpider(site.url)
    # try:
    #     asyncio.run(spider.get_sitemap_list())
    # except ClientConnectorError:
    #     self.retry()
    # except models.Site.DoesNotExist:
    #     logger.info('Record does not exist %s', data)
    #     self.retry()
    # else:
    #     logger.info('Write sitemap list to database')
    #     managers.manager_robots(data, spider.sitemap_list)
    #     del site
    #     del spider


@app.task(bind=True, default_retry_delay=10)
def good(self, url: str, mapping: dict):
    obj = GoodComposite(url=url, mapping=mapping)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(obj.run())

    """
    try:
        loop.run_until_complete(obj.run())
    except WebDriverException:
        self.retry()
    """
