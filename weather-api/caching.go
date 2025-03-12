package main

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

type Cache struct {
	Client *redis.Client
}

func NewCache(connectionStr string) *Cache {
	opt, err := redis.ParseURL(connectionStr)
	if err != nil {
		log.Fatalln(err)
	}
	client := redis.NewClient(opt)
	return &Cache{
		Client: client,
	}
}

func (c *Cache) Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	jsonData, err := json.Marshal(value)
	if err != nil {
		return err
	}

	return c.Client.Set(ctx, key, jsonData, expiration).Err()
}

func (c *Cache) Get(ctx context.Context, key string, dest interface{}) (bool, error) {
	val, err := c.Client.Get(ctx, key).Result()
	if err == redis.Nil {
		// Key does not exist
		return false, nil
	} else if err != nil {
		return false, err
	}

	if err := json.Unmarshal([]byte(val), &dest); err != nil {
		return false, err
	}
	
	return true, nil
}

func (c *Cache) Delete(ctx context.Context, key string) error{
	return c.Client.Del(ctx, key).Err()
}
