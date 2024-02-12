# Random Repos

## Introduction

`Random Repos` is a Python script designed to fetch random active GitHub repositories based on recent activity and summarize their READMEs. This tool is especially useful for developers looking to discover new projects, trends, or technologies within the GitHub community. Many repositories will not have a README. These are ommitted from the results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

To install `Random Repos`, you'll need Python 3.x and `pip`. Clone this repository or download the script directly. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use `Random Repos`, execute the script with Python and specify the desired number of repositories to fetch using the `-n` or `--number` argument:

```bash
python randomRepos.py --number 50
```

## Features

- Fetches active GitHub repositories based on recent activity.
- Summarizes READMEs of fetched repositories using OpenAI's API.
- Filters out already listed repositories to avoid duplicates.
- Generates markdown files for easy viewing and sharing.

## Dependencies

- `requests`: For making HTTP requests to GitHub's API.
- `beautifulsoup4`: For parsing HTML content.
- `openai`: To access OpenAI's API for summarizing READMEs.

## Configuration

Ensure you have set the following environment variables before running the script:

- `GITHUB_TOKEN`: Your GitHub API token.
- `OPENAI_API_TOKEN`: Your OpenAI API key.

## Documentation

For more detailed information about each function and its usage, refer to the inline comments within the script.

## Examples

Example of running the script to fetch and summarize 100 repositories:

```bash
python randomRepos.py --number 100
```

## Troubleshooting

If you encounter any issues regarding missing environment variables, ensure you have correctly set `GITHUB_TOKEN` and `OPENAI_API_TOKEN` in your environment.

## Contributors

Feel free to contribute to the project by submitting pull requests or opening issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
