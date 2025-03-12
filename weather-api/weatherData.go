package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

type WeatherResponse struct {
	Latitude        float64 `json:"latitude" redis:"latitude"`
	Longitude       float64 `json:"longitude" redis:"longitude"`
	ResolvedAddress string  `json:"resolvedAddress" redis:"resolved_address"`
	Address         string  `json:"address" redis:"address"`
	Timezone        string  `json:"timezone" redis:"timezone"`
	Days            []struct {
		Datetime      string  `json:"datetime" redis:"datetime"`
		DatetimeEpoch int     `json:"datetimeEpoch" redis:"datetime_epoch"`
		Tempmax       float64 `json:"tempmax" redis:"tempmax"`
		Tempmin       float64 `json:"tempmin" redis:"tempmin"`
		Temp          float64 `json:"temp" redis:"temp"`
		Sunrise       string  `json:"sunrise" redis:"sunrise"`
		SunriseEpoch  int     `json:"sunriseEpoch" redis:"sunrise_epoch"`
		Sunset        string  `json:"sunset" redis:"sunset"`
		SunsetEpoch   int     `json:"sunsetEpoch" redis:"sunset_epoch"`
		Moonphase     float64 `json:"moonphase" redis:"moonphase"`
		Description   string  `json:"description" redis:"description"`
		Icon          string  `json:"icon" redis:"icon"`
		Source        string  `json:"source" redis:"source"`
		Hours         []struct {
			Datetime      string  `json:"datetime" redis:"datetime"`
			DatetimeEpoch int     `json:"datetimeEpoch" redis:"datetime_epoch"`
			Temp          float64 `json:"temp" redis:"temp"`
			Feelslike     float64 `json:"feelslike" redis:"feelslike"`
			Icon          string  `json:"icon" redis:"icon"`
		} `json:"hours" redis:"hours"`
	} `json:"days" redis:"days"`
}

type ApiClient struct {
	Url    string
	Params string
	Cache  *Cache
}

const URL string = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
const PARAMS string = "?unitGroup=metric&include=hours&contentType=json&key="
const CACHE_TTL = time.Hour * 2

func NewApiClient(apiKey string, cache *Cache) *ApiClient {
	return &ApiClient{
		Cache:  cache,
		Params: PARAMS + apiKey,
		Url:    URL,
	}
}

func (client *ApiClient) GetData(location string) (*WeatherResponse, error) {
	// Get data from cache

	ctx := context.Background()
	cacheKey := "weather:" + location

	// try to get data
	var wData WeatherResponse
	found, err := client.Cache.Get(ctx, cacheKey, &wData)
	if err != nil {
		log.Printf("Error reading from cache: %v", err)
	}

	if found {
		log.Printf("Cache hit for location: %s", location)
		return &wData, nil
	}

	// Get data from api
	log.Printf("Cache miss for location: %s, fetching from API", location)
	url := fmt.Sprint(client.Url, location, client.Params)
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("API returned status code: %d", response.StatusCode)
	}
	var wResp WeatherResponse
	if err := json.NewDecoder(response.Body).Decode(&wResp); err != nil {
		log.Fatalln(err)
	}

	if err := client.Cache.Set(ctx, cacheKey, wResp, CACHE_TTL); err != nil {
		log.Printf("Failed to cache data: %v", err)
	}

	return &wResp, nil
}
