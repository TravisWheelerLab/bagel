FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y \
        python3 && \
    rm -rf /var/lib/apt/lists/*

COPY tool.py /bin/
COPY wrapper.sh /bin/psss-benchmark

