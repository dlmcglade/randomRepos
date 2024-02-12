## Overview

randomRepos is a code snippet that fetches random active GitHub repositories based on recent activity. Its purpose is to provide a tool for discovering repositories that have been pushed within the last week. By using the GitHub Search API, it retrieves the latest repositories and compares them with existing ones stored in a markdown file. The project's value proposition lies in its ability to keep users informed about new repositories and provide a useful metric by displaying the number of new repositories found and the total number of repositories in the file.

## Note on API Rate Limit

When using the -n argument to specify the number of repos to fetch (in the thousands, for example), it is easy to hit the API rate limit, so go easy!
