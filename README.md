# EcomScraper

EcomScraper is a powerful web scraping tool designed to extract detailed product information from e-commerce platforms like Amazon and Flipkart. This tool uses Scrapy for high-performance scraping and Playwright to handle dynamic, JavaScript-loaded pages.

## Project Overview

EcomScraper focuses on scraping products from popular e-commerce platforms in India (Amazon and Flipkart), retrieving essential data like product details, pricing, availability, and reviews. The scraper is designed to handle both static and dynamic content, ensuring robust performance even with complex web structures.

## Features

- **Scrapes product details** such as title, price, description, and images.
- **Extracts reviews**, ratings, and customer feedback.
- **Handles dynamic JavaScript-loaded content** using Playwright.
- **Supports pagination** for crawling multiple pages of products.
- Can be **extended to other e-commerce platforms** if required.

## Technologies Used

- **Scrapy**: A powerful web crawling and scraping framework to handle large-scale data extraction.
- **Playwright**: A browser automation tool for handling dynamic content and JavaScript-heavy pages.
- **Python**: The primary programming language for the project.
- **JSON/CSV**: Data export formats supported for easy storage and analysis.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EcomScraper.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ecomscraper
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Update the settings and configuration in the `settings.py` file.
2. Run the Scrapy spider for Amazon:
    ```bash
    scrapy crawl amazon_spider
    ```
3. Run the Scrapy spider for Flipkart:
    ```bash
    scrapy crawl flipkart_spider
    ```
4. Export the data to JSON or CSV:
    ```bash
    scrapy crawl amazon_spider -o amazon_data.json
    scrapy crawl flipkart_spider -o flipkart_data.csv
    ```

## Configuration

- **Proxies**: Configure proxies in `middlewares.py` to avoid IP bans.
- **User Agents**: Rotate user agents to mimic different browsers.
- **CAPTCHA Handling**: Integrate CAPTCHA-solving services like 2Captcha if necessary.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please contact [yourname@domain.com](mailto:yourname@domain.com).

---

Happy scraping!
