from typing import Iterable
import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod

from ecomscraper.utils.helpers import construct_absolute_url, convert_price_str_to_float

FLIPKART_BASE_URL = "https://www.flipkart.com/"
SUBCATEGORY_URLS = {
    'smartphones': "https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy,4io&otracker=categorytree",
    'laptops': "https://www.flipkart.com/computers/laptops/pr?sid=6bo,b5g&otracker=categorytree"
}


class FlipkartSpiderSpider(scrapy.Spider):
    name = "flipkart_spider"
    allowed_domains = ["www.flipkart.com"]

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

        for product in products[:5]:
            self.logger.info(f'Scraping product {product_num}....')
            print(f'Scraping product {product_num}....')

            product_link = product.xpath('.//@href').get()
            product_absolute_url = construct_absolute_url(FLIPKART_BASE_URL, product_link)
            self.logger.debug(f"Constructed URL: {product_absolute_url}")

            product_name = product.xpath('.//div[@class="KzDlHZ"]/text()').get()
            yield response.follow(
                url=product_absolute_url,
                callback=self.parse_product,
                meta={
                    "playwright": True,
                    # "playwright_page_methods": [
                    #     PageMethod("screenshot", path=f"product_{product_num}.png", full_page=True)
                    # ]
                },
                cb_kwargs={
                    "subcategory": subcategory,
                    "product_url": product_absolute_url,
                    "product_name": product_name
                },
            )
            product_num += 1

        # next_page = response.xpath('//a[contains(@class, "s-pagination-next")]/@href').get()
        # if next_page:
        #     absolute_next_page_url = construct_absolute_url(AMAZON_BASE_URL, next_page)
        #     self.logger.info(f"Following next page: {absolute_next_page_url}")
        #     yield response.follow(
        #         url=absolute_next_page_url,
        #         callback=self.parse,
        #         meta={"playwright": True},
        #         cb_kwargs={"subcategory": subcategory, "pagination_num": pagination_num + 1,
        #                    "product_num": product_num},
        #     )

    async def parse_product(self, response, **kwargs):
        subcategory = kwargs.get("subcategory", "unknown")
        product_absolute_url = kwargs.get("product_url", "unknown")

        product_name = kwargs.get("product_name")
        product_features_list = response.xpath('//div[@class="U+9u4y"]//li/text()').getall()
        product_features = ';'.join(product_features_list)

        # page = response.meta["playwright_page"]
        # await page.screenshot(path=f"example_{product_name}.png", full_page=True)
        # # screenshot contains the image's bytes
        # page.close()

        # # Getting brand name
        # extra_features_rows = response.xpath('//table[@class="a-normal a-spacing-micro"]/tbody/tr')
        #
        # brand_name = ""
        # for row in extra_features_rows:
        #     if str(row.xpath('./td[1]/text()').get()).strip().lower() == 'brand':
        #         brand_name = str(row.xpath('./td[2]/text()').get()).strip()

        price = response.xpath('//div[@class="hl05eU"]//div[@class="Nx9bqj CxhGGd"]/text()').get().strip()

        # print(price)
        price = convert_price_str_to_float(price)

        mrp = response.xpath('//div[@class="hl05eU"]//div[@class="yRaY8j A6+E6v"]/text()').get().strip()

        mrp = convert_price_str_to_float(mrp)

        discount = round((abs(price - mrp)  / mrp)*100, 2)

        rating_str = response.xpath('(//span[@class="Y1HWO0"])[1]').xpath('.//div/text()').get()
        rating = f'{rating_str.strip()}/5'

        num_of_ratings_str = response.xpath('//div[@class="_5OesEi HDvrBb"]/span[@class="Wphh3N"]').xpath('./span/span[1]/text()').get()
        num_of_ratings = int(convert_price_str_to_float(str(num_of_ratings_str).split(" ")[0]))

        yield {
            'category': subcategory,
            'product name': product_name,
            # 'brand': brand_name,
            'price': price,
            'mrp': mrp,
            'discount': discount,
            'rating': rating,
            'num of ratings': num_of_ratings,
            'product features': product_features,
            'product url': product_absolute_url

        }
