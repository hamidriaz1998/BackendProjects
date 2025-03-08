# Expense Tracker CLI

A simple command-line application for tracking personal expenses, written in Go.

## Features

- Add expenses with descriptions and amounts
- List all recorded expenses
- Get a summary of all expenses
- Get a summary of expenses by month
- Delete expenses by ID

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Build the application
go build
```

## Usage

### Adding an Expense

```bash
expense-tracker add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)
```

Arguments:

- `-d, --description` - Description of the expense (required)
- `-a, --amount` - Amount of the expense (required)

### Listing Expenses

```bash
expense-tracker list
# ID   Date        Description   Amount
# 1    2024-08-06  Lunch         $20.000000
```

### Getting Expense Summaries

For all expenses:

```bash
expense-tracker summary
# Total Expenses: $30.00
```

For expenses in a specific month:

```bash
expense-tracker summary --month 8
# Total Expenses for August: $20.00
```

Arguments:

- `-m, --month` - Get summary for specific month (1-12) (optional)

### Deleting an Expense

```bash
expense-tracker delete --id 2
# Expense deleted successfully
```

Arguments:

- `-i, --id` - ID of the expense to delete (required)

## Data Storage

Expenses are stored in a CSV file named `expenses.csv` in the same directory as the application. The file is created automatically when the application is first run.

## Dependencies

- [github.com/akamensky/argparse](https://github.com/akamensky/argparse) - Command-line argument parsing
- [github.com/gocarina/gocsv](https://github.com/gocarina/gocsv) - CSV handling for Go