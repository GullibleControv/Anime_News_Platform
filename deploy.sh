#!/bin/bash
# =================================================================
# Deployment Script for Anime News Platform
# =================================================================
# Run this script on your server to deploy the application
# Usage: ./deploy.sh
# =================================================================

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating from .env.production template..."
    cp .env.production .env
    echo -e "${YELLOW}Please edit .env with your actual values, then run this script again.${NC}"
    exit 1
fi

# Step 2: Pull latest code (if using git)
if [ -d .git ]; then
    echo "📥 Pulling latest code..."
    git pull origin main
fi

# Step 3: Build and start containers
echo "🔨 Building Docker images..."
docker compose -f docker-compose.prod.yml build

echo "🚀 Starting containers..."
docker compose -f docker-compose.prod.yml up -d

# Step 4: Wait for database
echo "⏳ Waiting for database..."
sleep 10

# Step 5: Run migrations
echo "📦 Running database migrations..."
docker exec anime-news-web python manage.py migrate --noinput

# Step 6: Collect static files
echo "📁 Collecting static files..."
docker exec anime-news-web python manage.py collectstatic --noinput

# Step 7: Show status
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "🌐 Your site should be available at:"
echo "   http://YOUR_SERVER_IP"
echo "   https://your-domain.com (after SSL setup)"
