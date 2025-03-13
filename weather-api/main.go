package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("Warning: .env file not found")
	}

	redisUrl := os.Getenv("REDIS_URL")
	if redisUrl == "" {
		log.Fatalln("REDIS_URL env variable is required")
		log.Fatalln("Exiting")
		os.Exit(1)
	}

	apiKey := os.Getenv("API_KEY")
	if apiKey == "" {
		log.Fatalln("API_KEY env variable is required")
		log.Fatalln("Exiting")
		os.Exit(1)
	}

	cache, err := NewCache(redisUrl)
	if err != nil {
		log.Fatalln("Connection to Redis failed: ", err)
		os.Exit(1)
	}
	apiClient := NewApiClient(apiKey, cache)

	http.HandleFunc("/weather", func(w http.ResponseWriter, r *http.Request) {
		location := r.URL.Query().Get("location")
		if location == "" {
			http.Error(w, "Location parameter is required", http.StatusBadRequest)
			return
		}

		data, err := apiClient.GetData(location)
		if err != nil {
			log.Fatalln(err)
			http.Error(w, "Error fetching weather data: "+err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(data)
	})
	
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request){
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
		w.Write([]byte("\n"))
		w.Write([]byte("Server is running"))
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Println("Server starting on port:", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
