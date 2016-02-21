Flask-Copilot
=============

Installation
============

.. code:: bash

    python -m pip install flask-copilot

Quickstart
==========

1. Initialize the ``Copilot`` extension on your Flask app.
2. Add URL routes normally. Include ``navbar_kwargs`` to register routes to
   your navbar.

.. code:: python

    from flask import Flask
    from flask_copilot import Copilot

    app = Flask(__name__)
    copilot = Copilot(app)

    @app.route('/', navbar_kwargs={'path': 'Home'})
    def index():
        """Render the home page."""
        return render_template('index.html')

3. Render your navbar using the ``navbar`` object automatically injected into
   your template context.

.. code:: jinja

    <ul>
      {% for entry in navbar recursive %}
        <li>
          <a href="{{ entry.url() }}">
            {{ entry.name }}
          </a>
          {% if entry.children %}
            <ul class="dropdown">{{ loop(entry.children) }}</ul>
          {% endif %}
        </li>
      {% endfor %}
    </ul>

Contents:

.. toctree::
   :maxdepth: 1

   api
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

