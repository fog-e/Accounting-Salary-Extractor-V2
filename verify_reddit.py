import os
import praw
from dotenv import load_dotenv

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

# Fetch a sample subreddit to verify connection
subreddit = reddit.subreddit("accounting")
print(f"Authenticated as {reddit.user.me()}")
print(f"Fetching public data from {subreddit.display_name}...")

for submission in subreddit.hot(limit=5):
    print(submission.title)
