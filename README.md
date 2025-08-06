# Backend Projects Repository

This repository serves as a central hub for my backend projects and code experiments. It's designed to house a variety of projects, ranging from simple API implementations to more complex distributed systems prototypes. The aim is to create a well-organized and documented collection of backend-related code.

## Project Overview

| Project Name                                     | Description                                                                                                                    |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [TaskTracker](./TaskTracker)                     | A simple command-line task tracking application written in Go, demonstrating CLI tool development and JSON data persistence.   |
| [github-activity](./github-activity)             | A simple CLI tool written in Go that fetches and displays a user's GitHub activity.                                            |
| [expense-tracker](./expense-tracker)             | A simple command-line expense tracking application written in Go, demonstrating CLI tool development and CSV data persistence. |
| [unit-converter](./unit-converter)               | A web application written in Go that provides a simple unit conversion service.                                                |
| [port-scanner](./port_scanner_py)                | A simple CLI tool written in Python that scans a range of ports on a given host.                                               |
| [weather-api](./weather-api)                     | A simple CLI tool written in Go that fetches and displays weather information for a given location.                            |
| [url-shortener-fastapi](./url-shortener-fastapi) | A simple URL shortening service written in FastAPI, demonstrating RESTful API development and database integration.            |
| [url-shortener-ts](./url-shortener-ts)           | A simple URL shortening service written in TypeScript, demonstrating RESTful API development and database integration.         |
| [personalBlog](./personalBlog)                   | A personal blog written in fastapi and jinja2 templates with bootstrap styling.                                                |
| [bloggingApi](./bloggingApi)                     | A simple blogging API written in fastapi, demonstrating RESTful API development and database integration.                      |

## Usage

### Option 1: Clone the entire repository

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/hamidriaz1998/BackendProjects.git
    cd BackendProjects
    ```

2.  **Navigate to a Project:**

    ```bash
    cd TaskTracker  # Example
    ```

3.  **Follow the Project's README:** Each project has its own `README.md` with specific instructions for building, running, and using the code.

### Option 2: Clone a single project using sparse checkout

If you only want to download the code for a specific project:

1. **Initialize a new repository:**

   ```bash
   git init <project-name>
   cd <project-name>
   ```

2. **Add the remote repository:**

   ```bash
   git remote add origin https://github.com/hamidriaz1998/BackendProjects.git
   ```

3. **Enable sparse checkout:**

   ```bash
   git config core.sparseCheckout true
   ```

4. **Specify which project you want:**

   ```bash
   echo "BackendProjects/<project-name>/*" >> .git/info/sparse-checkout
   ```

5. **Pull the content:**

   ```bash
   git pull origin main
   ```

6. **Follow the Project's README:** Check the project's `README.md` for specific instructions.
