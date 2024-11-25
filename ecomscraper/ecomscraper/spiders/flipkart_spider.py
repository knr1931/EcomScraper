import scrapy


class FlipkartSpiderSpider(scrapy.Spider):
    name = "flipkart_spider"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com/"]

    def parse(self, response, **kwargs):
        pass
