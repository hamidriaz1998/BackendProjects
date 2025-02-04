package main

import (
	"fmt"
	task "hamidriaz1998/TaskTrackerCLI/task"
	"log"
	"os"
	"strconv"
)

func main() {
	// Initialize Task Service
	task_service := task.NewTaskService("tasks.json")
	err := task_service.ReadFromFile()
	if err != nil {
		panic(err)
	}

	if len(os.Args) < 2 {
		fmt.Println("Available commands: add, delete, mark, list")
		os.Exit(1)
	}

	switch command := os.Args[1]; command {
	case "add":
		if len(os.Args) < 3 || (len(os.Args) > 2 && os.Args[2] == "help") {
			fmt.Println("Usage: add <task_description>")
			os.Exit(1)
		}
		task_service.AddTask(os.Args[2])
		err = task_service.WriteToFile()
		if err != nil {
			log.Fatalf("Error writing to file: %v", err)
		}

	case "delete":
		if len(os.Args) < 3 || (len(os.Args) > 2 && os.Args[2] == "help") {
			fmt.Println("Usage: delete <task_id>")
			os.Exit(1)
		}
		id, err := strconv.Atoi(os.Args[2])
		if err != nil {
			log.Fatalf("Invalid task ID: %v", err)
		}
		err = task_service.DeleteTask(id)
		if err != nil {
			log.Fatalf("Error deleting task: %v", err)
		}
		err = task_service.WriteToFile()
		if err != nil {
			log.Fatalf("Error writing to file: %v", err)
		}
	case "mark":
		if len(os.Args) < 4 || (len(os.Args) > 2 && os.Args[2] == "help") {
			fmt.Println("Usage: mark <task_id> <new_status>")
			fmt.Println("Status options: todo, in-progress, done")
			os.Exit(1)
		}
		id, err := strconv.Atoi(os.Args[2])
		if err != nil {
			log.Fatalf("Invalid Task id: %v", err)
		}
		err = task_service.UpdateStatus(id, os.Args[3])
		if err != nil {
			log.Fatalf("Error updating task status: %v", err)
		}
		err = task_service.WriteToFile()
		if err != nil {
			log.Fatalf("Error writing to file: %v", err)
		}
	case "list":
		if len(os.Args) > 2 && os.Args[2] == "help" {
			fmt.Println("Usage: list [status]")
			fmt.Println("Status options: todo, in-progress, done")
			os.Exit(1)
		}
		switch length := len(os.Args); length {
		case 2:
			fmt.Println("All Tasks:")
			task_service.PrintTasks()
		case 3:
			filtered_tasks, err := task_service.TasksByStatus(os.Args[2])
			if err != nil {
				log.Fatalf("Error filtering tasks: %v", err)
				os.Exit(1)
			}
			fmt.Println("Printing Tasks with status: ", os.Args[2])
			for _, t := range filtered_tasks {
				t.Print()
			}
		default:
			log.Println("Invalid number of arguments for list command")
			os.Exit(1)
		}
	default:
		fmt.Println("Unknown Command: ", command)
		fmt.Println("Available commands: add, delete, mark, list")
		os.Exit(1)
	}
}
