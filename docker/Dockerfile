FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Pacific/Brisbane

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata \
        ca-certificates \
        gnupg \
        software-properties-common \
        dirmngr \
        wget \
        curl \
        git \
        bc \
        cmake \
        build-essential \
        python3-pip \
        gdal-bin \
        libgdal-dev \
        pdal \
        grass-core \
        grass-dev \
        libssl-dev \
        libssh2-1-dev \
        libcurl4-openssl-dev \
        libxml2-dev && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
        ninja \
        boto3 \
        geopandas \
        rasterio \
        pyproj \
        awscli \
        laspy

