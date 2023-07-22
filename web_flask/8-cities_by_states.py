#!/usr/bin/python3
"""Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Closes the database at the end of the request."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with a list of States and their Cities."""
    states = sorted(storage.all('State').values(), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

