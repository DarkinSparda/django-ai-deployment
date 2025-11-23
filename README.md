# Django AI Blog Generator

An AI-powered blog generator using Django, Google Gemini, and AssemblyAI.

## Quick Start

### Local Development (Without Docker)
```bash
cd backend/ai_blog_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Local Development (With Docker)
```bash
docker compose up --build
```
Visit http://localhost:8000

### Production Deployment (Northflank)
See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## Project Structure

```
.
├── backend/
│   ├── ai_blog_app/           # Django project
│   │   ├── ai_blog_app/       # Settings
│   │   ├── blog_generator/    # Blog app
│   │   ├── api/               # API endpoints
│   │   └── manage.py
│   ├── Dockerfile             # Docker build instructions
│   └── .dockerignore          # Files to exclude from Docker
├── frontend/
│   └── templates/             # HTML templates
├── docker-compose.yml         # Local Docker setup
├── .env                       # Environment variables (not in git)
└── SETUP_GUIDE.md            # Complete deployment guide

## Features

- AI blog generation using Google Gemini
- Audio transcription with AssemblyAI
- REST API with JWT authentication
- Swagger API documentation
- Docker containerization
- Ready for Northflank deployment

## Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database (for production)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# API Keys
GEMINI_API_KEY=your-gemini-key
ASSEMBLY_AI_API=your-assemblyai-key
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **AI**: Google Gemini, AssemblyAI
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Deployment**: Docker, Northflank
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise

## Learn More

- [Docker & Deployment Guide](SETUP_GUIDE.md) - Complete tutorial from zero to production
- [Northflank Config](.northflank.yml) - Infrastructure as code

## License

MIT
