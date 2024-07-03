import os
from dotenv import load_dotenv
import praw

# Load environment variables from .env file
load_dotenv()

# Retrieve the values from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Initialize Reddit API with your credentials
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    redirect_uri=REDIRECT_URI
)

# Generate the authorization URL using detailed scopes
auth_url = reddit.auth.url(['identity', 'read'], state='uniqueKey', duration='permanent')
print(f"Visit this URL to authorize: {auth_url}")

# Capture the code from the URL and use it to obtain the refresh token
code = input("Enter the code from the URL: ")

# Obtain the refresh token
try:
    refresh_token = reddit.auth.authorize(code)
    print(f"Refresh token: {refresh_token}")
except Exception as e:
    print(f"Error obtaining refresh token: {e}")
