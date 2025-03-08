package expense

import (
	"fmt"
	"time"
)

type Expense struct {
	Id          int       `csv:"id"`
	Date        time.Time `csv:"date"`
	Description string    `csv:"description"`
	Amount      float64   `csv:"amount"`
}

func (e Expense) Print() {
	fmt.Printf("%-6d\t%-20s\t%-25s\t$%.2f\n", e.Id, e.GetDate(), e.Description, e.Amount)
}

func (e Expense) GetDate() string {
	y, m, d := e.Date.Date()
	return fmt.Sprintf("%d-%v-%d", y, m, d)
}
