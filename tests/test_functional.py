"""Flask-Copilot functional tests."""

from flask import render_template_string

from flask_copilot import Copilot


def test_default_routing_behavior(test_app, test_pilot):
    """Test that Flask-Copilot doesn't interfere with normal behavior."""
    test_pilot.init_app(test_app)

    @test_app.route('/')
    def index():
        pass

    assert not test_pilot.navbar_entries


def test_rule_registration(test_app, test_pilot):
    """Test registering a rule and navbar entry."""
    test_pilot.init_app(test_app)

    @test_app.route('/', navbar_kwargs={'path': ('Home',)})
    def index():
        pass

    assert len(test_pilot.navbar_entries) == 1


def test_string_rule_registration(test_app, test_pilot):
    """Test that registering a rule with a single string path works."""
    test_pilot.init_app(test_app)

    @test_app.route('/', navbar_kwargs={'path': 'Home'})
    def index():
        pass

    assert len(test_pilot.navbar_entries) == 1


def test_name_string_converstion(test_app, test_pilot):
    """Test that path entries are converted to strings."""
    class Foo(object):
        def __str__(self):
            return 'Foo'

    test_pilot.init_app(test_app)

    @test_app.route('/', navbar_kwargs={'path': (Foo(),)})
    def index():
        pass

    assert len(test_pilot.navbar_entries) == 1
    assert test_pilot.navbar_entries[0].name == 'Foo'


def test_descendant_rule_registration(test_app, test_pilot):
    """Test registering a hierarchy of rules."""
    test_pilot.init_app(test_app)

    @test_app.route('/', navbar_kwargs={'path': ('Home',)})
    def home():
        pass

    @test_app.route(
        '/foo/bar/baz/', navbar_kwargs={'path': ('Foo', 'Bar', 'Baz')})
    def baz():
        pass

    @test_app.route(
        '/foo/bar/quux/', navbar_kwargs={'path': ('Foo', 'Bar', 'Quux')})
    def quux():
        pass

    assert len(test_pilot.navbar_entries) == 2

    foo = test_pilot.navbar_entries[0]
    assert foo.name == 'Foo'
    assert len(foo.children) == 1

    bar = foo.children[0]
    assert len(bar.children) == 2
    assert bar.children[0].name == 'Baz'
    assert bar.children[1].name == 'Quux'


def test_endpoint_replacement(test_app, test_pilot):
    """Test that missing endpoints are filled in when desired."""
    test_pilot.init_app(test_app)

    @test_app.route('/foo/bar/', navbar_kwargs={'path': ('Foo', 'Bar')})
    def bar():
        pass

    assert not test_pilot.navbar_entries[0].endpoint

    @test_app.route('/foo/', navbar_kwargs={'path': ('Foo',)})
    def foo():
        pass

    assert test_pilot.navbar_entries[0].endpoint


def test_default_extension_registration(test_app):
    """Test that the extension is automatically initialized when desired."""
    original_url_rule_class = test_app.url_rule_class
    Copilot(test_app)
    new_url_rule_class = test_app.url_rule_class

    assert original_url_rule_class is not new_url_rule_class


def test_template_context(test_app, test_pilot):
    """Test that the template context gets injected properly."""
    test_pilot.init_app(test_app)

    @test_app.route('/', navbar_kwargs={'path': ('Home',)})
    def index():
        pass

    template_string = '''
        {% for entry in navbar %}
            <a href="{{ entry.url() }}">{{ entry.name }}</a>
        {% endfor %}
    '''
    with test_app.test_request_context('/'):
        rendered = render_template_string(template_string)

    expected = '<a href="/">Home</a>'
    assert rendered.strip() == expected
