"""
Supplier Invoice Loader - Configuration Loader
"""

try:
    from config.config_customer import *
except ImportError:
    print("WARNING: config_customer.py not found, using template")
    from config.config_template import *


# Create config object from imported variables
class _Config:
    """Config wrapper to convert module variables into object attributes"""

    def __init__(self):
        # Import all variables from current module
        import sys

        current_module = sys.modules[__name__]
        for name in dir(current_module):
            if not name.startswith("_") and name != "Config":
                setattr(self, name, getattr(current_module, name))


config = _Config()
