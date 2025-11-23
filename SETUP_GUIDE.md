# Docker & Northflank Deployment Guide

This guide will teach you Docker from zero to successfully deploying on Northflank.

---

## Part 1: Understanding What We Built

### Files We Created

1. **[backend/Dockerfile](backend/Dockerfile)** - The recipe to build your Django app into a Docker image
2. **[docker-compose.yml](docker-compose.yml)** - Orchestrates multiple containers (Django + PostgreSQL) for local testing
3. **[backend/.dockerignore](backend/.dockerignore)** - Tells Docker what files to ignore (keeps image small)
4. **Updated [backend/ai_blog_app/ai_blog_app/settings.py](backend/ai_blog_app/ai_blog_app/settings.py)** - Now supports environment variables for production
5. **Updated [backend/ai_blog_app/requirements.txt](backend/ai_blog_app/requirements.txt)** - Added production dependencies

### What Each File Does

#### Dockerfile Explained
```dockerfile
FROM python:3.12-slim           # Start with Python 3.12
WORKDIR /app                     # Set working directory
COPY requirements.txt /app/      # Copy dependencies list
RUN pip install -r requirements.txt  # Install dependencies
COPY ai_blog_app/ /app/         # Copy your code
EXPOSE 8000                      # Tell Docker we use port 8000
CMD gunicorn ...                 # Start production server
```

#### docker-compose.yml Explained
```yaml
services:
  db:                            # PostgreSQL database
    image: postgres:16-alpine    # Use official PostgreSQL image

  web:                           # Your Django app
    build: ./backend             # Build from our Dockerfile
    depends_on: db               # Wait for database first
```

---

## Part 2: Installing Docker

### On Ubuntu/Debian Linux:

```bash
# Update package index
sudo apt-get update

# Install required packages
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Apply group changes (or just log out and log back in)
newgrp docker

# Verify installation
docker --version
docker compose version
```

---

## Part 3: Testing Docker Locally

Once Docker is installed, test our setup:

```bash
# Navigate to project root
cd /home/abdullah-mohammed/Desktop/personal_projects/django-ai-deployment

# Build and start containers
docker compose up --build

# This will:
# 1. Build your Django app into a Docker image
# 2. Download PostgreSQL image
# 3. Start both containers
# 4. Run migrations
# 5. Start the server on http://localhost:8000
```

### Common Docker Commands

```bash
# See running containers
docker ps

# See all containers (including stopped)
docker ps -a

# View logs
docker compose logs -f web

# Stop containers
docker compose down

# Rebuild after code changes
docker compose up --build

# Remove everything (including volumes)
docker compose down -v

# Execute commands inside container
docker compose exec web python manage.py createsuperuser
```

---

## Part 4: Deploying to Northflank

### What is Northflank?
Northflank is a cloud platform that runs Docker containers. It's like having a server that automatically runs your Docker image.

