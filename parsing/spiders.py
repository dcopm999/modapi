
import logging
import re
import zlib
from typing import Dict
import aiohttp

from lxml import etree
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import WebDriverException, NoSuchElementException

logger = logging.getLogger(__name__)

ENCODING = 'utf-8'


class BaseSpider: # pylint: disable=too-few-public-methods
    def __init__(self, headers=None) -> None:
        logger.debug('BaseSpider.__init__(headers)')
        if headers is None:
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'}
        else:
            self.headers = headers
        logger.debug('self.headers = %s', self.headers)

    @staticmethod
    def _gen_dict(items) -> Dict[str, str]:
        # TODO: rewrite this, without if in interaction
        result = {}
        for item in items:
            if item.tag.find('loc') > 0:
                result['url'] = item.text
            elif item.tag.find('lastmod') > 0:
                result['lastmod'] = item.text
        return result

    async def _get_file(self, url: str) -> str:
        logger.info('Download file: %s', url)
        # TODO: use share session
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, verify_ssl=False) as response:
                logger.debug('request info %s', response.request_info)
                if  response.status == 200:
                    suff = url.split('.')[-1]
                    if  suff in ['xml', 'txt']:
                        logger.debug('Download file with text format: %s', url)
                        result = await response.text()
                    else:
                        logger.debug('Download file with byte format: %s', url)
                        file_body = await response.read()
                        if suff == 'gz':
                            logger.debug('decompress gzip file: %s', url)
                            result = zlib.decompress(file_body, zlib.MAX_WBITS | 16).decode(ENCODING)
                        elif suff == 'z':
                            logger.debug('decompress glib file: %s', url)
                            result = zlib.decompress(file_body, zlib.MAX_WBITS).decode(ENCODING)
                        elif suff == 'def':
                            logger.debug('decompress deflat file: %s', url)
                            result = zlib.decompress(file_body, -zlib.MAX_WBITS).decode(ENCODING)
                    logger.debug(url)
                else:
                    logger.debug(response.status)
                    result = ''
                return result


class RobotstxtSpider(BaseSpider): # pylint: disable=too-few-public-methods
    # TODO: implement the method __aiter__
    '''
    Spider class for parsing robots.txt and search for sitemap files

    params:
            url: str

    example:
        import asyncio
        logging.basicConfig(level='DEBUG')
        sitemap_spider = RobotstxtSpider('https://shop.mango.com')
        asyncio.run(sitemap_spider.get_sitemap_list())
        print(sitemap_spider.sitemap_list)
    '''
    def __init__(self, url: str, headers=None) -> None:
        if url[-1] != '/':
            url += '/'
        self.url = url
        self.sitemap_list = []
        super(RobotstxtSpider, self).__init__(headers)

    async def _sitemap_from_robotstxt(self, robots_body: str) -> list:
        logger.info('Parse robots.txt and find sitemap')
        finder = re.compile(r'[sS]itemap:\s+.+')
        sitemap_row = finder.findall(robots_body)[0]
        logger.info('Find result %s', sitemap_row)
        return re.findall(r'http?s://.+', sitemap_row)[-1].split('\\n')[0]

    async def _find_sitemap_nested(self, url: str) -> None:
        logger.debug('find nested sitemap from: %s', url)
        parent = re.split(r'<?xml version="1.0" encoding="UTF-8"?>\r', await self._get_file(url))
        parent_xml = etree.fromstringlist(parent)
        if re.search('sitemapindex', parent_xml.tag) is not None:
            for sitemaps in parent_xml.iterchildren():
                self.sitemap_list.append(self._gen_dict(sitemaps.iterchildren()))

    async def get_sitemap_list(self) -> None:
        robotstxt_url = self.url + 'robots.txt'
        robotstxt_body = await self._get_file(robotstxt_url)
        sitemap_parent_url = await self._sitemap_from_robotstxt(robotstxt_body)
        self.sitemap_list.append({'url': sitemap_parent_url})
        await self._find_sitemap_nested(sitemap_parent_url)


class SitemapSpider(BaseSpider): # pylint: disable=too-few-public-methods
    def __init__(self, url: str, headers=None) -> None:
        self.url = url
        self.url_list = []
        super(SitemapSpider, self).__init__(headers)

    async def get_good_list(self) -> None:
        sitemap_body = re.split(
            r'\<\?xml version="1\.0" encoding="UTF\-8"\?\>[\n, \r]',
            await self._get_file(self.url)
        )
        sitemap_xml = etree.fromstringlist(sitemap_body)
        self.url_list = [self._gen_dict(items) for items in sitemap_xml.iterchildren()]


