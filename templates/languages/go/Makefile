.PHONY: fmt lint test build

fmt:
	gofmt -w .
	go vet ./...

lint:
	golangci-lint run

test:
	go test ./... -race -cover

build:
	go build ./...
