package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"
)

type PageData struct {
	// Length data
	LengthValue  string
	LengthFrom   string
	LengthTo     string
	LengthResult string

	// Weight data
	WeightValue  string
	WeightFrom   string
	WeightTo     string
	WeightResult string

	// Temperature data
	TempValue  string
	TempFrom   string
	TempTo     string
	TempResult string

	// Active tab
	ActiveTab string
}

var data PageData = PageData{
	LengthValue: "",
	LengthFrom:  "meter",
	LengthTo:    "foot",
	WeightValue: "",
	WeightFrom:  "kilogram",
	WeightTo:    "pound",
	TempValue:   "",
	TempFrom:    "celsius",
	TempTo:      "fahrenheit",
	ActiveTab:   "length",
}

func main() {
	// Parse templates
	tmpl, err := template.ParseFiles("templates/index.html")
	if err != nil {
		log.Fatalf("Error parsing templates: %v", err)
	}

	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl.Execute(w, data)
	})

	http.HandleFunc("/convert/length", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Redirect(w, r, "/", http.StatusSeeOther)
			return
		}

		valueStr := r.FormValue("value")
		from := r.FormValue("from")
		to := r.FormValue("to")

		data.LengthTo = to
		data.LengthFrom = from
		data.LengthValue = valueStr

		value, err := strconv.ParseFloat(valueStr, 64)
		if err != nil {
			data.LengthResult = "Invalid input"
			tmpl.Execute(w, data)
			return
		}

		converter := NewConverter("length", from, to, value)
		result := converter.Convert()
		data.LengthResult = fmt.Sprintf("%.6g %s = %.6g %s", value, from, result, to)
		data.ActiveTab = "length"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/convert/weight", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Redirect(w, r, "/", http.StatusSeeOther)
			return
		}

		valueStr := r.FormValue("value")
		from := r.FormValue("from")
		to := r.FormValue("to")

		data.WeightValue = valueStr
		data.WeightFrom = from
		data.WeightTo = to

		value, err := strconv.ParseFloat(valueStr, 64)
		if err != nil {
			data.WeightResult = "Invalid input"
			tmpl.Execute(w, data)
			return
		}

		converter := NewConverter("weight", from, to, value)
		result := converter.Convert()
		data.WeightResult = fmt.Sprintf("%.6g %s = %.6g %s", value, from, result, to)
		data.ActiveTab = "weight"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/convert/temperature", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Redirect(w, r, "/", http.StatusSeeOther)
			return
		}

		valueStr := r.FormValue("value")
		from := r.FormValue("from")
		to := r.FormValue("to")

		data.TempValue = valueStr
		data.TempFrom = from
		data.TempTo = to

		value, err := strconv.ParseFloat(valueStr, 64)
		if err != nil {
			data.TempResult = "Invalid input"
			tmpl.Execute(w, data)
			return
		}

		converter := NewConverter("temperature", from, to, value)
		result := converter.Convert()
		data.TempResult = fmt.Sprintf("%.6g %s = %.6g %s", value, from, result, to)
		data.ActiveTab = "temp"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/reset/length", func(w http.ResponseWriter, r *http.Request) {
		data.LengthValue = ""
		data.LengthFrom = "meter"
		data.LengthTo = "foot"
		data.LengthResult = ""
		data.ActiveTab = "length"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/reset/temperature", func(w http.ResponseWriter, r *http.Request) {
		data.TempValue = ""
		data.TempFrom = "celsius"
		data.TempTo = "fahrenheit"
		data.TempResult = ""
		data.ActiveTab = "temp"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/reset/weight", func(w http.ResponseWriter, r *http.Request) {
		data.WeightValue = ""
		data.WeightFrom = "kilogram"
		data.WeightTo = "pound"
		data.WeightResult = ""
		data.ActiveTab = "weight"

		tmpl.Execute(w, data)
	})

	http.HandleFunc("/reset/all", func(w http.ResponseWriter, r *http.Request) {
		data.LengthValue = ""
		data.LengthFrom = "meter"
		data.LengthTo = "foot"
		data.LengthResult = ""
		data.TempValue = ""
		data.TempFrom = "celsius"
		data.TempTo = "fahrenheit"
		data.TempResult = ""
		data.WeightValue = ""
		data.WeightFrom = "kilogram"
		data.WeightTo = "pound"
		data.WeightResult = ""
		data.ActiveTab = "length"

		tmpl.Execute(w, data)
	})

	fmt.Println("Server starting on http://localhost:3000")
	log.Fatal(http.ListenAndServe(":3000", nil))
}
