# GitHub Activity CLI

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

*   Pushing commits
*   Creating issues
*   Starring repositories
*   Forking repositories
*   Creating branches/repositories

## Prerequisites

*   Go installed (version 1.23.2 or later).

## Installation

1.  Clone the repository.
2.  Navigate to the `github-activity` directory.
3.  Run `go mod tidy` to download dependencies.
