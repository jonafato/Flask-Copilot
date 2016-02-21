"""Flask-Copilot test configuration."""

from flask import Flask
from flask_copilot import Copilot
import pytest


@pytest.fixture
def test_pilot():
    """Return a test extension."""
    return Copilot()


@pytest.fixture
def test_app():
    """Return a bare test application."""
    return Flask('test-pilot')
