"""Flask-Copilot example application."""

from flask import Flask, render_template
from flask_copilot import Copilot


app = Flask(__name__)
Copilot(app)


# Make sure Home is the first thing in the list with ``order``.
@app.route('/', navbar_kwargs={'path': 'Home', 'order': ''})
def index():
    """Render the homepage."""
    return render_template('index.j2')


@app.route('/about/flask/', navbar_kwargs={'path': ('About', 'Flask')})
def about_flask():
    """About Flask."""
    return render_template('about-flask.j2')


@app.route('/about/copilot/', navbar_kwargs={'path': ('About', 'Copilot')})
def about_copilot():
    """About Flask-Copilot."""
    return render_template('about-copilot.j2')


if __name__ == '__main__':
    app.run(debug=True)
