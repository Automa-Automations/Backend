ARG GO_VERSION=1.22
FROM golang:${GO_VERSION}-bookworm as builder

WORKDIR /usr/src/app
COPY <<service_dir>>/go.mod <<service_dir>>/go.sum ./
RUN go mod download && go mod verify
COPY <<service_dir>>/. .
RUN go build -v -o /run-app .

EXPOSE 3000
EXPOSE 3001


FROM debian:bookworm

COPY --from=builder /run-app /usr/local/bin/
CMD ["run-app", "server"]
