package main

import (
	"expense-tracker/expense"
	"fmt"
	"os"
	"time"

	"github.com/akamensky/argparse"
)

func main() {
	parser := argparse.NewParser("Expense Tracker", "Track you expenses")

	addCommand := parser.NewCommand("add", "Add a new expense")
	listCommand := parser.NewCommand("list", "List all expenses")
	summaryCommand := parser.NewCommand("summary", "Get a summary of expenses")
	deleteCommand := parser.NewCommand("delete", "Delete an Expense")

	// Add command arguments
	addDescription := addCommand.String("d", "description", &argparse.Options{
		Required: true,
		Help:     "Description of the Expense",
	})

	addAmount := addCommand.Float("a", "amount", &argparse.Options{
		Required: true,
		Help:     "Amount of the expense",
	})

	// Summary command arguments
	summaryMonth := summaryCommand.Int("m", "month", &argparse.Options{
		Required: false,
		Help:     "Get summary of specific month (1-12)",
		Default:  0,
	})

	// Delete command arguments
	deleteId := deleteCommand.Int("i", "id", &argparse.Options{
		Required: true,
		Help:     "ID of the expense to delete",
	})

	// Parse arguments
	if err := parser.Parse(os.Args); err != nil {
		fmt.Println(parser.Usage(err))
		os.Exit(1)
	}

	// Process commands
	service := expense.NewExpenseService("expenses.csv")

	switch {
	case addCommand.Happened():
		id := service.AddExpense(*addDescription, *addAmount)
		fmt.Printf("Expense added successfully (ID: %d)\n", id)
		service.Save()

	case listCommand.Happened():
		service.PrintExpenses()

	case summaryCommand.Happened():
		total := service.Summary(*summaryMonth)
		if *summaryMonth == 0 {
			fmt.Printf("Total Expenses: $%.2f\n", total)
		} else {
			month := time.Month(*summaryMonth).String()
			fmt.Printf("Total Expenses for %s: $%.2f\n", month, total)
		}

	case deleteCommand.Happened():
		service.Delete(*deleteId)
		fmt.Println("Expense deleted successfully")
		service.Save()
	}
}
