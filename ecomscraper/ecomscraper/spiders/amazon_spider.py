from typing import Iterable

import random
import scrapy
from scrapy import Request

AMAZON_MOBILE_PHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url=AMAZON_MOBILE_PHONES_URL,
            callback=self.parse,
            meta={"playwright": True},
        )

    def parse(self, response, **kwargs):
        yield {"url": response.url}
