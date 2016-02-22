"""Navigation help for Flask applications."""

from copy import deepcopy
from functools import partial, total_ordering
import os
import pkg_resources
import sys

from flask import url_for
from sortedcontainers import SortedList
from werkzeug.routing import Rule

__all__ = ('Copilot',)

try:
    _dist = pkg_resources.get_distribution(__package__)
    if not __file__.startswith(os.path.join(_dist.location, __package__)):
        # Manually raise the exception if there is a distribution but
        # it's installed from elsewhere.
        raise pkg_resources.DistributionNotFound
except pkg_resources.DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version


MODERN_PYTHON = sys.version_info.major >= 3
if MODERN_PYTHON:
    basestring = str


class Copilot(object):
    """The Flask-Copilot extension.

    Args:
        app (Optional[flask.Flask]): The application instance that this
            copilot should be registered to.
    """

    def __init__(self, app=None):
        """Initialize the extension."""
        self.navbar_entries = SortedList()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register the extension with the application.

        Args:
            app (flask.Flask): The application to register with.
        """
        app.url_rule_class = partial(NavigationRule, copilot=self)
        app.context_processor(self.inject_context)

    def inject_context(self):
        """Return a dict used for a template context."""
        navbar = filter(lambda entry: entry.visible, self.navbar_entries)
        return {'navbar': navbar}

    def register_entry(self, navbar_kwargs):
        """Register a navbar entry with the copilot.

        Args:
            navbar_kwargs (dict): Arguments passed to the
                :class:`NavbarEntry` instance.
        """
        # Add a new rule for each level in the path.
        path = navbar_kwargs.pop('path')
        # If a single object is used rather than an iterable (including
        # a single string), wrap it before using.
        if not hasattr(path, '__iter__') or isinstance(path, basestring):
            path = [path]

        entry_group = self.navbar_entries
        # HACK: I'd like to intelligently replace the URL rule in the
        # case where the intended rule is provided, but the function has
        # already created a blank "placeholder" rule for it. There are
        # probably nicer ways to approach this, but it works.
        for name, is_last in iter_islast(path):
            kwargs = deepcopy(navbar_kwargs)
            kwargs['name'] = name
            for existing_entry in entry_group:
                # If there's an existing entry for this "link", use it
                # instead of creating a new one. If this existing entry
                # has no rule and this is the last item in ``path``, the
                # rule was intended to be assigned to this entry, so
                # overwrite the blank rule with the one provided via
                # ``navbar_kwargs``.
                if existing_entry.name == name:
                    entry = existing_entry
                    if is_last:
                        entry.endpoint = kwargs['endpoint']
                    break
            else:
                # If we can't find an existing entry, create one with a
                # blank endpoint. If this rule is not the final one in
                # the list, the endpoint was not intended for this, so
                # don't assign it.
                if not is_last:
                    kwargs['endpoint'] = None
                entry = NavbarEntry(**kwargs)
                entry_group.add(entry)
            entry_group = entry.children


@total_ordering
class NavbarEntry(object):
    """Stores information related to a routing rule's navbar position.

    Args:
        name (str): The text of the link in the navbar. This element is
            converted to a ``str`` when added to the navbar and used for
            display and sorting purposes. This value should be unique
            within a group (i.e. a single name should not have more than
            one URL rule associated with it).
        endpoint (str): The endpoint assigned to the URL rule this
            ``NavbarEntry`` belongs to. This should be used to generate
            the URL for the link.
        url_for_kwargs (dict): Keyword arguments to be passed to
            ``url_for`` when generating URLs from ``endpoint``.
        order: An object used to sort the navigation entries. If not
            provided, the entry's name (the last element of ``path``)
            will be used. All entries in the same group must be
            orderable together.
        when (Optional[callable]): If provided, the link will appear
            only when the value returned by ``when()`` is truthy.
    """

    def __init__(self, name, endpoint,
                 url_for_kwargs=None, order=None, when=None):
        """Initialize the instance."""
        # Set the real defaults.
        if url_for_kwargs is None:
            url_for_kwargs = {}
        if order is None:
            order = name

        # Store the information needed to generate the navbar links.
        self.name = str(name)
        self.endpoint = endpoint
        self.url_for_kwargs = url_for_kwargs
        self.children = SortedList()
        self.order = order
        self.when = when

    def __lt__(self, other):
        """Return sort order based on ``self.order`` and ``other.order``."""
        return self.order < other.order

    @property
    def visible(self):
        """Return ``True`` when this entry should be visible.

        Rules dictating visibility, in order or precedence:

        1. If an entry has a ``when`` method, its result is returned.
        2. If an entry has children and no endpoint (i.e. it exists
           solely as a container for other links), it is visible when
           any of its children are.
        3. Finally, when the first two rules don't apply, visibility
           defaults to ``True``.
        """
        if self.when:
            return self.when()
        elif self.children and not self.endpoint:
            return any(child.visible for child in self.children)
        return True

    def url(self, default_href='#'):
        """Return a rendered URL for this entry.

        Args:
            default_href (str): The value to return if no endpoint is
                assigned to this entry. Defaults to ``'#'``.
        """
        if not self.endpoint:
            return default_href
        return url_for(self.endpoint, **self.url_for_kwargs)


class NavigationRule(Rule):
    """Store navigation information along with routing rules.

    Args:
        *args (list): Positional arguments passed to the underlying
            `werkzeug.routing.Rule` object.
        **kwargs (dict): Keyword arguments passed to the underlying
            :class:`werkzeug.routing.Rule` object.
        copilot (Copilot): The Flask-Copilot instance that this rule's
            navbar entry will be registered with. This argument must be
            passed as a keyword argument.
        navbar_kwargs (Optional[dict]): Keyword args passed to
            :class:`NavbarEntry`. This argument must be passed as a
            keyword argument.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the rule."""
        copilot = kwargs.pop('copilot')
        navbar_kwargs = kwargs.pop('navbar_kwargs', None)
        super(NavigationRule, self).__init__(*args, **kwargs)
        if navbar_kwargs:
            navbar_kwargs['endpoint'] = self.endpoint
            copilot.register_entry(navbar_kwargs)


# NOTE: Taken and slightly modified from the ActiveState Code Recipe at
# https://code.activestate.com/recipes/392015-finding-the-last-item-in-a-loop/
def iter_islast(iterable):
    """Generate (item, islast) pairs for an iterable.

    Generates pairs where the first element is an item from the iterable
    source and the second element is a boolean flag indicating if it is
    the last item in the sequence.
    """
    it = iter(iterable)
    prev = next(it)
    for item in it:
        yield prev, False
        prev = item
    yield prev, True