class BaseGoodSpider(BaseSpider):
    def __init__(self, url: str, mapping: dict, headers=None):
        super(BaseGoodSpider, self).__init__(headers)
        logger.info('Selenium: parsing %s', url)
        logger.debug("BaseGoodSpider.__init__(url, mapping, headers)")

        self.mapping = mapping
        logger.debug('self.mapping = %s', self.mapping)

        self.driver.headers = self.headers
        self.url = url
        self._get()

    def _get(self) -> None:
        logger.debug('Selenium: Get %s', self.url)
        self.driver.get(self.url)

    async def get_brand(self) -> str:
        logger.debug('Selenium: Get brand : %s', self.mapping['brand'])
        result = None
        try:
            result = self.mapping['brand']
        except NoSuchElementException:
            logger.exception('Selenium: brand not found')
        finally:
            return result

    async def get_name(self) -> str:
        logger.debug('Selenium: Get name xpath: %s', self.mapping['name'])
        result = None
        try:
            result = self.driver.find_element(By.XPATH, self.mapping['name']).text
        except NoSuchElementException:
            logger.exception('Selenium: name not found')
        finally:
            logger.debug('Selenium: name result=%s', result)
            return result

    async def get_description(self) -> str:
        logger.debug('Selenium: Get description xpath: %s', self.mapping['description'])
        result = None
        try:
            result = self.driver.find_element(By.XPATH, self.mapping['description']).text
        except NoSuchElementException:
            logger.exception('Selenium: description not found')
        finally:
            logger.debug('Selenium: description result=%s', result)
            return result

    async def get_article(self) -> str:
        logger.debug('Selenium: Get article xpath: %s', self.mapping['article'])
        result = None
        try:
            result = self.driver.find_element(By.XPATH, self.mapping['article']).text
        except NoSuchElementException:
            logger.exception('Selenium: article not found')
        finally:
            logger.debug('Selenium: article result=%s', result)
            return result

    async def get_image(self) -> list:
        logger.debug('Selenium: Get image xpath: %s', self.mapping['image'])
        result = None
        try:
            image_list = self.driver.find_elements(By.XPATH, self.mapping['image'])
            result = [image.get_attribute("src") for image in image_list]
        except NoSuchElementException:
            logger.exception('Selenium: image not found')
        finally:
            logger.debug('Selenium: image result=%s', result)
            return result

    async def get_category(self) -> str:
        logger.debug('Selenium: Get category xpath: %s', self.mapping['category'])
        result = None
        try:
            result = self.driver.find_element(By.XPATH, self.mapping['category']).text
        except NoSuchElementException:
            logger.exception('Selenium: category not found')
        finally:
            logger.debug('Selenium: category result=%s', result)
            return result

    async def get_price(self):
        mapping = self.mapping['price']
        logger.debug('Selenium: Get price xpath: %s', mapping)
        try:
            response = self.driver.find_element(By.XPATH, mapping).text
            logger.debug('Selenium: price result=%s', response)
        except NoSuchElementException:
            logger.exception('Selenium: price not found')
            response = None
            logger.debug('Selenium: price result=%s', response)
        finally:
            if isinstance(response, str):
                result = ''
                for item in response:
                    if item.isnumeric():
                        result += item
                result = int(result)
            logger.debug('Selenium: price result=%s', result)
            return result

    async def get_discount(self):
        mapping = self.mapping['discount']
        logger.debug('Selenium: Get discount xpath: %s', mapping)
        try:
            response = self.driver.find_element(By.XPATH, mapping).text
        except NoSuchElementException:
            logger.exception('Selenium: discount not found')
            response = None
        finally:
            if isinstance(response, str):
                result = ''
                for item in response:
                    if item.isnumeric():
                        result += item
                result = int(result)
            elif response is None:
                result = 0
        logger.debug('Selenium: discount result=%s', result)
        return result

    async def get_result(self) -> dict:
        logger.debug('Selenium: getting the result')
        return {
            'brand': await self.get_brand(),
            'name': await self.get_name(),
            'description': await self.get_description(),
            'article': await self.get_article(),
            'category': await self.get_category(),
            'price': await self.get_price(),
            'discount': await self.get_discount(),
            'image': await self.get_image(),
        }


class GoodSpiderFirefox(BaseGoodSpider):
    def __init__(self, url: str, mapping: dict, headers=None):
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        logger.debug('options: %s', options)
        options.add_argument("--headless")  
        logger.debug('added options argument --headers')
        
        capabilities = DesiredCapabilities.FIREFOX
        logger.debug('capabilities: %s', capabilities)
        capabilities['-marionette'] = True
        logger.debug('added capabilities argument --marionette: True')
        logger.debug('Selenium: inititalize')
        try:
            self.driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options, capabilities=capabilities)
        except WebDriverException as msg:
            logger.exception('Selenium: Exception %s', msg)
            raise WebDriverException('Selenium: Initialization error')
        else:
            logger.debug('Selenium: inititalized')
        super(GoodSpiderFirefox, self).__init__(url, mapping, headers=None)


class GoodSpiderChrome(BaseGoodSpider):
    def __init__(self, url: str, mapping: dict, headers=None):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--window-size=1920,1080")
        try:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        except WebDriverException as msg:
            logger.exception('Selenium: Exception %s', msg)
            raise WebDriverException('Selenium: Initialization error')
        else:
            logger.info('Selenium: inititalized')
        super(GoodSpiderChrome, self).__init__(url, mapping, headers=None)
