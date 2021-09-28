FROM debian:bullseye-slim

VOLUME /data

RUN apt-get update && \
    apt-get install -y \
        python3 && \
    rm -rf /var/lib/apt/lists/*

COPY tool.py /bin/psss-benchmark

