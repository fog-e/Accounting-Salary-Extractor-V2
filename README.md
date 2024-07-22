# 📊 **Accounting Salary Extractor** 📈

## **Project Overview**
Scraping, processing, and analyzing salary data from various accounting-related subreddits.

## **Features** ✨
- **Data Gathering**: Scrapes posts and replies from a list of subreddits including r/accounting, r/FinancialCareers, r/Salary, and more.
- **Text Processing**: Utilizes regular expressions and NLP to identify and extract salary mentions.
- **Salary Conversion**: Converts hourly, weekly, monthly, and bi-weekly wages to annual salaries.
- **Currency Conversion**: Converts mentioned salaries to USD using reliable exchange rates.
- **OpenAI Integration**: Uses OpenAI to retrieve any missing information and calculate estimates for vague salary entries as needed.
- **Data Storage**: Organizes and stores the processed data in a CSV file for easy analysis.

## **Usage Advice** 🛠️
### Obtain Refresh Token:
```sh
python obtain_refresh_token.py

