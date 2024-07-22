import os
import json
import praw
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

# Get the current time and time three months ago
current_time = datetime.utcnow()
three_months_ago = current_time - timedelta(days=90)

def fetch_top_posts_and_comments(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    
    # Fetch the top posts of the last 3 months
    try:
        top_posts = subreddit.top(time_filter="month", limit=limit)
    except Exception as e:
        print(f"Error fetching top posts: {e}")
        return []

    data = []
    for post in top_posts:
        try:
            post_time = datetime.utcfromtimestamp(post.created_utc)
            print(f"Checking post: {post.title} - {post_time}")
            if post_time > three_months_ago:
                print(f"Found post: {post.title} - {post_time}")
                post_data = {
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "created": post_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "comments": [],
                    "theme": "Victorian Accountant"
                }

                # Fetch the top comments for the post
                post.comments.replace_more(limit=0)
                top_comments = post.comments.list()[:limit]
                for comment in top_comments:
                    comment_data = {
                        "body": comment.body,
                        "score": comment.score,
                        "created": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "theme": "Victorian Accountant"
                    }
                    post_data["comments"].append(comment_data)

                data.append(post_data)
            else:
                print(f"Post {post.title} is older than three months and will be skipped.")
        except Exception as e:
            print(f"Error processing post {post.id}: {e}")
    
    return data

# Fetch the data
print("Starting data fetch...")
data = fetch_top_posts_and_comments('accounting')
print(f"Data fetched: {data}")

# Save the data to a JSON file
try:
    with open('reddit_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data fetched and saved to reddit_data.json")
except Exception as e:
    print(f"Error saving data to JSON file: {e}")
