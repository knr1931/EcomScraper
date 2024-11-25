from typing import Iterable

import random
import scrapy
from scrapy import Request

AMAZON_MOBILE_PHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
]


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url=AMAZON_MOBILE_PHONES_URL,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_context_kwargs": {
                    "user_agent": random.choice(USER_AGENTS),
                },
                "playwright_page_methods": [
                    {"method": "set_extra_http_headers", "args": [{
                        "User-Agent": random.choice(USER_AGENTS),
                        "Accept-Language": "en-US,en;q=0.9",
                    }]},
                    {"method": "wait_for_load_state", "args": ["networkidle"]},
                ],
            },

        )

    def parse(self, response, **kwargs):
        yield {"url": response.url}
