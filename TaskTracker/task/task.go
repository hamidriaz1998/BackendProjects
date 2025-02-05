package task

import (
	"fmt"
	"time"
)

type Task struct {
	Id     int    `json:"id"`
	Description   string `json:"description"`
	Status string `json:"status"`
	CreatedAt time.Time  `json:"createdAt"`
	UpdatedAt time.Time  `json:"updatedAt"`
}

func (task Task) Print() {
	fmt.Printf("ID: %d, Task: %s, Status: %s\n", task.Id, task.Description, task.Status)
}
