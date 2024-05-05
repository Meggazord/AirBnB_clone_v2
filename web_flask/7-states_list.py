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


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Route that displays 'Hello HBNB!' """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Route that displays 'HBNB' """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Route that displays 'C ' followed by the value of the text variable """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """ Route that displays 'Python ' followed by the value of the text variable """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<n>', strict_slashes=False)
def is_number(n):
    """ Route that displays 'n is a number' only if n is an integer """
    try:
        int_n = int(n)
        return '{} is a number'.format(int_n)
    except ValueError:
        return '', 404
    

@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    """ Route that displays a number html template only if n is an integer """
    try:
        int_n = int(n)
        return render_template('5-number.html', n=n)
    except ValueError:
        return '', 404


@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def odd_or_even(n):
    """ Route that displays a number html template only if n is an integer """
    try:
        if int(n) % 2 == 0:
            check = 'even'
        else:
            check = 'odd'
        return render_template('6-number_odd_or_even.html', n=n, check=check)
    except ValueError:
        return '', 404


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Displays a HTML page with the list of State objects. """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
