# Scrapy settings for ecomscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "ecomscraper"

SPIDER_MODULES = ["ecomscraper.spiders"]
NEWSPIDER_MODULE = "ecomscraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ecomscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "ecomscraper.middlewares.EcomscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "ecomscraper.middlewares.EcomscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "ecomscraper.pipelines.EcomscraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

HTTPCACHE_ENABLED = True  # Enable HTTP caching in `scrapy-playwright`
HTTPCACHE_EXPIRATION_SECS = 300 # 3600  # Cached responses expire after 1 hour (3600 seconds)
HTTPCACHE_DIR = "playwright_cache"  # Store cache in the "playwright_cache" directory
HTTPCACHE_IGNORE_HTTP_CODES = [404, 500]  # Do not cache responses with status codes 404 (Not Found) or 500 (Server Error)
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"  # Use the filesystem for caching

# Additional settings for `scrapy-playwright`
PLAYWRIGHT_ENABLED = True  # Enable Playwright to use browser context and perform rendering tasks in Scrapy
PLAYWRIGHT_BROWSER_TYPE = 'chromium'  # Choose the browser type (e.g., 'chromium', 'firefox', 'webkit')
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # Set default navigation timeout (milliseconds) for page loading
PLAYWRIGHT_HEADLESS = True  # Run browser in headless mode to speed up crawling (set to `False` for visual debugging)

# If using Playwright with caching, ensure that the cache used matches the browser context's storage state
# By default, caching in Scrapy will use filesystem storage; if needed, you can customize storage (e.g., `RedisCacheStorage`).


# Set settings whose default value is deprecated to a future-proof value
DOWNLOAD_HANDLERS = {
    'http': 'ecomscraper.downloadhandlers.EcomPlaywrightDownloadHandler',
    'https': 'ecomscraper.downloadhandlers.EcomPlaywrightDownloadHandler',
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_FORMAT = "%(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "scrapy_log.txt"  # Save logs to a file
LOG_LEVEL = "INFO"           # Set the logging level
