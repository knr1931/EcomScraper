from typing import Iterable

import random
import scrapy
from numpy.ma.core import absolute
from scrapy import Request

AMAZON_ALL_MOBILE_PHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"
AMAZON_SMARTPHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1805560031&s=popularity-rank&fs=true&ref=lp_1805560031_sar"


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url=AMAZON_SMARTPHONES_URL,
            callback=self.parse,
            meta={"playwright": True},
        )

    def parse(self, response, **kwargs):

        products = response.xpath('//div[@class="a-section a-spacing-base"]//h2/a')

        for product in products:
            product_link = product.xpath('.//@href').get()
            product_absolute_url = f'https://www.amazon.in{product_link}'
            yield {
                "product_url": product_absolute_url
            }

        next_page = response.xpath('//a[contains(@class, "s-pagination-next")]/@href').get()

        if next_page:
            next_page_link = f'https://www.amazon.in{next_page}'
            yield response.follow(
                url=next_page_link,
                callback=self.parse,
                meta={"playwright": True},
            )
