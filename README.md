# Team Retrospectives Tool

A web-based tool for conducting team retrospectives in tech companies. Built with Django backend and Vue.js frontend.

## Project Structure

```
retrospectives/
├── backend/                 # Django backend
│   ├── api/                # Django API app
│   ├── retrospectives/     # Django project settings
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies (development)
│   └── requirements-prod.txt # Python dependencies (production)
├── frontend/               # Vue.js frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml      # Development environment
└── README.md
```

## Features (Planned)

- Create and manage retrospective sessions
- Real-time collaboration
- Template-based retrospective formats
- Action item tracking
- Team member management
- Historical data and insights

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Note**: The development setup uses SQLite database. For production, use `requirements-prod.txt` which includes PostgreSQL support.

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Development

This project uses:
- **Backend**: Python 3.8+, Django 4.2, Django REST Framework, JWT Authentication
- **Frontend**: Vue 3, Vite, TypeScript, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)

## API Endpoints

- `/api/users/` - User management
- `/api/teams/` - Team management
- `/api/retrospectives/` - Retrospective sessions
- `/api/retrospective-items/` - Individual retrospective items
- `/api/action-items/` - Action items tracking
- `/api/auth/` - JWT authentication endpoints

## Production Deployment

For production deployment:
1. Use `pip install -r requirements-prod.txt`
2. Configure PostgreSQL database in settings
3. Set environment variables for SECRET_KEY, DEBUG, etc.
4. Use gunicorn as WSGI server
