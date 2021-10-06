FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y \
        python3 && \
    rm -rf /var/lib/apt/lists/*

COPY prepare_data.py /bin/prepare_data
COPY run_tool.sh /bin/run_tool
COPY tool.py /bin/tool.py
