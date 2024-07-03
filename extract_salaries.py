import os
from dotenv import load_dotenv
import praw
import re
import csv
from forex_python.converter import CurrencyRates

# Load environment variables from .env file
load_dotenv()

# Retrieve the values from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

# Initialize Reddit API with your credentials
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    refresh_token=REFRESH_TOKEN
)

# Initialize Currency Converter
currency_rates = CurrencyRates()

def convert_to_annual_salary(salary, period, currency='USD'):
    annual_salary = 0
    if period == 'hourly':
        annual_salary = salary * 40 * 52
    elif period == 'weekly':
        annual_salary = salary * 52
    elif period == 'monthly':
        annual_salary = salary * 12
    elif period == 'bi-weekly':
        annual_salary = salary * 26
    else:
        annual_salary = salary

    if currency != 'USD':
        annual_salary = currency_rates.convert(currency, 'USD', annual_salary)

    return annual_salary

def extract_salary_details(text):
    patterns = {
        'hourly': r'\$([0-9]+(\.[0-9]+)?)\s*\/\s*hour',
        'weekly': r'\$([0-9]+(\.[0-9]+)?)\s*\/\s*week',
        'monthly': r'\$([0-9]+(\.[0-9]+)?)\s*\/\s*month',
        'bi-weekly': r'\$([0-9]+(\.[0-9]+)?)\s*\/\s*bi-week'
    }
    for period, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            salary = float(match.group(1))
            return convert_to_annual_salary(salary, period)
    return None

def scrape_subreddit(subreddit_name, limit=100):
    salary_data = []
    subreddit = reddit.subreddit(subreddit_name)
    for comment in subreddit.comments(limit=limit):
        comment_text = comment.body
        salary = extract_salary_details(comment_text)
        if salary:
            salary_data.append({
                'Salary (USD)': salary,
                'Location': 'N/A',  # Placeholder, to be extracted
                'Experience (Years)': 'N/A',  # Placeholder, to be extracted
                'Job Title': 'N/A',  # Placeholder, to be extracted
                'Date': comment.created_utc,
                'Salary Source': 'Explicit',
                'Additional Information': comment.link_permalink
            })
    return salary_data

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Main script
salary_data = scrape_subreddit('accounting', limit=100)
save_to_csv(salary_data, 'salary_data.csv')
