from typing import Iterable
import scrapy
from pygments.lexer import default
from scrapy import Request

from ecomscraper.utils.helpers import construct_absolute_url, convert_str_to_float, convert_str_to_int

FLIPKART_BASE_URL = "https://www.flipkart.com/"
SUBCATEGORY_URLS = {
    'smartphones': "https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy,4io&otracker=categorytree",
    'laptops': "https://www.flipkart.com/computers/laptops/pr?sid=6bo,b5g&otracker=categorytree"
}


class FlipkartSpiderSpider(scrapy.Spider):
    name = "flipkart_spider"
    allowed_domains = ["www.flipkart.com", "https://proxy.scrapeops.io/"]

    def start_requests(self) -> Iterable[Request]:
        self.logger.info("Starting the Flipkart spider...")
        print("Starting the Flipkart spider...")  # Log an informational message
        subcategories = getattr(self, "subcategories", "all").split(',')

        if not subcategories or "all" in subcategories:
            subcategories = SUBCATEGORY_URLS.keys()

        for subcategory in subcategories:
            self.logger.info(f"Scraping subcategory: {subcategory}")
            print(f"Scraping subcategory: {subcategory}")
            subcategory_url = SUBCATEGORY_URLS.get(subcategory.strip())
            if subcategory_url:
                yield scrapy.Request(
                    url=subcategory_url,
                    callback=self.parse,
                    meta={"playwright": True},
                    cb_kwargs={"subcategory": subcategory}
                )

    async def parse(self, response, **kwargs):
        subcategory = kwargs.get("subcategory", "unknown")
        pagination_num = kwargs.get("pagination_num", 1)
        product_num = kwargs.get("product_num", 1)

        self.logger.info(f'Scraping {subcategory} on page {pagination_num}')
        print(f'Scraping {subcategory} on page {pagination_num}')

        products = response.xpath('//div[@class="_75nlfW"]//a[@class="CGtC98"]')

        for product in products:
            self.logger.info(f'Scraping product {product_num}....')
            print(f'Scraping product {product_num}....')

            # Scraping fields like product name, price, link etc.........
            product_link = product.xpath('.//@href').get()
            product_absolute_url = construct_absolute_url(FLIPKART_BASE_URL, product_link)
            self.logger.debug(f"Constructed URL: {product_absolute_url}")

            product_name = product.xpath('.//div[@class="KzDlHZ"]/text()').get(default="").strip()

            price_str = product.xpath('.//div[@class="Nx9bqj _4b5DiR"]/text()').get(default="").strip()
            mrp_str = product.xpath('.//div[@class="yRaY8j ZYYwLA"]/text()').get(default="").strip()

            price = convert_str_to_float(price_str)
            mrp = convert_str_to_float(mrp_str)
            discount = round((abs(price - mrp) / mrp) * 100, 2) if mrp !=0 else 0

            rating_str = product.xpath('.//div[@class="XQDdHH"]/text()').get(default="").strip()
            rating = f'{rating_str.strip()}/5'

            num_of_ratings_str = product.xpath('.//span[@class="Wphh3N"]/span/span[1]/text()').get(default="").strip()
            num_of_ratings = convert_str_to_int(num_of_ratings_str.split(" ")[0])

            product_features_list = response.xpath('.//ul[@class="G4BRas"]//li/text()').getall()
            product_features = ';'.join(product_features_list)

            product_image_url = product.xpath('.//div[@class="_4WELSP"]/img/@src').get()

            yield {
                "subcategory": subcategory,
                "product_url": product_absolute_url,
                "product_name": product_name,
                'price': price,
                'mrp': mrp,
                'discount': discount,
                'rating': rating,
                'num of ratings': num_of_ratings,
                'product features': product_features,
                'product url': product_absolute_url,
                'product image_url': product_image_url
            }

            product_num += 1

        next_page = response.xpath('//a[@class="_9QVEpD" and span[text()="Next"]]/@href').get()

        if next_page:
            absolute_next_page_url = construct_absolute_url(FLIPKART_BASE_URL, next_page)
            self.logger.info(f"Following next page: {absolute_next_page_url}")
            yield response.follow(
                url=absolute_next_page_url,
                callback=self.parse,
                meta={"playwright": True},
                cb_kwargs={"subcategory": subcategory, "pagination_num": pagination_num + 1,
                           "product_num": product_num},
            )
