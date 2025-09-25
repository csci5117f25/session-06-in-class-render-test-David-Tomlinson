# Render-test
A basic website -- just enough to test out hooking things up to render, and not much more.

We will go over steps in lecture. You should fill out the following:

## What steps do I need to do when I download this repo to get it running?

1. Install pipenv: `pip install pipenv`
2. Install dependencies: `pipenv install`
3. Activate virtual environment: `pipenv shell`

## What commands starts the server?

**Development server:**
```bash
python server.py
```

**Production server (for Render):**
```bash
gunicorn server:app
```

## Database Setup

This app now includes PostgreSQL database connectivity with connection pooling.

### Local Development:
1. Create a `.env` file (copy from `.env.example`)
2. Add your database connection string to `.env`:
   ```
   DATABASE_URL=postgresql://username:password@hostname:port/database_name
   ```
3. Install dependencies: `pipenv install`
4. Run the app: `python server.py`

### Database Schema:
You'll need to create a `person` table in your database:
```sql
CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

### API Endpoints:
- `GET /` - Main page
- `GET /people` - List all people (with pagination)
- `POST /people` - Add a new person
- `GET /health` - Health check

## Render Deployment

This repository is now configured for Render deployment with the following files:
- `render.yaml` - Render service configuration
- `requirements.txt` - Python dependencies (generated from Pipfile)
- `database.py` - Database connection pooling and helper functions

### Deploy to Render:
1. Push this repository to GitHub
2. Connect your GitHub repository to Render
3. Add a PostgreSQL database in Render
4. Set the `DATABASE_URL` environment variable in Render
5. Render will automatically detect the `render.yaml` configuration
6. The app will be deployed with gunicorn as the production server