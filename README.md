# Accounting Salary Extractor

## Project Overview

Welcome to the **Accounting Salary Extractor** – your one-stop-shop for scraping, processing, and analyzing salary data from the r/accounting subreddit. Perfect for when you have too much free time and not enough self-control. Future goal: use this data to manipulate the CPA salary market like RealPage did for rentals (but maybe let's not get ahead of ourselves just yet).

## Features

1. **Data Gathering**: Scrapes posts and replies from the r/accounting subreddit.
2. **Text Processing**: Uses regular expressions and NLP to find mentions of salaries.
3. **Salary Conversion**: Converts hourly, weekly, monthly, and bi-weekly wages to annual salaries.
4. **Currency Conversion**: Converts mentioned salaries to USD.
5. **Data Storage**: Stores the processed data in a CSV file.

## Usage

1. **Obtain Refresh Token**:
    ```bash
    python obtain_refresh_token.py
    ```

2. **Verify Reddit Authentication**:
    ```bash
    python verify_reddit.py
    ```

3. **Extract Salary Data**:
    ```bash
    python extract_salaries.py
    ```

## Contributing

Feel free to lol

## License

This project is licensed under the MIT License because we believe in sharing... just not everything.

---

Future plans include upgrading this project to manipulate the CPA salary market. But let's keep that between us for now.
