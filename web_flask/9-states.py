#!/usr/bin/python3
"""
Starts a Flask web application
"""

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


@app.route('/states', strict_slashes=False)
def states():
    """
    Displays a HTML page with the list of State objects.

    Returns:
        Rendered HTML template with the list of State objects.
    """
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """
    Displays a HTML page with the list of City objects linked to the State with the given id.

    Args:
        id (str): The id of the State.

    Returns:
        Rendered HTML template with the list of City objects linked to the State with the given id.
    """
    state = storage.get(State, id)
    if state is None:
        return render_template('9-not_found.html'), 404
    return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
