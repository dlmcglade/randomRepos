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

# Load existing data
try:
    with open('randomActiveGits.md', 'r') as file:
        existing_data = file.read()
except FileNotFoundError:
    existing_data = ""

# Determine new and duplicate repos
new_section_label = "## New Repositories\n"
existing_repos = existing_data.split(new_section_label)[0] if new_section_label in existing_data else existing_data
new_repos_section = existing_data.split(new_section_label)[1] if new_section_label in existing_data else ""

new_repos = []
duplicates = []
for repo in random_repos:
    repo_markdown = format_repo_in_markdown(repo)
    if repo_markdown not in existing_data:
        new_repos.append(repo_markdown)
    else:
        duplicates.append(repo_markdown)

# Update the file
with open('randomActiveGits.md', 'w') as file:
    if existing_repos.strip():
        file.write(existing_repos.strip() + "\n\n")
    if duplicates:
        file.write("## Duplicates (Previously New)\n")
        file.write("".join(duplicates) + "\n")
    if new_repos:
        file.write(new_section_label)
        file.write("".join(new_repos))

print(f"Updated randomActiveGits.md with {len(new_repos)} new repositories and {len(duplicates)} duplicates.")
