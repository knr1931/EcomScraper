from typing import Iterable

import scrapy
from scrapy import Request
from ecomscraper.ecomscraper.utils.helpers import construct_absolute_url

AMAZON_BASE_URL = "https://www.amazon.in"
AMAZON_ALL_MOBILE_PHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"
SUBCATEGORY_URLS = {
    'smartphones': "https://www.amazon.in/s?i=electronics&rh=n%3A1805560031&s=popularity-rank&fs=true&ref=lp_1805560031_sar",
    'laptops': "https://www.amazon.in/s?i=computers&rh=n%3A1375424031&s=popularity-rank&fs=true&ref=lp_1375424031_sar"
}


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]


    def start_requests(self) -> Iterable[Request]:
        self.logger.info("Starting the spider...")  # Log an informational message
        subcategories = getattr(self, "subcategories", "all").split(',')

        if not subcategories or "all" in subcategories:
            subcategories = SUBCATEGORY_URLS.keys()

        for subcategory in subcategories:
            subcategory_url = SUBCATEGORY_URLS.get(subcategory.strip())
            if subcategory_url:
                yield scrapy.Request(
                    url=subcategory_url,
                    callback=self.parse,
                    meta={"playwright": True},
                    cb_kwargs={"subcategory": subcategory}
                )

    def parse(self, response, **kwargs):
        subcategory = kwargs.get("subcategory", "unknown")
        self.logger.info(f"Scraping subcategory: {subcategory}")

        products = response.xpath('//div[@class="a-section a-spacing-base"]//h2/a')

        for product in products:
            product_link = product.xpath('.//@href').get()
            product_absolute_url = construct_absolute_url(AMAZON_BASE_URL, product_link)
            self.logger.debug(f"Constructed URL: {product_absolute_url}")
            yield {
                "subcategory": subcategory,
                "product_url": product_absolute_url
            }

        self.follow_pagination(response, subcategory)

    def follow_pagination(self, response, subcategory: str):
        next_page = response.xpath('//a[contains(@class, "s-pagination-next")]/@href').get()
        if next_page:
            absolute_next_page_url = construct_absolute_url(AMAZON_BASE_URL, next_page)
            self.logger.info(f"Following next page: {absolute_next_page_url}")
            yield response.follow(
                url=absolute_next_page_url,
                callback=self.parse,
                meta={"playwright": True},
                cb_kwargs={"subcategory": subcategory},
            )
