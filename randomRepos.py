import requests
from datetime import datetime, timedelta
import os
import argparse
from bs4 import BeautifulSoup
from openai import OpenAI

# Setup argument parsing
parser = argparse.ArgumentParser(description='Fetch random active GitHub repositories based on recent activity and summarize their READMEs')
parser.add_argument('-n', '--number', type=int, default=100, help='Number of repositories to fetch')
args = parser.parse_args()

# Ensure the GITHUB_TOKEN and OPENAI_API_TOKEN are set
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')
if not GITHUB_TOKEN or not OPENAI_API_TOKEN:
    print("One or more required environment variables (GITHUB_TOKEN, OPENAI_API_TOKEN) are not set.")
    exit()

client = OpenAI(api_key=OPENAI_API_TOKEN)

# GitHub Search API and OpenAI configurations
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

def fetch_content(url):
    """Fetch the 'README' section text content of a web page given its URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        readme_section = soup.find('article', class_='markdown-body')
        if readme_section:
            text = readme_section.get_text(separator=' ', strip=True)
        else:
            text = None
        return text
    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None

def summarize_content(content):
    """Generate a short summary of the provided content using OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize this content in a short paragraph:\n{content}"}
            ]
        )
        # Assuming the first choice's message content is directly accessible as an attribute
        summary = response.choices[0].message.content.strip() if response.choices else "Summary not available."
        return summary
    except Exception as e:
        print(f"Failed to summarize content: {e}")
        return None



def main():
    fetched_repos = fetch_repositories(args.number)
    existing_repos = read_and_categorize_existing_file()

    existing_repo_urls = [line.split('](')[1].split(')')[0] for line in existing_repos]
    new_repos_markdown = [format_repo_in_markdown(repo) for repo in fetched_repos if repo['html_url'] not in existing_repo_urls]

    # Update markdown file with new repositories
    update_markdown_file(new_repos_markdown, existing_repos)

    # New section to fetch, summarize READMEs, and write summaries
    summaries = []
    for repo in fetched_repos:
        repo_readme_url = repo['html_url']  # Assuming README at repo main page, adjust if needed
        content = fetch_content(repo_readme_url)
        if content:
            summary = summarize_content(content)
            if summary:
                summaries.append(f"- **[{repo['name']}]({repo['html_url']}):** {summary}\n")

    # Write summaries to a separate file
    if summaries:
        with open('repo_summaries.md', 'w', encoding='utf-8') as summary_file:
            summary_file.write("## Repository Summaries\n")
            summary_file.writelines(summaries)

    # Output summary information
    print(f"New Repositories Found: {len(new_repos_markdown)}")
    total_repos = len(existing_repos) + len(new_repos_markdown)
    print(f"Total Repositories in File Now: {total_repos}")
    print(f"Summaries Generated: {len(summaries)}")

if __name__ == "__main__":
    start_time = datetime.now()  # Record the start time
    print("Script started.")

    main()

    print("Script ended.")
    end_time = datetime.now()  # Record the end time
    execution_time = end_time - start_time  # Calculate the difference
    print(f"Execution Time: {execution_time}")


