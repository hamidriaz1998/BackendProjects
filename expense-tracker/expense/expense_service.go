package expense

import (
	"fmt"
	"os"
	"time"

	"slices"

	"github.com/gocarina/gocsv"
)

type ExpenseService struct {
	FilePath string
	Expenses []Expense
}

func NewExpenseService(filepath string) *ExpenseService {
	service := ExpenseService{
		FilePath: filepath,
		Expenses: []Expense{},
	}
	service.Load()
	return &service
}

func (service *ExpenseService) Save() {
	file, err := os.Create(service.FilePath)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	if err := gocsv.MarshalFile(&service.Expenses, file); err != nil {
		panic(err)
	}
}
func (service *ExpenseService) Load() {
	info, err := os.Stat(service.FilePath)
	if os.IsNotExist(err) {
		emptyFile, err := os.Create(service.FilePath)
		if err != nil {
			panic(err)
		}
		emptyFile.Close()
		return
	}

	// If file size is 0 bytes, it's empty
	if info.Size() == 0 {
		return
	}

	file, err := os.Open(service.FilePath)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	if err := gocsv.UnmarshalFile(file, &service.Expenses); err != nil {
		panic(err)
	}
}

func (service *ExpenseService) PrintExpenses() {
	fmt.Println("ID     Date                 Description               Amount")
	fmt.Println("------ -------------------- ------------------------- ----------")
	for _, expense := range service.Expenses {
		expense.Print()
	}
}

func (service *ExpenseService) AddExpense(description string, amount float64) int {
	var id int
	if len(service.Expenses) == 0 {
		id = 1
	} else {
		id = service.Expenses[len(service.Expenses)-1].Id + 1
	}
	service.Expenses = append(service.Expenses,
		Expense{
			Id:          id,
			Date:        time.Now(),
			Description: description,
			Amount:      amount,
		},
	)
	return id
}

func (service *ExpenseService) Summary(month int) float64 {
	sum := 0.0

	if month <= 0 || month >= 12 {
		for _, e := range service.Expenses {
			sum += e.Amount
		}
		return sum
	}

	for _, e := range service.Expenses {
		if int(e.Date.Month()) == month {
			sum += e.Amount
		}
	}
	return sum
}

func (service *ExpenseService) Delete(id int) {
	for i, e := range service.Expenses {
		if e.Id == id {
			service.Expenses = slices.Delete(service.Expenses, i, i+1)
			return
		}
	}
}
