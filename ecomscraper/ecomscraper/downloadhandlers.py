from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler
import random


class EcomPlaywrightDownloadHandler(ScrapyPlaywrightDownloadHandler):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # Add more user agents here
    ]

    async def _create_page(self, request, spider):
        # Customize Playwright context kwargs
        context_kwargs = request.meta.get("playwright_context_kwargs", {})
        context_kwargs.setdefault("user_agent", random.choice(self.USER_AGENTS))

        # Customize Playwright page methods
        page_methods = request.meta.get("playwright_page_methods", [])
        page_methods.append({"method": "set_extra_http_headers", "args": [{
            "User-Agent": context_kwargs["user_agent"],
            "Accept-Language": "en-US,en;q=0.9",
        }]})

        # Update request.meta with the customized settings
        request.meta["playwright_context_kwargs"] = context_kwargs
        request.meta["playwright_page_methods"] = page_methods

        # Call the parent _create_page method
        return await super()._create_page(request, spider)
