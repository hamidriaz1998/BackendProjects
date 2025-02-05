# TaskTrackerCLI

Solution for the [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/).
A simple command-line task tracking application written in Go. This application allows you to add, delete, mark (update status), and list tasks. Tasks are stored in a JSON file.

## Features

- **Add tasks:** Add new tasks to your task list.
- **Delete tasks:** Remove tasks from your task list by their ID.
- **Mark tasks:** Update the status of a task (e.g., todo, in-progress, done).
- **List tasks:** Display all tasks or filter tasks by status.
- **Persistence:** Tasks are saved to and loaded from a `tasks.json` file.

## Installation

1.  **Prerequisites:**

    - Go installed on your system (version 1.16 or later).

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/hamidriaz1998/TaskTrackerCLI.git
    cd TaskTrackerCLI
    ```

3.  **Build the application:**

    ```bash
    go build -o tasktracker main.go
    ```

## Usage

```bash
./tasktracker <command> [arguments]
```

### Commands

- **`add <task_description>`:** Adds a new task with the given description.

  ```bash
  ./tasktracker add "Buy groceries"
  ```

- **`delete <task_id>`:** Deletes the task with the given ID.

  ```bash
  ./tasktracker delete 1
  ```

- **`mark <task_id> <new_status>`:** Updates the status of the task with the given ID. Valid status options are: `todo`, `in-progress`, `done`.

  ```bash
  ./tasktracker mark 1 in-progress
  ```

- **`list [status]`:** Lists all tasks or tasks with the specified status. If no status is provided, all tasks are listed. Valid status options are: `todo`, `in-progress`, `done`.

  ```bash
  ./tasktracker list
  ./tasktracker list done
  ```

### Help

Each command has a `help` argument. Use this to get usage instructions.

```bash
./tasktracker add help
./tasktracker delete help
./tasktracker mark help
./tasktracker list help
```

## Configuration

The task data is stored in a file named `tasks.json` in the same directory as the executable. This filename can be changed by modifying the `main.go` file.

## Example

```bash
# Add a task
./tasktracker add "Clean the house"
Task added with ID:  1

# List all tasks
./tasktracker list
All Tasks:
ID: 1, Task: Clean the house, Status: todo

# Mark the task as in-progress
./tasktracker mark 1 in-progress

# List tasks with status "in-progress"
./tasktracker list in-progress
Printing Tasks with status:  in-progress
ID: 1, Task: Clean the house, Status: in-progress

# Mark the task as done
./tasktracker mark 1 done

# Delete the task
./tasktracker delete 1

# List all tasks (should be empty)
./tasktracker list
All Tasks:
```

## Testing

To run the tests, execute the following command:

```bash
go test ./task/...
```

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
