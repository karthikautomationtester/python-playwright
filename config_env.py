import os
import pytest
from playwright.sync_api import Playwright

# Environment-based configuration
ENVIRONMENT = os.getenv("TEST_ENV", "local")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Environment-specific browser context settings"""
    base_config = {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }
    
    if ENVIRONMENT == "ci":
        # CI-specific settings
        base_config.update({
            "record_video_dir": "test-results/videos/",
            "record_video_size": {"width": 1920, "height": 1080},
        })
    elif ENVIRONMENT == "local":
        # Local development settings
        base_config.update({
            "slow_mo": 100,
        })
    
    return base_config

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Environment-specific browser launch settings"""
    base_config = {
        **browser_type_launch_args,
        "headless": ENVIRONMENT == "ci",  # Headless in CI, headed locally
    }
    
    return base_config
