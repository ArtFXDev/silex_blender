from silex_client.core.context import Context
from addon_utils import enable


def register():
    # Enable the addon
    enable("silex_blender", default_set=True)

    # Start Silex services
    Context.get().start_services()


def unregister():
    pass
