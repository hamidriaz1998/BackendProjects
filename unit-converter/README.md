# Unit Converter

A web-based unit converter application built with Go that allows users to convert between various units of measurement.

## Features

- **Multiple Conversion Types**:

  - Length (millimeter, centimeter, meter, kilometer, inch, foot, yard, mile)
  - Weight (milligram, gram, kilogram, ounce, pound, tonne)
  - Temperature (Celsius, Fahrenheit, Kelvin)

- **Modern User Interface**:

  - Clean, responsive design using Tailwind CSS
  - Tab-based navigation
  - Intuitive form controls

- **Simple to Use**:
  - Enter a value, select your units, and click convert
  - Reset functionality to clear inputs
  - Persistent form values

## Technology Stack

- **Backend**: Go (Golang)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Tailwind CSS

## Getting Started

### Prerequisites

- Go (version 1.18 or higher)
- Node.js and npm (for Tailwind CSS processing)

### Installation

1. Get the code:

   - See the [main repository README](../README.md) for instructions on cloning either the entire repository or just this project using sparse checkout.

2. Install dependencies:

   ```
   go mod tidy
   npm install
   ```

3. Generate CSS:

   ```
   npm run watch
   ```

   (This will start the Tailwind CSS watcher that regenerates the CSS when changes are made)

4. Build and run the application:

   ```
   go build
   ./unit-converter
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Project Structure

```
unit-converter/
├── converter.go       # Core conversion logic
├── main.go            # Web server and HTTP handlers
├── templates/
│   └── index.html     # Main HTML template
├── static/
│   ├── tailwind.css   # Tailwind source CSS
│   └── styles.css     # Compiled CSS
├── go.mod             # Go module definition
└── package.json       # Node.js package definition
```

## Usage

1. Select the type of conversion you want to perform (Length, Weight, or Temperature)
2. Enter the value you want to convert
3. Select the source unit from the "From" dropdown
4. Select the target unit from the "To" dropdown
5. Click "Convert" to see the result
6. Use "Reset" to clear the form

## Acknowledgements

- [Tailwind CSS](https://tailwindcss.com/) for the styling framework
- [Go](https://golang.org/) for the backend language
- [Inter Font](https://rsms.me/inter/) for typography
