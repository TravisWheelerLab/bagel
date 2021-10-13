FROM debian:bullseye-slim AS transmark-rocplot 

ARG easel_version=0.48

RUN apt-get update && apt-get -y install \
    autoconf \
    build-essential

ADD https://github.com/EddyRivasLab/easel/archive/easel-${easel_version}.tar.gz easel.tar.gz
RUN tar xf easel.tar.gz
WORKDIR /easel-easel-${easel_version}
RUN autoconf && \
    ./configure && \
    make

RUN mkdir /transmark-rocplot 
WORKDIR /transmark-rocplot
COPY Makefile ./
COPY transmark-rocplot.c ./

RUN make ESLDIR=/easel-easel-${easel_version} 

# -----------------------------------------------------------------------------

FROM debian:bullseye-slim

COPY --from=transmark-rocplot /transmark-rocplot/transmark-rocplot ./
CMD ./transmark-rocplot -h

