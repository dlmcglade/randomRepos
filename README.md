# Random Active GitHub Repositories Fetcher
A Python script that fetches a user-specified number of GitHub repositories that have been recently updated and appends their essential details (formatted in Markdown) to a file.

## Description
This script leverages the GitHub Search API to fetch a user-specified number of GitHub repositories updated in the last week. The repositories are appended to a Markdown file (`randomActiveGits.md`). The output provides the repository's URL and description to facilitate sharing and exploring these projects.

## Features

- **Customizable Fetch Quantity:** You can specify the number of repositories to fetch, up to a maximum of 1000. It can be specified by using `-n` followed by the desired number (up to 1000)- although the script may fetch less if there simply aren't that many repositories that have been updated in the last week.
- **API Pagination Handling:** The script effectively manages API pagination to fetch a large number of repositories.
- **Markdown Formatting:** The repositories' essential details are formatted in Markdown, ready for sharing or web presentation.
- **Secure Authentication:** The script uses a GitHub personal access token for secure API access.
- **Recent Updates:** It only fetches repositories that have been updated within the last week.

## NOTE

- The script appends to the output file each time it is run, which could result in a bit of bloating if you're running it over and over, so you may need to manage the output file by occaisionally deleting it or archiving it- will be working on a way to manage this within the script.