### Prerequisites
1. Create a Northflank account: https://northflank.com
2. Connect your GitHub/GitLab account (or use Northflank's Git)
3. Push your code to a Git repository

### Deployment Steps

#### Step 1: Push to GitHub
```bash
# Make sure you're in project root
cd /home/abdullah-mohammed/Desktop/personal_projects/django-ai-deployment

# Add all files
git add .

# Commit
git commit -m "Add Docker configuration for deployment"

# Push to GitHub
git push origin main
```

#### Step 2: Create Northflank Project
1. Log into Northflank
2. Click "Create Project"
3. Name it "ai-blog-app"

#### Step 3: Create PostgreSQL Database
1. In your project, click "Add Service"
2. Select "Database"
3. Choose "PostgreSQL"
4. Select version 16
5. Choose a plan (start with the free tier)
6. Name it "ai-blog-db"
7. Click "Create Database"
8. Wait for it to be ready
9. Note the connection details (Northflank provides these automatically)

#### Step 4: Deploy Django App
1. Click "Add Service"
2. Select "Combined Service" (build + deployment)
3. Connect your Git repository
4. Select the repository with your code
5. Configure:
   - **Name**: `ai-blog-api`
   - **Build Context**: `backend`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Port**: `8000`

#### Step 5: Add Environment Variables
In the service settings, add these environment variables:

```
DEBUG=False
SECRET_KEY=<generate-a-new-secret-key>
ALLOWED_HOSTS=*.northflank.app,yourdomain.com
DATABASE_URL=<copy from database service>
GEMINI_API_KEY=<your-gemini-api-key>
ASSEMBLY_AI_API=<your-assembly-ai-key>
```

To generate a new SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Step 6: Deploy
1. Click "Deploy Service"
2. Wait for build to complete
3. Access your app at the provided URL

---

## Part 5: Useful Northflank Features

### View Logs
- Go to your service
- Click "Logs" tab
- See real-time application logs

### Scale Your App
- Go to service settings
- Adjust replicas (number of containers)
- Adjust resources (CPU/RAM)

### Custom Domain
1. Go to service settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Auto-Deploy on Push
- Northflank automatically rebuilds when you push to your Git repository
- You can disable this in settings if needed

---

## Part 6: Troubleshooting

### Local Docker Issues

**Problem**: Port 8000 already in use
```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill it
kill -9 <PID>
```

**Problem**: Permission denied
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Problem**: Database connection failed
- Make sure both containers are running: `docker ps`
- Check logs: `docker compose logs db`

### Northflank Issues

**Problem**: Build fails
- Check build logs in Northflank dashboard
- Verify Dockerfile path is correct: `backend/Dockerfile`
- Ensure requirements.txt is present

**Problem**: App crashes on startup
- Check application logs
- Verify all environment variables are set
- Check DATABASE_URL is correct

**Problem**: Static files not loading
- Ensure WhiteNoise is in MIDDLEWARE
- Run collectstatic during deployment (already in our Dockerfile CMD)

---

## Part 7: Best Practices

### Security
1. Never commit `.env` files (already in `.gitignore`)
2. Use strong SECRET_KEY in production
3. Set DEBUG=False in production
4. Use environment variables for secrets

### Performance
1. Use PostgreSQL in production (not SQLite)
2. Use gunicorn with multiple workers
3. Enable WhiteNoise for static files
4. Use CDN for media files (for larger apps)

### Monitoring
1. Check logs regularly
2. Set up alerts in Northflank
3. Monitor database size
4. Track API usage

---

## Part 8: Next Steps

After successful deployment:

1. **Create superuser**
   ```bash
   # On Northflank, use the console feature
   python manage.py createsuperuser
   ```

2. **Test API endpoints**
   - Visit `https://your-app.northflank.app/api/`
   - Check Swagger docs at `/api/schema/swagger-ui/`

3. **Set up CI/CD**
   - Northflank auto-deploys on git push
   - Add GitHub Actions for testing

4. **Monitor costs**
   - Check Northflank billing dashboard
   - Optimize resource usage

---

## Quick Reference

### Local Development
```bash
docker compose up              # Start
docker compose down            # Stop
docker compose logs -f web     # View logs
docker compose exec web bash   # Enter container
```

### Production (Northflank)
- Code push → Auto deploy
- View logs in dashboard
- Scale in service settings
- Database backups automatic

---

## Questions?

### What is a Docker Image?
A packaged version of your app with all dependencies. Like a ZIP file that contains everything needed to run your app.

### What is a Container?
A running instance of an image. You can have multiple containers from one image.

### Why PostgreSQL instead of SQLite?
SQLite is file-based and doesn't work well with multiple containers. PostgreSQL is a proper database server.

### Why Gunicorn?
Django's development server (`runserver`) is not production-ready. Gunicorn is a production WSGI server that handles multiple requests efficiently.

### What is WhiteNoise?
A Python library that serves static files (CSS, JS, images) efficiently without needing nginx.

---

Good luck with your deployment! 🚀
