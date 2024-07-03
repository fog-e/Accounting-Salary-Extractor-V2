import os
from dotenv import load_dotenv
import praw
import re
import csv
from datetime import datetime
from forex_python.converter import CurrencyRates

# Load environment variables from .env file
load_dotenv()

# Retrieve the values from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')

# Initialize Currency Converter
currency_rates = CurrencyRates()

# Initialize Reddit API with your credentials
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

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
    
    return round(annual_salary, 2)

def extract_salary_details(text):
    salary_patterns = [
        (r'\$?(\d+[\.,]?\d*)\s*(?:per\s*hour|hourly)', 'hourly'),
        (r'\$?(\d+[\.,]?\d*)\s*(?:per\s*week|weekly)', 'weekly'),
        (r'\$?(\d+[\.,]?\d*)\s*(?:per\s*month|monthly)', 'monthly'),
        (r'\$?(\d+[\.,]?\d*)\s*(?:per\s*bi-week|bi-weekly)', 'bi-weekly'),
        (r'\$?(\d+[\.,]?\d*)\s*(?:per\s*year|annual|annually|yearly)', 'yearly')
    ]
    currency_patterns = [r'\b(USD|EUR|GBP|CAD|AUD)\b']

    for pattern, period in salary_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            salary = float(match.group(1).replace(',', ''))
            currency_match = re.search('|'.join(currency_patterns), text, re.IGNORECASE)
            currency = currency_match.group(0) if currency_match else 'USD'
            return convert_to_annual_salary(salary, period, currency), currency

    return None, None

def scrape_subreddit(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.top(limit=limit)
    salary_data = []

    for post in posts:
        post_date = datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d')
        post_text = post.title + " " + post.selftext
        salary, currency = extract_salary_details(post_text)
        if salary:
            salary_data.append({
                'Salary (USD)': salary,
                'Location': 'N/A',  # Placeholder, to be extracted
                'Experience (Years)': 'N/A',  # Placeholder, to be extracted
                'Job Title': 'N/A',  # Placeholder, to be extracted
                'Date': post_date,
                'Salary Source': 'Explicit',
                'Additional Information': post.url
            })

        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comment_date = datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d')
            comment_text = comment.body
            salary, currency = extract_salary_details(comment_text)
            if salary:
                salary_data.append({
                    'Salary (USD)': salary,
                    'Location': 'N/A',  # Placeholder, to be extracted
                    'Experience (Years)': 'N/A',  # Placeholder, to be extracted
                    'Job Title': 'N/A',  # Placeholder, to be extracted
                    'Date': comment_date,
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
