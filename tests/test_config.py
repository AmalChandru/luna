import os
import pytest
from app.config import get_config

# Import configuration classes for testing purposes
from app.config.development import Config as DevConfig
from app.config.production import Config as ProdConfig

@pytest.fixture
def mock_environment(monkeypatch):
    """Fixture to mock environment variables."""
    def set_env(env_name):
        monkeypatch.setenv('FLASK_ENV', env_name)
    return set_env

def test_get_config_development(mock_environment):
    """Test that the development config is returned when FLASK_ENV is set to development."""
    mock_environment('development')
    config = get_config()
    assert isinstance(config, DevConfig)

def test_get_config_production(mock_environment):
    """Test that the production config is returned when FLASK_ENV is set to production."""
    mock_environment('production')
    config = get_config()
    assert isinstance(config, ProdConfig)

def test_get_config_default(mock_environment):
    """Test that the default config is returned when FLASK_ENV is not set."""
    mock_environment('')  # Unset environment variable
    config = get_config()
    assert isinstance(config, DevConfig)
