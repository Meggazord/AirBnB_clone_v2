#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a HTML page with the list of State objects"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(debug=True)
