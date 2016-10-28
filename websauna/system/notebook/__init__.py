"""IPython Notebook integration."""
from pyramid.config import Configurator
from pyramid.events import subscriber
from websauna.system.admin.admin import Admin
from websauna.system import Initializer
from websauna.utils.autoevent import after
from websauna.utils.autoevent import bind_events
from websauna.utils.autoevent import event_source


import websauna.system.notebook.views


class NotebookInitializer():

    def __init__(self, config:Configurator):
        self.config = config


    @after(Initializer.configure_templates)
    def configure_templates(self):
        """Include our package templates folder in Jinja 2 configuration."""
        self.config.add_jinja2_search_path('websauna.system.notebook:templates', name='.html', prepend=False)  # HTML templates for

    def run(self):
        # Nothing here, advisors get called later
        bind_events(self.config.registry.initializer, self)
        self.configure_notebook()
        admin = Admin().construct()
        entry = menu.RouteEntry("admin-notebook", label="Shellsss", icon="fa-terminal", route_name="admin_shell", condition=lambda request:request.has_permission('shell'))
        admin.get_root_menu().add_entry(entry)

    @event_source
    def configure_notebook(self):
        """Setup pyramid_notebook integration."""
        self.config.add_route('admin_shell', '/notebook/admin-shell')
        self.config.add_route('shutdown_notebook', '/notebook/shutdown')
        self.config.add_route('notebook_proxy', '/notebook/*remainder')
        self.config.scan(websauna.system.notebook.views)


def includeme(config: Configurator):
    init = NotebookInitializer(config)
    init.run()
