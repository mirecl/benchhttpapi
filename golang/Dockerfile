FROM golang:latest as builder
LABEL maintainer="Grazhdankov"
WORKDIR /
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main

######## Start a new stage #######
FROM alpine:latest  
RUN apk --no-cache add ca-certificates \
    && apk add --no-cache tzdata
ENV TZ=Europe/Moscow
WORKDIR /
COPY --from=builder /main .
CMD ["./main"] 