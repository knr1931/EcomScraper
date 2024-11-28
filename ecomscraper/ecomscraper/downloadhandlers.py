from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler
import random
from scrapy_playwright.page import PageMethod


class EcomPlaywrightDownloadHandler(ScrapyPlaywrightDownloadHandler):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Windows NT 6.0; rv:10.0) Gecko/20100101 Firefox/10.0",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko",

    ]

    async def _create_page(self, request, spider):
        # Customize Playwright context kwargs

        user_agent = random.choice(self.USER_AGENTS)
        context_kwargs = request.meta.get("playwright_context_kwargs", {})
        context_kwargs.setdefault("user_agent", user_agent)

        request.meta["playwright_page_methods"] = [
            PageMethod("set_extra_http_headers", {
                "User-Agent": user_agent,
                "Accept-Language": "en-US,en;q=0.9"
            }),
        ]

        # Update request.meta with the customized settings
        request.meta["playwright_context_kwargs"] = context_kwargs

        # Call the parent _create_page method
        return await super()._create_page(request, spider)
