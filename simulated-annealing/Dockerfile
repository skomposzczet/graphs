FROM rust:alpine3.18
RUN apk update && apk upgrade --no-cache && \
    apk add musl-dev && \
    adduser -D user
USER user
WORKDIR /app
CMD ["sh"]
