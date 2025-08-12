#!/bin/bash
set -e

# Deployment script for Turbit APIs
echo "Starting deployment of Turbit APIs..."

# Check if required files exist
if [ ! -f ".env" ]; then
    echo "Error: .env file not found"
    exit 1
fi

if [ ! -f "init-mongo.js" ]; then
    echo "Error: init-mongo.js file not found"
    exit 1
fi

if [ ! -d "mongoconnector" ]; then
    echo "Error: mongoconnector directory not found"
    exit 1
fi

# Stop existing containers if running
echo "🛑 Stopping existing containers..."
docker-compose down -v || true

#pull from repo
echo "Pulling fresh from GIT..."
git pull

# Remove existing images to force rebuild
echo "Cleaning up old images..."
docker image prune -f
docker-compose build --no-cache

# Start the services
echo "Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Display running services
echo "Service status:"
docker-compose ps

# Display service URLs
echo ""
echo "Service URLs:"
echo "  Task 1 API: http://localhost:6000"
echo "  Task 2 API: http://localhost:7000"
echo "  MongoDB: mongodb://localhost:27017"
echo ""
echo "Deployment complete!"

# Show logs for troubleshooting if needed
echo "To view logs, run:"
echo "  docker-compose logs -f"
echo ""
echo "🔧 To stop services, run:"
echo "  docker-compose down"