Commands for running in Ubuntu:

# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Check running containers
docker ps

# Test the healthcheck endpoint
curl http://localhost:9000/healthcheck

# Access PostgreSQL
docker-compose exec postgres psql -U flaskuser -d flaskdb

# Access Redis CLI
docker-compose exec redis redis-cli

git config --global user.name "alexrothos"
git config --global user.email "alexrothos@gmail.com"