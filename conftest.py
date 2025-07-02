import pytest
import os
from playwright.sync_api import Playwright, Browser, BrowserContext, Page

# Environment variable for browser selection
BROWSER_NAME = os.getenv("BROWSER", "chromium")  # Default to chromium
BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", None)  # chrome, msedge, etc.

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context settings"""
    return {
        **browser_context_args,
        # Viewport size
        "viewport": {"width": 1920, "height": 1080},
        # User agent
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        # Locale and timezone
        "locale": "en-US",
        "timezone_id": "America/New_York",
        # Permissions
        "permissions": ["geolocation"],
        # Extra HTTP headers
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9"
        },
        # Record video (optional)
        # "record_video_dir": "videos/",
        # "record_video_size": {"width": 1920, "height": 1080},
        # Screenshots on failure
        # "record_har_path": "har_files/test.har",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch settings"""
    return {
        **browser_type_launch_args,
        # Browser window settings
        "headless": False,  # Set to True for headless mode
        "slow_mo": 100,     # Slow down operations by 100ms
        # Browser arguments
        "args": [
            "--start-maximized",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ],
        # Downloads directory
        # "downloads_path": "downloads/",
        # Devtools (for debugging)
        "devtools": False,
    }

# Custom browser fixture for Chrome specifically (renamed to avoid conflicts)
@pytest.fixture(scope="session")
def chrome_browser(playwright: Playwright):
    """Custom browser fixture with Chrome-specific settings"""
    try:
        browser = playwright.chromium.launch(
            channel="chrome",  # Use system Chrome instead of Chromium
            headless=False,
            slow_mo=50,
            args=[
                "--start-maximized",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--no-sandbox"  # Useful for CI environments
            ]
        )
    except Exception as e:
        # Fallback to regular Chromium if Chrome is not available
        print(f"Chrome not found, falling back to Chromium: {e}")
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=50,
            args=[
                "--start-maximized",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        )
    yield browser
    browser.close()

# Environment-based browser fixture
@pytest.fixture(scope="session")
def browser_env(playwright: Playwright):
    """Browser fixture that respects environment variables"""
    try:
        launch_options = {
            "headless": os.getenv("HEADLESS", "false").lower() == "true",
            "slow_mo": int(os.getenv("SLOW_MO", "50")),
            "args": [
                "--start-maximized",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        }
        
        # Add channel if specified
        if BROWSER_CHANNEL:
            launch_options["channel"] = BROWSER_CHANNEL
        
        # Select browser based on environment
        if BROWSER_NAME == "firefox":
            browser = playwright.firefox.launch(**launch_options)
        elif BROWSER_NAME == "webkit":
            browser = playwright.webkit.launch(**launch_options)
        else:  # Default to chromium
            browser = playwright.chromium.launch(**launch_options)
        
        yield browser
        browser.close()
    except Exception as e:
        print(f"Error launching browser {BROWSER_NAME}: {e}")
        # Fallback to basic chromium
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

# Optional: Test configuration
@pytest.fixture(autouse=True)
def configure_test_environment(page: Page):
    """Configure test environment for each test"""
    # Set default timeout
    page.set_default_timeout(30000)  # 30 seconds
    
    # Set default navigation timeout
    page.set_default_navigation_timeout(30000)
    
    # Add any global page setup here
    yield
    
    # Cleanup after each test (optional)
    # page.close()
