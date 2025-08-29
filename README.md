# Simple Web Scraper

This is a versatile Python script for scraping data from websites. It fetches HTML content from a given URL, extracts specific data based on user-defined CSS selectors, and saves the results to a file in either JSON or CSV format.

## Features

-   **HTTP Requests**: Fetches HTML content with built-in error handling and a request timeout.
-   **Data Extraction**: Uses Beautiful Soup 4 to parse HTML and extract data based on CSS selectors.
-   **Flexible Selectors**: Supports both simple selectors for text and dictionary-based selectors for extracting attributes (e.g., `href` from a link).
-   **Structured Output**: Can save the scraped data into a list of dictionaries, which can then be exported as a JSON or CSV file.
-   **Command-Line Interface**: Easily run the script from the command line with optional arguments for the URL, output filename, and format.

## Requirements

Before you can run the script, you need to install the necessary Python libraries.

-   `requests`: To send HTTP requests and get the HTML content.
-   `beautifulsoup4`: To parse the HTML and navigate the document tree.

You can install these dependencies using `pip`:

```bash
pip3 install requests beautifulsoup4
