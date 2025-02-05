package task_test

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"testing"
	"time"

	task "hamidriaz1998/TaskTrackerCLI/task"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestTaskService_AddTask(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add a task
	task_service.AddTask("task 1")

	// Verify the task was added
	assert.Len(t, task_service.Tasks, 1)
	assert.Equal(t, "task 1", task_service.Tasks[0].Description)
	assert.Equal(t, "todo", task_service.Tasks[0].Status)
}

func TestTaskService_UpdateTask(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add a task
	task_service.AddTask("task 1")

	// Update the task
	err = task_service.UpdateTask(1, "updated task 1")
	require.NoError(t, err)

	// Verify the task was updated
	assert.Len(t, task_service.Tasks, 1)
	assert.Equal(t, "updated task 1", task_service.Tasks[0].Description)
}

func TestTaskService_UpdateStatus(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add a task
	task_service.AddTask("task 1")

	// Update the status
	err = task_service.UpdateStatus(1, "in-progress")
	require.NoError(t, err)

	// Verify the status was updated
	assert.Len(t, task_service.Tasks, 1)
	assert.Equal(t, "in-progress", task_service.Tasks[0].Status)
}

func TestTaskService_DeleteTask(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add a task
	task_service.AddTask("task 1")

	// Delete the task
	err = task_service.DeleteTask(1)
	require.NoError(t, err)

	// Verify the task was deleted
	assert.Len(t, task_service.Tasks, 0)
}

func TestTaskService_TasksByStatus(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add tasks with different statuses
	task_service.AddTask("task 1")
	task_service.AddTask("task 2")
	task_service.UpdateStatus(1, "in-progress")

	// Get tasks by status
	tasks, err := task_service.TasksByStatus("in-progress")
	require.NoError(t, err)

	// Verify the correct tasks were returned
	assert.Len(t, tasks, 1)
	assert.Equal(t, "task 1", tasks[0].Description)
}

func TestTaskService_WriteToFile(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add a task
	task_service.AddTask("task 1")

	// Write tasks to file
	err = task_service.WriteToFile()
	require.NoError(t, err)

	// Read tasks from file
	data, err := ioutil.ReadFile(file.Name())
	require.NoError(t, err)

	// Verify the tasks were written to the file
	var tasks []task.Task
	err = json.Unmarshal(data, &tasks)
	require.NoError(t, err)
	assert.Len(t, tasks, 1)
	assert.Equal(t, "task 1", tasks[0].Description)
}

func TestTaskService_ReadFromFile(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Write tasks to file
	tasks := []task.Task{
		{Id: 1, Description: "task 1", Status: "todo", CreatedAt: time.Now(), UpdatedAt: time.Now()},
	}
	data, err := json.Marshal(tasks)
	require.NoError(t, err)
	err = ioutil.WriteFile(file.Name(), data, 0644)
	require.NoError(t, err)

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Read tasks from file
	err = task_service.ReadFromFile()
	require.NoError(t, err)

	// Verify the tasks were read from the file
	assert.Len(t, task_service.Tasks, 1)
	assert.Equal(t, "task 1", task_service.Tasks[0].Description)
}

func TestTaskService_ReadFromFile_Error(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Read tasks from file
	err = task_service.ReadFromFile()
	require.Error(t, err)
}

func TestTask_Print(t *testing.T) {
	task := task.Task{Id: 1, Description: "task 1", Status: "todo", CreatedAt: time.Now(), UpdatedAt: time.Now()}
	task.Print()
}

func TestTaskService_PrintTasks(t *testing.T) {
	// Create a temporary file
	file, err := ioutil.TempFile("", "tasks.json")
	require.NoError(t, err)
	defer os.Remove(file.Name())

	// Initialize Task Service
	task_service := task.NewTaskService(file.Name())

	// Add tasks
	task_service.AddTask("task 1")
	task_service.AddTask("task 2")

	// Print tasks
	task_service.PrintTasks()
}
