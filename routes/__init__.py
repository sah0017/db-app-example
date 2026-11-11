# Each feature keeps its routes in its own file in this folder
# (routes/actors.py, routes/films.py, ...). Keeping features in separate
# files means teammates working on different features don't edit the
# same file, so their changes don't conflict.
#
# A feature file must create a Flask Blueprint named bp. It can also set
# NAV_LINK to put a link to the feature on every page, for example:
#
#     bp = Blueprint('actors', __name__)
#     NAV_LINK = ('Actors', 'actors.get_actors')   # (label, endpoint)
#
# register_blueprints() below finds every feature file and registers it,
# so adding a feature never requires editing app.py.

import importlib
import pkgutil


def register_blueprints(app):
    """Register the blueprint from every module in this folder and
    return the list of (label, endpoint) navigation links."""
    nav_links = []
    # Sorted by file name, so the navigation links always appear in the same order
    for module_info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        bp = getattr(module, "bp", None)
        if bp is None:
            continue
        app.register_blueprint(bp)
        nav_link = getattr(module, "NAV_LINK", None)
        if nav_link:
            nav_links.append(nav_link)
    return nav_links
