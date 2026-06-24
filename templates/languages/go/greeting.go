package main

import "fmt"

// Greet returns a greeting for name. Replace with your own first behavior.
func Greet(name string) string {
	if name == "" {
		name = "stranger"
	}
	return fmt.Sprintf("Hello, %s!", name)
}
