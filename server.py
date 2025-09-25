from flask import Flask, render_template, request, jsonify
import os
from database import setup, add_person, get_people

app = Flask(__name__)

# Initialize database connection pool
@app.before_first_request
def initialize_database():
    if 'DATABASE_URL' in os.environ:
        setup()

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            try:
                add_person(name)
                return jsonify({'success': True, 'message': f'Added {name} to database'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        else:
            return jsonify({'success': False, 'error': 'Name is required'}), 400

    # GET request - return list of people
    try:
        page = int(request.args.get('page', 0))
        people_list = get_people(page=page)
        return jsonify({'people': [dict(person) for person in people_list]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'DATABASE_URL' in os.environ})