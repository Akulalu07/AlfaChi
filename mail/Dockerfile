FROM golang:1.21-alpine

WORKDIR /app

COPY main.go .

RUN go mod init mail && go mod tidy

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o mail .

CMD ["./mail"]