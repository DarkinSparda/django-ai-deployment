# Docker Quick Reference

## Installation

```bash
# Run the installation script
bash install-docker.sh

# Or install manually (see SETUP_GUIDE.md)
```

## Essential Docker Commands

### Images (Blueprints)
```bash
# List all images
docker images

# Remove an image
docker rmi <image-name>

# Remove all unused images
docker image prune -a
```

### Containers (Running Instances)
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container-id>

# Remove a container
docker rm <container-id>

# Remove all stopped containers
docker container prune
```

### Building & Running
```bash
# Build an image
docker build -t my-app .

# Run a container
docker run -p 8000:8000 my-app

# Run in background
docker run -d -p 8000:8000 my-app

# Run with environment variables
docker run -e DEBUG=True -p 8000:8000 my-app
```

### Logs & Debugging
```bash
# View logs
docker logs <container-id>

# Follow logs (real-time)
docker logs -f <container-id>

# Enter a running container
docker exec -it <container-id> bash

# Inspect container
docker inspect <container-id>
```

## Docker Compose Commands

### Basic Operations
```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Rebuild and start
docker compose up --build

# Stop services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```

### Viewing & Managing
```bash
# View logs
docker compose logs

# Follow logs for specific service
docker compose logs -f web

# List running services
docker compose ps

# Restart a service
docker compose restart web
```

### Executing Commands
```bash
# Run a command in a service
docker compose exec web python manage.py migrate

# Create Django superuser
docker compose exec web python manage.py createsuperuser

# Open a shell in container
docker compose exec web bash

# Run a one-off command
docker compose run web python manage.py shell
```

## Common Tasks for This Project

### Local Development
```bash
# Start everything
docker compose up --build

# View Django logs
docker compose logs -f web

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic

# Open Django shell
docker compose exec web python manage.py shell

# Stop everything
docker compose down
```

### Cleaning Up
```bash
# Stop and remove everything
docker compose down -v

# Remove all unused containers, networks, images
docker system prune -a

# See disk usage
docker system df
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change the port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Permission Denied
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker

# Or just log out and back in
```

### Container Won't Start
```bash
# Check logs
docker compose logs web

# Check if database is ready
docker compose logs db

# Rebuild from scratch
docker compose down -v
docker compose up --build
```

### Out of Disk Space
```bash
# See what's using space
docker system df

# Clean up
docker system prune -a
docker volume prune
```

## Understanding the Workflow

### Build Process
```
Dockerfile → Build → Image → Run → Container
```

### With Docker Compose
```
docker-compose.yml → Orchestrates → Multiple Containers
                                    ├── web (Django)
                                    └── db (PostgreSQL)
```

### Environment Variables
```
.env → Docker Compose → Containers
```

## Best Practices

1. **Always use `.dockerignore`** - Keeps images small
2. **Use volumes for data** - Persists data between restarts
3. **Tag your images** - `docker build -t myapp:v1.0 .`
4. **Clean up regularly** - `docker system prune`
5. **Check logs often** - `docker compose logs -f`
6. **Use multi-stage builds** - For smaller production images
7. **Don't run as root** - Create a user in Dockerfile (advanced)

## Quick Debugging Checklist

Container won't start?
- [ ] Check logs: `docker compose logs`
- [ ] Verify .env file exists
- [ ] Check port availability: `lsof -i :8000`
- [ ] Rebuild: `docker compose up --build`

Database connection failed?
- [ ] Is db container running? `docker compose ps`
- [ ] Check DATABASE_URL environment variable
- [ ] Check db logs: `docker compose logs db`

Changes not reflected?
- [ ] Did you rebuild? `docker compose up --build`
- [ ] Are you mounting volumes correctly?
- [ ] Check .dockerignore isn't excluding your files

## Resources

- Official Docker Docs: https://docs.docker.com
- Docker Compose Docs: https://docs.docker.com/compose/
- Docker Hub (images): https://hub.docker.com
- Our Setup Guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Pro Tips

```bash
# Clean everything and start fresh
docker compose down -v && docker system prune -a && docker compose up --build

# Watch logs from all services
docker compose logs -f

# Execute multiple commands
docker compose exec web bash -c "python manage.py migrate && python manage.py createsuperuser"

# Copy files from container
docker compose cp web:/app/db.sqlite3 ./backup.db

# Copy files to container
docker compose cp ./data.json web:/app/data.json
```
