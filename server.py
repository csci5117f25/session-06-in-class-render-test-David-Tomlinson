import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os
from datetime import datetime
from database import setup, add_guestbook_entry, get_guestbook_entries, get_guestbook_count

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# Initialize database connection pool
def initialize_database():
    if 'DATABASE_URL' in os.environ:
        try:
            setup()
            print("Database connection pool initialized successfully")
        except Exception as e:
            print(f"Failed to initialize database: {e}")
    else:
        print("DATABASE_URL not found in environment variables")

# Initialize database on app startup
initialize_database()

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    # Track session data - visits, preferences, etc.
    if 'visit_count' not in session:
        session['visit_count'] = 0
    session['visit_count'] += 1
    
    # Store last visit timestamp
    session['last_visit'] = datetime.now().isoformat()
    
    # Remember user's preferred name if provided
    if name:
        session['preferred_name'] = name
    
    # Pass user session data to template
    user_session = session.get('user')
    pretty = json.dumps(user_session, indent=4) if user_session else None
    
    return render_template('hello.html', name=name, session=user_session, pretty=pretty)

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    # Track guestbook visits in session
    if 'guestbook_visits' not in session:
        session['guestbook_visits'] = 0
    session['guestbook_visits'] += 1
    
    # Check if database is available
    if 'DATABASE_URL' not in os.environ:
        flash('Database not configured. Please set DATABASE_URL environment variable.', 'error')
        return render_template('guestbook.html', 
                             entries=[], 
                             current_page=0, 
                             total_pages=0,
)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()
        
        if not name or not message:
            flash('Both name and message are required!', 'error')
            return redirect(url_for('guestbook'))
        
        if len(name) > 100:
            flash('Name must be 100 characters or less!', 'error')
            return redirect(url_for('guestbook'))
            
        if len(message) > 500:
            flash('Message must be 500 characters or less!', 'error')
            return redirect(url_for('guestbook'))
        
        try:
            add_guestbook_entry(name, message)
            flash('Thank you for signing the guestbook!', 'success')
            return redirect(url_for('guestbook'))
        except Exception as e:
            flash(f'Error adding entry: {str(e)}', 'error')
            return redirect(url_for('guestbook'))
    
    # GET request - display guestbook
    try:
        page = int(request.args.get('page', 0))
        entries_per_page = 10
        
        entries = get_guestbook_entries(page=page, entries_per_page=entries_per_page)
        total_entries = get_guestbook_count()
        total_pages = (total_entries + entries_per_page - 1) // entries_per_page
        
        return render_template('guestbook.html', 
                             entries=entries, 
                             current_page=page, 
                             total_pages=total_pages,
)
    except Exception as e:
        flash(f'Error loading guestbook: {str(e)}', 'error')
        return render_template('guestbook.html', 
                             entries=[], 
                             current_page=0, 
                             total_pages=0,
)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'DATABASE_URL' in os.environ})

#AUTH0 ROUTES
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("hello"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    return render_template("hello.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))