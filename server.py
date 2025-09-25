from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from database import setup, add_guestbook_entry, get_guestbook_entries, get_guestbook_count

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

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
    return render_template('hello.html', name=name)

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    # Check if database is available
    if 'DATABASE_URL' not in os.environ:
        flash('Database not configured. Please set DATABASE_URL environment variable.', 'error')
        return render_template('guestbook.html', entries=[], current_page=0, total_pages=0)
    
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
                             total_pages=total_pages)
    except Exception as e:
        flash(f'Error loading guestbook: {str(e)}', 'error')
        return render_template('guestbook.html', entries=[], current_page=0, total_pages=0)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'DATABASE_URL' in os.environ})