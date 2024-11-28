from typing import Iterable

import scrapy
from scrapy import Request
from ecomscraper.utils.helpers import construct_absolute_url, convert_str_to_float

AMAZON_BASE_URL = "https://www.amazon.in"
AMAZON_ALL_MOBILE_PHONES_URL = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"
SUBCATEGORY_URLS = {
    'smartphones': "https://www.amazon.in/s?i=electronics&rh=n%3A1805560031&s=popularity-rank&fs=true&ref=lp_1805560031_sar",
    'laptops': "https://www.amazon.in/s?i=computers&rh=n%3A22963796031&s=popularity-rank&fs=true&ref=lp_22963796031_sar"
}


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]

    def start_requests(self) -> Iterable[Request]:
        self.logger.info("Starting the Amazon spider...")
        print("Starting the Amazon spider...")  # Log an informational message
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

        self.logger.info("Finished the Amazon spider...")
        print("Finished Scraping Amazon site...")

    def parse(self, response, **kwargs):
        subcategory = kwargs.get("subcategory", "unknown")
        pagination_num = kwargs.get("pagination_num", 1)
        product_num = kwargs.get("product_num", 1)

        self.logger.info(f'Scraping {subcategory} on page {pagination_num}')
        print(f'Scraping {subcategory} on page {pagination_num}')

        products = response.xpath('//div[@class="a-section a-spacing-base"]//h2/a')

        for product in products:
            self.logger.info(f'Scraping product {product_num}....')
            print(f'Scraping product {product_num}....')

            product_link = product.xpath('.//@href').get()
            product_absolute_url = construct_absolute_url(AMAZON_BASE_URL, product_link)
            self.logger.debug(f"Constructed URL: {product_absolute_url}")
            yield response.follow(
                url=product_absolute_url,
                callback=self.parse_product,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,

                },
                cb_kwargs={"subcategory": subcategory, "product_url": product_absolute_url},
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

        name_features_text = str(response.xpath('//span[@id="productTitle"]/text()').get()).strip()

        # Splitting product name and product features from name_features_text
        name_features_list = name_features_text.split("|")
        product_name = name_features_list[0]
        product_features = ','.join(name_features_list[1:])

        page = response.meta["playwright_page"]
        await page.screenshot(path=f"example_{product_name}.png", full_page=True)
        # screenshot contains the image's bytes
        page.close()

        # Getting brand name
        extra_features_rows = response.xpath('//table[@class="a-normal a-spacing-micro"]/tbody/tr')

        brand_name = ""
        for row in extra_features_rows:
            if str(row.xpath('./td[1]/text()').get()).strip().lower() == 'brand':
                brand_name = str(row.xpath('./td[2]/text()').get()).strip()

        price = str(response.xpath(
            '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"]/text()').get()).strip()

        print(price)
        price = convert_str_to_float(price)


        mrp = str(response.xpath(
            '//div[@class="a-section a-spacing-small aok-align-center"]//span[@class="a-offscreen"]/text()').get()).strip()

        mrp = convert_str_to_float(mrp)

        discount = round((price - mrp) / mrp, 2)

        rating = f'{str(response.xpath('(//span[@id="acrPopover"])[1]//span[@class="a-size-base a-color-base"]/text()').get()).strip()}/5'

        num_of_reviews = int(convert_str_to_float(str(response.xpath(
            '(//div[@id="averageCustomerReviews"])[1]//span[@id="acrCustomerReviewText"]/text()').get()).strip().split(
            " ")[0]))

        yield {
            'category': subcategory,
            'product name': product_name,
            'brand': brand_name,
            'price': price,
            'mrp': mrp,
            'discount': discount,
            'rating': rating,
            'num of reviews': num_of_reviews,
            'product features': product_features,
            'product url': product_absolute_url

        }
