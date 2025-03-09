# GitHub Activity CLI

Solution for the [github-user-activity](https://roadmap.sh/projects/github-user-activity) challenge from [roadmap.sh](https://roadmap.sh/).

A command-line tool to display recent public activity for a given GitHub username.

## Usage

```bash
go run main.go <username>
```

Example:

```bash
go run main.go hamidriaz1998
```

## Output

The tool will fetch and display a list of recent GitHub activities, such as:

- Pushing commits
- Creating issues
- Starring repositories
- Forking repositories
- Creating branches/repositories

## Prerequisites

- Go installed (version 1.23.2 or later).

## Installation

1.  Get the code:

    - See the [main repository README](../README.md) for instructions on cloning either the entire repository or just this project using sparse checkout.

2.  Navigate to the `github-activity` directory (if you cloned the entire repository).
3.  Run `go mod tidy` to download dependencies.
