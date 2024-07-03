import os
import openai
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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Reddit API with your credentials
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    refresh_token=REFRESH_TOKEN
)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

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
        'hourly': r'\$([0-9]+(\.[0-9]+)?)\s*/\s*hour',
        'weekly': r'\$([0-9]+(\.[0-9]+)?)\s*/\s*week',
        'monthly': r'\$([0-9]+(\.[0-9]+)?)\s*/\s*month',
        'bi-weekly': r'\$([0-9]+(\.[0-9]+)?)\s*/\s*bi-week',
        'yearly': r'\$([0-9]+(\.[0-9]+)?)\s*/\s*year',
        'annual': r'\$([0-9]+(\.[0-9]+)?)\s*(?:per\s*)?year'
    }
    for period, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            salary = float(match.group(1))
            return convert_to_annual_salary(salary, period)
    return None

def extract_additional_details(text):
    location_pattern = r'(?i)\b(?:location|city|state|country):\s*(\w+(?:\s+\w+)*)'
    experience_pattern = r'(?i)\b(?:experience|years):\s*([0-9]+)\s*(?:years|yrs)?'
    job_title_pattern = r'(?i)\b(?:job|title|position):\s*(\w+(?:\s+\w+)*)'

    location = re.search(location_pattern, text)
    experience = re.search(experience_pattern, text)
    job_title = re.search(job_title_pattern, text)

    return {
        'Location': location.group(1) if location else 'N/A',
        'Experience (Years)': experience.group(1) if experience else 'N/A',
        'Job Title': job_title.group(1) if job_title else 'N/A'
    }

def get_vague_salary_from_gpt(text):
    prompt = (
        "Extract an estimated annual salary from the following text if it vaguely alludes to salary information:\n\n"
        f"Text: {text}\n\n"
        "Response: "
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5
    )
    return response.choices[0].text.strip()

def scrape_subreddit(subreddit_name, limit=300):
    salary_data = []
    vague_data = []
    subreddit = reddit.subreddit(subreddit_name)
    for comment in subreddit.comments(limit=limit):
        comment_text = comment.body
        print(f"Checking comment: {comment_text}")  # Debugging print
        salary = extract_salary_details(comment_text)
        if salary:
            print(f"Extracted salary: {salary}")  # Debugging print
            additional_details = extract_additional_details(comment_text)
            salary_data.append({
                'Salary (USD)': salary,
                'Location': additional_details['Location'],
                'Experience (Years)': additional_details['Experience (Years)'],
                'Job Title': additional_details['Job Title'],
                'Date': comment.created_utc,
                'Salary Source': 'Explicit',
                'Additional Information': comment.link_permalink,
                'URL': f"https://reddit.com{comment.permalink}"
            })
        else:
            vague_salary = get_vague_salary_from_gpt(comment_text)
            if vague_salary:
                additional_details = extract_additional_details(comment_text)
                vague_data.append({
                    'Vague Salary': vague_salary,
                    'Location': additional_details['Location'],
                    'Experience (Years)': additional_details['Experience (Years)'],
                    'Job Title': additional_details['Job Title'],
                    'Date': comment.created_utc,
                    'Salary Source': 'Vague',
                    'Additional Information': comment.link_permalink,
                    'URL': f"https://reddit.com{comment.permalink}"
                })
        if len(salary_data) >= 300:
            break
    return salary_data, vague_data

def save_to_csv(data, filename):
    if not data:
        print("No salary data found.")  # Debugging print
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Main script
explicit_salary_data, vague_salary_data = scrape_subreddit('accounting', limit=1000)
save_to_csv(explicit_salary_data, 'explicit_salary_data.csv')
save_to_csv(vague_salary_data, 'vague_salary_data.csv')
