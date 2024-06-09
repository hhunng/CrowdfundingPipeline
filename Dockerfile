# Use the latest version of the Ubuntu distribution as the base image
FROM ubuntu:latest

# Update the package lists and install the necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app
