FROM golang:1.23.2-alpine

WORKDIR /app

RUN go install github.com/air-verse/air@latest

COPY go.mod go.sum ./
RUN go mod download
COPY . .

ENV PORT=3000

EXPOSE $PORT

CMD ["air"]
