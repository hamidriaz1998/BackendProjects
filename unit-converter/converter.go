package main

import "strings"

type Converter struct {
	Measurement string
	FromUnit    string
	ToUnit      string
	value       float64
}

func NewConverter(measurement, from, to string, value float64) *Converter {
	return &Converter{
		Measurement: measurement,
		FromUnit:    from,
		ToUnit:      to,
		value:       value,
	}
}

func (conv Converter) Convert() float64 {
	if conv.FromUnit == conv.ToUnit {
		return conv.value
	}
	switch strings.ToLower(conv.Measurement) {
	case "length":
		return conv.ConvertLength()
	case "weight":
		return conv.ConvertWeight()
	case "temperature":
		return conv.ConvertTemperature()
	}
	return 0.0
}

func (conv Converter) ConvertLength() float64 {
	toMeters := map[string]float64{
		"millimeter": 0.001,
		"centimeter": 0.01,
		"meter":      1.0,
		"kilometer":  1000.0,
		"inch":       0.0254,
		"foot":       0.3048,
		"yard":       0.9144,
		"mile":       1609.34,
	}

	valueInMeters := conv.value * toMeters[strings.ToLower(conv.FromUnit)]
	result := valueInMeters / toMeters[strings.ToLower(conv.ToUnit)]

	return result
}

func (conv Converter) ConvertWeight() float64 {
	toKilograms := map[string]float64{
		"gram":      0.001,
		"milligram": 0.000001,
		"kilogram":  1.0,
		"tonne":     1000.0,
		"ounce":     0.0283495,
		"pound":     0.453592,
	}

	valueInKilograms := conv.value * toKilograms[strings.ToLower(conv.FromUnit)]
	result := valueInKilograms / toKilograms[strings.ToLower(conv.ToUnit)]

	return result
}

func (conv Converter) ConvertTemperature() float64 {
	from := strings.ToLower(conv.FromUnit)
	to := strings.ToLower(conv.ToUnit)

	if from == to {
		return conv.value
	}

	var valueInCelsius float64
	switch from {
	case "celsius":
		valueInCelsius = conv.value
	case "fahrenheit":
		valueInCelsius = (conv.value - 32) * 5.0 / 9.0
	case "kelvin":
		valueInCelsius = conv.value - 273.15
	}

	switch to {
	case "celsius":
		return valueInCelsius
	case "fahrenheit":
		return (valueInCelsius * 9.0 / 5.0) + 32
	case "kelvin":
		return valueInCelsius + 273.15
	}
	return 0.0
}
