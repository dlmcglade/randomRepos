import requests
import random
from datetime import datetime, timedelta
import os
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Fetch random active GitHub repositories')
parser.add_argument('-n', '--number', type=int, default=5, help='Number of repositories to fetch')
args = parser.parse_args()

# Number of repositories to fetch
num_repos_to_fetch = min(args.number, 1000)  # Limit to 1000 to adhere to practical limits

# Function to format the repository information in Markdown
def format_repo_in_markdown(repo):
    description = repo['description'] or "No description provided"
    return f"- **[{repo['name']}]({repo['html_url']})**: {description}\n"

# Calculate the date one week ago in the required format
one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GitHub Search API endpoint for repositories
url = "https://api.github.com/search/repositories"

# Use the GITHUB_TOKEN environment variable
github_token = os.getenv('GITHUB_TOKEN')  # Get the GITHUB_TOKEN environment variable

# Make sure you have the GITHUB_TOKEN environment variable set in your environment
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

headers = {"Authorization": f"token {github_token}"}

repositories = []  # List to hold fetched repositories

# Make multiple API calls to fetch up to 1000 repositories
for page in range(1, 11):  # GitHub allows up to 10 pages for search API, 100 items per page
    params = {
        "q": f"pushed:>={one_week_ago}",
        "sort": "updated",
        "order": "desc",
        "per_page": 100,
        "page": page
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    repositories.extend(data['items'])
    # Break if we have fetched all available repositories or reached the desired number
    if len(repositories) >= num_repos_to_fetch or len(data['items']) < 100:
        break

# Adjust the number of repositories to fetch based on the actual number of fetched repositories
num_repos_to_fetch = min(num_repos_to_fetch, len(repositories))

# Randomly select the specified number of repositories from the list
random_repos = random.sample(repositories, num_repos_to_fetch)

# Open the Markdown file in append mode
with open('randomActiveGits.md', 'a') as file:
    # Write a header with the current date and time
    file.write(f"\n## Random Active Repositories as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fetching {num_repos_to_fetch} Repositories\n")
    for repo in random_repos:
        # Format each repository in Markdown and write to the file
        file.write(format_repo_in_markdown(repo))

print(f"{num_repos_to_fetch} random active repositories have been appended to randomActiveGits.md.")
