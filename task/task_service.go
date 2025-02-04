package task

import (
	"encoding/json"
	"errors"
	"os"
	"time"
)

type TaskService struct {
	Tasks    []Task
	FilePath string
}

// NewTaskService creates a new TaskService instance.
func NewTaskService(filePath string) *TaskService {
	return &TaskService{
		Tasks:    []Task{},
		FilePath: filePath,
	}
}

func (ts *TaskService) PrintTasks() {
	for _, task := range ts.Tasks {
		task.Print()
	}
}

// AddTask adds a new task.
func (ts *TaskService) AddTask(task string) {
	ts.Tasks = append(ts.Tasks, Task{Id: len(ts.Tasks) + 1, Description: task, Status: "todo", CreatedAt: time.Now(), UpdatedAt: time.Now()})
}

// UpdateTask updates the task description for a given ID.
func (ts *TaskService) UpdateTask(id int, task string) error {
	for i := range ts.Tasks {
		if ts.Tasks[i].Id == id {
			ts.Tasks[i].Description = task
			return nil
		}
	}
	return errors.New("task not found")
}

// UpdateStatus updates the status of a task.
func (ts *TaskService) UpdateStatus(id int, status string) error {
	if status != "todo" && status != "in-progress" && status != "done" {
		return errors.New("invalid status")
	}
	for i := range ts.Tasks {
		if ts.Tasks[i].Id == id {
			ts.Tasks[i].Status = status
			return nil
		}
	}
	return errors.New("task not found")
}

// DeleteTask deletes a task by ID.
func (ts *TaskService) DeleteTask(id int) error {
	for i := range ts.Tasks {
		if ts.Tasks[i].Id == id {
			ts.Tasks = append(ts.Tasks[:i], ts.Tasks[i+1:]...)
			return nil
		}
	}
	return errors.New("task not found")
}

// TasksByStatus returns tasks filtered by status.
func (ts *TaskService) TasksByStatus(status string) ([]Task, error) {
	if status != "in-progress" && status != "todo" && status != "done" {
		return nil, errors.New("invalid status")
	}
	result := []Task{}
	for _, task := range ts.Tasks {
		if task.Status == status {
			result = append(result, task)
		}
	}
	return result, nil
}

// WriteToFile writes tasks to the JSON file.
func (ts *TaskService) WriteToFile() error {
	jsonData, err := json.Marshal(ts.Tasks)
	if err != nil {
		return err
	}
	err = os.WriteFile(ts.FilePath, jsonData, 0644)
	if err != nil {
		return err
	}
	return nil
}

// ReadFromFile reads tasks from the JSON file.
func (ts *TaskService) ReadFromFile() error {
	data, err := os.ReadFile(ts.FilePath)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			ts.Tasks = []Task{}
			return nil
		}
		return err
	}

	err = json.Unmarshal(data, &ts.Tasks)
	if err != nil {
		return err
	}
	return nil
}
