#!/bin/bash

# Use this script to build, tag, and publish the Docker image from your local machine.
set -e

docker build -t docs-v2 .

docker tag docs-v2:latest ghcr.io/hololinked-dev/docs-v2:latest

docker push ghcr.io/hololinked-dev/docs-v2:latest

echo "Docker image built and pushed successfully."