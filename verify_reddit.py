import os
from dotenv import load_dotenv
import praw

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

# Fetch public data
try:
    print("Fetching public data from r/accounting...")
    for submission in reddit.subreddit('accounting').hot(limit=5):
        print(submission.title)
except Exception as e:
    print(f"Error fetching public data: {e}")

# Verify authentication
try:
    user = reddit.user.me()
    print(f"Authenticated as {user}")
except Exception as e:
    print(f"Authentication failed: {e}")
