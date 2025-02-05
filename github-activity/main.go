package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Invalid number of arguments")
		fmt.Printf("Usage: %s <username>\n", os.Args[0])
		os.Exit(1)
	}

	body, err := getGithubUserActivity(os.Args[1])
	if err != nil {
		fmt.Printf("Error fetchting user activity: %s\n", err)
	}
	err = displayActivity(body)
	if err != nil {
		fmt.Printf("Error displaying activity: %s", err)
	}
}

func getGithubUserActivity(username string) ([]byte, error) {
	url := fmt.Sprintf("https://api.github.com/users/%s/events", username)
	res, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	body, err := io.ReadAll(res.Body)
	if err != nil {
		fmt.Printf("Error Reading response body: %s\n", err)
		os.Exit(1)
	}
	return body, nil
}

func displayActivity(jsonData []byte) error {
	var events []map[string]any
	err := json.Unmarshal(jsonData, &events)
	if err != nil {
		return err
	}
	if len(events) == 0 {
		fmt.Println("No recent activity found.")
		return nil
	}
	for _, event := range events {
		finalString := ""
		eventType := event["type"].(string)
		payload, ok := event["payload"].(map[string]any)
		if !ok {
			finalString = fmt.Sprintf("Performed event of type %s", eventType)
			fmt.Println(finalString)
			continue
		}
		repo, ok := event["repo"].(map[string]any)
		if !ok {
			finalString = fmt.Sprintf("Performed event of type %s", eventType)
			fmt.Println(finalString)
			continue
		}
		name, ok := repo["name"].(string)
		if !ok {
			finalString = fmt.Sprintf("Performed event of type %s", eventType)
			fmt.Println(finalString)
			continue
		}
		switch eventType {
		case "PushEvent":
			commits, ok := payload["commits"].([]any)
			if !ok {
				finalString = fmt.Sprintf("Performed event of type %s", eventType)
				fmt.Println(finalString)
				continue
			}
			commitCount := len(commits)
			finalString = fmt.Sprintf("Pushed %d commit(s) to %s", commitCount, name)
		case "IssuesEvent":
			action, ok := payload["action"].(string)
			if !ok {
				finalString = fmt.Sprintf("Performed event of type %s", eventType)
				fmt.Println(finalString)
				continue
			}
			action = strings.ToUpper(string(action[0])) + action[1:]
			finalString = fmt.Sprintf("%s an issue in %s", action, name)
		case "WatchEvent":
			finalString = fmt.Sprintf("Starred %s", name)
		case "ForkEvent":
			finalString = fmt.Sprintf("Forked %s", name)
		case "CreateEvent":
			finalString = fmt.Sprintf("Created %v in %s", payload["ref_type"], name)
		default:
			finalString = fmt.Sprintf("Performed event of type %s in %s", eventType, name)
		}
		fmt.Println("- ", finalString)
	}
	return nil
}
