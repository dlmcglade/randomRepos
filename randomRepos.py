import requests
import random
from datetime import datetime, timedelta
import os
import argparse

# Setup argument parsing
parser = argparse.ArgumentParser(description='Fetch random active GitHub repositories based on recent activity')
parser.add_argument('-n', '--number', type=int, default=50, help='Number of repositories to fetch')
args = parser.parse_args()

# Ensure the GITHUB_TOKEN is set
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("GITHUB_TOKEN environment variable not set.")
    exit()

# GitHub Search API endpoint configuration
API_URL = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
DATE_ONE_WEEK_AGO = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

def fetch_repositories(num_repos):
    all_repos = []
    page = 1
    while len(all_repos) < num_repos:
        params = {
            "q": f"pushed:>={DATE_ONE_WEEK_AGO}",
            "sort": "updated",
            "order": "desc",
            "per_page": 100,
            "page": page
        }
        response = requests.get(API_URL, headers=HEADERS, params=params).json()
        repos = response.get('items', [])
        if not repos:
            break  # No more items to fetch
        all_repos.extend(repos)
        if len(repos) < 100:  # Less than 100 results indicates last page
            break
        page += 1
    return all_repos[:num_repos]

def format_repo_in_markdown(repo):
    return f"- **[{repo['name']}]({repo['html_url']})**: {repo.get('description', 'No description provided')}"

def read_and_categorize_existing_file():
    existing_repos = []
    try:
        with open('randomActiveGits.md', 'r') as file:
            lines = file.readlines()
            existing_repos = [line.strip() for line in lines if line.startswith("- **[")]
    except FileNotFoundError:
        pass
    return existing_repos

def update_markdown_file(new_repos, existing_repos):
    with open('randomActiveGits.md', 'w') as file:
        if new_repos:
            file.write("## New Repositories\n")
            file.write("\n".join(new_repos) + "\n\n")
        if existing_repos:
            file.write("## Existing Repositories\n")
            file.write("\n".join(existing_repos) + "\n")

def main():
    fetched_repos = fetch_repositories(args.number)
    existing_repos = read_and_categorize_existing_file()

    # Extract URLs for comparison to identify truly new repos
    existing_repo_urls = [line.split('](')[1].split(')')[0] for line in existing_repos]
    new_repos = [format_repo_in_markdown(repo) for repo in fetched_repos if repo['html_url'] not in existing_repo_urls]

    # Combine new and existing repositories for the update
    update_markdown_file(new_repos, existing_repos)

    # Output summary information
    print(f"New Repositories Found: {len(new_repos)}")
    total_repos = len(existing_repos) + len(new_repos)  # Correctly count total repositories
    print(f"Total Repositories in File Now: {total_repos}")

if __name__ == "__main__":
    main()
