ARG GO_VERSION=1.22
FROM golang:${GO_VERSION}-bookworm as builder

WORKDIR /usr/src/app
COPY services/lala123SQS/go.mod services/lala123SQS/go.sum ./
RUN go mod download && go mod verify
COPY services/lala123SQS/. .
RUN go build -v -o /run-app .

EXPOSE 3000
EXPOSE 3001


FROM debian:bookworm

COPY --from=builder /run-app /usr/local/bin/
CMD ["run-app", "server"]
