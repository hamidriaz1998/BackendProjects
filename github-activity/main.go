package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

type GithubActivity struct {
	Type string `json:"type"`
	Repo struct {
		Name string `json:"name"`
	}
	Payload struct {
		Commits []struct {
			Message string `json:"message"`
		} `json:"commits"`
		Action  string `json:"action"`
		Ref     string `json:"ref"`
		RefType string `json:"ref_type"`
	} `json:"payload"`
}

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
	err = displayActivity(body, os.Args[1])
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

func displayActivity(jsonData []byte, username string) error {
	var events []GithubActivity
	err := json.Unmarshal(jsonData, &events)
	if err != nil {
		return err
	}
	if len(events) == 0 {
		fmt.Println("No recent activity found.")
		return nil
	}
	fmt.Printf("%s's recent activity(s)\n", username)
	for _, event := range events {
		finalString := ""
		name := event.Repo.Name
		switch event.Type {
		case "PushEvent":
			commitCount := len(event.Payload.Commits)
			finalString = fmt.Sprintf("Pushed %d commit(s) to %s", commitCount, name)
		case "IssuesEvent":
			action := event.Payload.Action
			action = strings.ToUpper(string(action[0])) + action[1:]
			finalString = fmt.Sprintf("%s an issue in %s", action, name)
		case "WatchEvent":
			finalString = fmt.Sprintf("Starred %s", name)
		case "ForkEvent":
			finalString = fmt.Sprintf("Forked %s", name)
		case "CreateEvent":
			finalString = fmt.Sprintf("Created %v in %s", event.Payload.RefType, name)
		default:
			finalString = fmt.Sprintf("Performed event of type %s in %s", event.Type, name)
		}
		fmt.Println("- ", finalString)
	}
	return nil
}
