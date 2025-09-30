import os
import logging
import socket

from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import Playwright
from browser_use.browser.browser import Browser, IN_DOCKER
from browser_use.browser.context import BrowserContextConfig
from browser_use.browser.chrome import (
    CHROME_ARGS,
    CHROME_DETERMINISTIC_RENDERING_ARGS,
    CHROME_DISABLE_SECURITY_ARGS,
    CHROME_DOCKER_ARGS,
    CHROME_HEADLESS_ARGS,
)
from browser_use.browser.utils.screen_resolution import get_screen_resolution, get_window_adjustments
from .custom_context import CustomBrowserContext

logger = logging.getLogger(__name__)


class CustomBrowser(Browser):

    async def new_context(self, config: BrowserContextConfig | None = None) -> CustomBrowserContext:
        """Create a browser context"""
        browser_config = self.config.model_dump() if self.config else {}
        context_config = config.model_dump() if config else {}
        merged_config = {**browser_config, **context_config}
        return CustomBrowserContext(config=BrowserContextConfig(**merged_config), browser=self)

    async def _setup_builtin_browser(self, playwright: Playwright) -> PlaywrightBrowser:
        """Sets up and returns a Playwright Browser instance with audio support, VNC resolution, and anti-detection measures."""

        assert self.config.browser_binary_path is None, (
            'browser_binary_path should be None if trying to use the builtin browsers'
        )

        # ----------------------------
        # DETERMINE SCREEN RESOLUTION
        # ----------------------------
        screen_size = None

        vnc_resolution_str = os.environ.get("VNC_RESOLUTION")
        if IN_DOCKER and vnc_resolution_str:
            try:
                width_str, height_str = vnc_resolution_str.lower().split('x')
                screen_size = {'width': int(width_str), 'height': int(height_str)}
                logger.info(f"Docker VNC mode detected. Using resolution {vnc_resolution_str}")
            except Exception as e:
                logger.warning(f"Could not parse VNC_RESOLUTION='{vnc_resolution_str}'. Error: {e}")

        if screen_size is None:
            if (
                hasattr(self.config, 'new_context_config')
                and self.config.new_context_config is not None
                and hasattr(self.config.new_context_config, 'window_width')
                and self.config.new_context_config.window_width is not None
                and hasattr(self.config.new_context_config, 'window_height')
                and self.config.new_context_config.window_height is not None
            ):
                screen_size = {
                    'width': self.config.new_context_config.window_width,
                    'height': self.config.new_context_config.window_height,
                }
                logger.info(f"Using UI settings for window size: {screen_size['width']}x{screen_size['height']}")
            else:
                if self.config.headless:
                    screen_size = {'width': 1920, 'height': 1080}
                    logger.info("Headless mode: default size 1920x1080")
                else:
                    screen_size = get_screen_resolution()
                    logger.info(f"Using screen resolution: {screen_size['width']}x{screen_size['height']}")

        offset_x, offset_y = (0, 0) if self.config.headless else get_window_adjustments()

        # ----------------------------
        # BUILD CHROME ARGS
        # ----------------------------
        chrome_args = {
            f'--remote-debugging-port={self.config.chrome_remote_debugging_port}',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-features=AudioServiceOutOfProcess',
            '--alsa-output-device=pulse',
            *CHROME_ARGS,
            *(CHROME_DOCKER_ARGS if IN_DOCKER else []),
            *(CHROME_HEADLESS_ARGS if self.config.headless else []),
            *(CHROME_DISABLE_SECURITY_ARGS if self.config.disable_security else []),
            *(CHROME_DETERMINISTIC_RENDERING_ARGS if self.config.deterministic_rendering else []),
            f'--window-position={offset_x},{offset_y}',
            f'--window-size={screen_size["width"]},{screen_size["height"]}',
            *self.config.extra_browser_args,
        }

        # Remove remote debugging port if already used
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', self.config.chrome_remote_debugging_port)) == 0:
                chrome_args.remove(f'--remote-debugging-port={self.config.chrome_remote_debugging_port}')

        browser_class = getattr(playwright, self.config.browser_class)
        args = {
            'chromium': list(chrome_args),
            'firefox': list({'-no-remote', *self.config.extra_browser_args}),
            'webkit': list({'--no-startup-window', *self.config.extra_browser_args}),
        }

        # ----------------------------
        # LAUNCH CHROMIUM
        # ----------------------------
        env = os.environ.copy()  # docker-compose already sets PULSE_SERVER and VNC_RESOLUTION

        browser = await browser_class.launch(
            channel='chromium',
            headless=self.config.headless,
            args=args[self.config.browser_class],
            proxy=self.config.proxy.model_dump() if self.config.proxy else None,
            handle_sigterm=False,
            handle_sigint=False,
            env=env,  # pass Docker environment variables
        )

        return browser
