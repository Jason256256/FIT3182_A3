#!/bin/bash

echo "Starting containerized big data infrastructure (Kafka & MongoDB)..."
# Launch containers relative to where this script lives
docker-compose -f ../config/docker-compose.yml up -d

echo "Waiting 10 seconds for Kafka broker initialization..."
sleep 10

echo "Creating Apache Kafka traffic event streaming topic..."
docker exec -it $(docker ps -q -f name=kafka) kafka-topics --create --topic awas-traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 2>/dev/null || echo "Topic already exists."

echo "Infrastructure is running successfully!"