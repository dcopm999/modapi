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
    try:
        loop.run_until_complete(sitemap.run())
    except WebDriverException:
        self.retry()


@app.task(bind=True)
def robots_txt(self, url):
    site = SiteComposite(url=url)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(site.run())
    except WebDriverException:
        self.retry()


@app.task(bind=True) # default_retry_delay=10)
def good(self, url: str, mapping: dict):
    obj = GoodComposite(url=url, mapping=mapping)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(obj.run())
    except WebDriverException:
        self.retry()
