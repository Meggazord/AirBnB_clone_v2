#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """
    Removes the current SQLAlchemy Session.

    Args:
        exception: Exception raised during the request.
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Displays a HTML page with the list of State objects and associated City objects.

    Returns:
        Rendered HTML template with the list of State objects and associated City objects.
    """
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
