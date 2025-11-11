FROM golang:1.25.4-trixie

WORKDIR /app

COPY main.go .

RUN go mod init mail && go mod tidy

RUN GOEXPERIMENT=greenteagc go build -o mail .

RUN chmod +x mail

CMD ["./mail"]