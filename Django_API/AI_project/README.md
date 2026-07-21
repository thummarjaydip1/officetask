# Fruit Pro Django Project

A Django project for managing fruit-related operations.

## Project Structure

```
fruit_pro/
├── manage.py
├── fruit_pro/              # Project settings and configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── fruit_app/              # Main application
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded media files
├── requirements.txt        # Project dependencies
└── .gitignore             # Git ignore rules
```

## Installation

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

## Usage

- **Admin panel:** `http://127.0.0.1:8000/admin/`
- **API routes:** `http://127.0.0.1:8000/api/`

## Configuration

- Static files URL: `/static/`
- Media files URL: `/media/`
- Database: SQLite (`db.sqlite3`)

## Commands

```bash
# Create a new app
python manage.py startapp <app_name>

# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Start development server
python manage.py runserver
```

## Requirements

- Python 3.8+
- Django 6.0+

## License

MIT License
