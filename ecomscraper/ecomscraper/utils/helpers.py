from urllib.parse import urljoin

def construct_absolute_url(base_url, relative_url):
    """
    Constructs an absolute URL from a base URL and a relative URL.
    """
    if relative_url:
        return urljoin(base_url, relative_url)
    return None

def log_pagination(logger, current_page, next_page_url):
    """
    Logs information about pagination.
    """
    logger.info(f"Processing page {current_page}, next page: {next_page_url}")