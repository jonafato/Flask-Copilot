"""Flask-Copilot NavbarEntry tests."""

import pytest

from flask_copilot import NavbarEntry


def test_default_visibility():
    """Test that NavbarEntries are visible by default."""
    assert NavbarEntry('Test', None).visible


@pytest.mark.parametrize('setting', (True, False))
def test_provided_visibility(setting):
    """Test that a NavbarEntry's visibility is controlled by ``when``."""
    entry = NavbarEntry('Test', None, when=lambda: setting)
    assert bool(entry.visible) == setting


@pytest.mark.parametrize('setting', (True, False))
def test_computed_visibility(setting):
    """Test that a NavbarEntry is visible when any of its descendants are."""
    root = NavbarEntry('Test', None)
    child = NavbarEntry('Child', None, when=lambda: setting)
    root.children.append(child)
    assert bool(root.visible) == setting


@pytest.mark.parametrize('setting', (True, False))
def test_visibility_precendence(setting):
    """Test that ``when`` takes precedence of descendant computation."""
    root = NavbarEntry('Test', None, when=lambda: setting)
    child = NavbarEntry('Child', None, when=lambda: not setting)
    assert bool(root.visible) == setting
    assert bool(root.visible) != bool(child.visible)


def test_default_sort():
    """Test that children are sorted by their name by default."""
    root = NavbarEntry('Test', None)
    a = NavbarEntry('A', None)
    b = NavbarEntry('B', None)
    c = NavbarEntry('C', None)
    root.children.add(c)
    root.children.add(a)
    root.children.add(b)
    assert root.children == [a, b, c]


def test_explicit_sort():
    """Test that children are properly sorted by their provided order."""
    root = NavbarEntry('Test', None)
    a = NavbarEntry('A', None, order=3)
    b = NavbarEntry('B', None, order=2)
    c = NavbarEntry('C', None, order=1)
    root.children.add(c)
    root.children.add(a)
    root.children.add(b)
    assert root.children == [c, b, a]
