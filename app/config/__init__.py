import os

def get_config():
    """Return the appropriate configuration class based on the environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        from .production import Config
    elif env == 'testing':
        from .testing import Config
    else:
        from .development import Config
    
    return Config