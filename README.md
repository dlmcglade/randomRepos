# Random GitHub Repositories Fetcher

## Introduction
This Python script fetches a list of random active GitHub repositories based on recent activity. It's useful for exploring new projects, understanding trending technologies, or simply satisfying your curiosity about what's happening on GitHub.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation
To use this script, you need Python installed on your system. If you don't have Python, download and install it from [python.org](https://python.org).

1. Clone this repository or download the script directly.
2. Navigate to the script's directory.
3. Install the required dependencies using pip:

```
pip install requests
```

## Usage
Before running the script, ensure you have a GitHub token set as an environment variable `GITHUB_TOKEN`. This token is required to authenticate with the GitHub API and avoid rate limiting.

Run the script with the following command:

```
python randomRepos.py --number <number_of_repositories>
```

- `--number` (optional): Specify the number of random repositories to fetch. Defaults to 50 if not provided.

## Features
- Fetches a specified number of random active GitHub repositories.
- Utilizes the GitHub API with authentication to avoid rate limits.
- Command-line argument support for easy customization.

## Dependencies
- Python 3.x
- `requests` library

## Configuration
Ensure you have a GitHub token and it's set as an environment variable:

```
export GITHUB_TOKEN='your_token_here'
```

## Examples
Fetching 100 random repositories:

```
python randomRepos.py --number 100
```

## Troubleshooting
- **Missing GITHUB_TOKEN**: Make sure you've set the `GITHUB_TOKEN` environment variable as described in the [Configuration](#configuration) section.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
