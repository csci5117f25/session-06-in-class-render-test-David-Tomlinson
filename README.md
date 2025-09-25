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
You'll need to create a `guestbook` table in your database:
```sql
CREATE TABLE guestbook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Features:
- **Guestbook Form**: Users can sign the guestbook with their name and message
- **Entry Display**: Shows all guestbook entries with timestamps
- **Pagination**: Displays 10 entries per page with navigation
- **Input Validation**: Name (100 chars max), Message (500 chars max)
- **Flash Messages**: Success/error feedback for form submissions
- **Responsive Design**: Works on desktop and mobile devices

### Routes:
- `GET /` - Main page with link to guestbook
- `GET /guestbook` - Display guestbook with form and entries
- `POST /guestbook` - Add new guestbook entry
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