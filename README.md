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

## Render Deployment

This repository is now configured for Render deployment with the following files:
- `render.yaml` - Render service configuration
- `requirements.txt` - Python dependencies (generated from Pipfile)

### Deploy to Render:
1. Push this repository to GitHub
2. Connect your GitHub repository to Render
3. Render will automatically detect the `render.yaml` configuration
4. The app will be deployed with gunicorn as the production server