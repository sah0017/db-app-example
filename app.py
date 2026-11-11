import os
import secrets

from core import app
from flask import abort, request, session
from flask.templating import render_template
from routes import register_blueprints

# This file holds only what every feature shares: CSRF protection, the
# navigation links and the home page. Each feature's routes are in its own
# file in the routes folder (see routes/__init__.py).

# Every form includes a token from the user's session, so a POST
# sent from another website (which can't read the token) is rejected
@app.context_processor
def add_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return {'csrf_token': session['csrf_token']}

@app.before_request
def check_csrf_token():
    if request.method == 'POST':
        expected = session.get('csrf_token', '')
        submitted = request.form.get('csrf_token', '')
        if not expected or not secrets.compare_digest(expected, submitted):
            abort(400, "This form has expired. Go back, reload the page and try again.")

# Register every feature's routes and remember their navigation links
nav_links = register_blueprints(app)

# Make the navigation links available to every template (used by base.html)
@app.context_processor
def add_nav_links():
    return {'nav_links': nav_links}

# A decorator used to tell the application
# which URL is associated with which function
@app.route('/hello')
def hello():
    return 'HELLO'

# APP ROUTE TO RENDER HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    # The debugger lets anyone who sees an error page run code, so it is
    # off unless FLASK_DEBUG=1 is set (for example in .env)
    app.run(port=8000, debug=os.environ.get('FLASK_DEBUG') == '1')
