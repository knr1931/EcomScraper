import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/"]

    def parse(self, response, **kwargs):
        pass
