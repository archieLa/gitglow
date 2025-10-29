#!/usr/bin/env python3
"""
GitGlow Main Application
========================

Entry point for the GitGlow application. Handles initialization,
configuration, and orchestration of all components.
"""

import logging
import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

from .config.settings import GitGlowConfig
from .api.github_client import GitHubClient
from .display.matrix_controller import MatrixController
from .web.app import create_web_app
from .config.wifi_manager import WiFiManager


class GitGlowApp:
    """Main GitGlow application class."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize GitGlow application.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = GitGlowConfig(config_path)
        self.logger = self._setup_logging()
        self.github_client: Optional[GitHubClient] = None
        self.matrix_controller: Optional[MatrixController] = None
        self.wifi_manager: Optional[WiFiManager] = None
        self.web_app = None
        self.running = False
        
    def _setup_logging(self) -> logging.Logger:
        """Set up application logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    async def initialize(self) -> None:
        """Initialize all application components."""
        self.logger.info("Initializing GitGlow...")
        
        # Initialize WiFi manager
        self.wifi_manager = WiFiManager(self.config)
        
        # Check if we need to enter setup mode
        if not self.config.is_configured():
            self.logger.info("Configuration incomplete, entering setup mode")
            await self._enter_setup_mode()
            return
        
        # Initialize GitHub client
        self.github_client = GitHubClient(
            token=self.config.github_token,
            rate_limit_strategy=self.config.rate_limit_strategy
        )
        
        # Initialize LED matrix controller
        self.matrix_controller = MatrixController(self.config)
        
        # Create web application
        self.web_app = create_web_app(self.config, self)
        
        self.logger.info("GitGlow initialized successfully")
    
    async def _enter_setup_mode(self) -> None:
        """Enter captive portal setup mode."""
        self.logger.info("Starting captive portal for setup...")
        
        # Start WiFi hotspot
        await self.wifi_manager.start_hotspot()
        
        # Start web interface for configuration
        from .web.captive_portal import create_setup_app
        self.web_app = create_setup_app(self.config, self)
        
        self.logger.info("Setup mode active - connect to 'GitGlow-Setup' network")
    
    async def run(self) -> None:
        """Run the main application loop."""
        await self.initialize()
        
        if not self.config.is_configured():
            # Run in setup mode
            await self._run_setup_mode()
        else:
            # Run normal operation
            await self._run_normal_mode()
    
    async def _run_setup_mode(self) -> None:
        """Run application in setup mode."""
        self.running = True
        
        # Start web server for configuration
        from hypercorn.asyncio import serve
        from hypercorn.config import Config
        
        hypercorn_config = Config()
        hypercorn_config.bind = ["0.0.0.0:80"]
        
        self.logger.info("Starting setup web server on port 80")
        
        try:
            await serve(self.web_app, hypercorn_config)
        except KeyboardInterrupt:
            self.logger.info("Setup interrupted by user")
        finally:
            await self.shutdown()
    
    async def _run_normal_mode(self) -> None:
        """Run application in normal operation mode."""
        self.running = True
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._update_contribution_graph()),
            asyncio.create_task(self._monitor_pull_requests()),
            asyncio.create_task(self._run_web_server()),
        ]
        
        # Set up signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown()))
        
        self.logger.info("GitGlow running normally - GitHub monitoring active")
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            await self.shutdown()
    
    async def _update_contribution_graph(self) -> None:
        """Background task to update contribution graph."""
        while self.running:
            try:
                # Fetch contribution data from GitHub
                contributions = await self.github_client.get_contributions(
                    username=self.config.github_username,
                    weeks=32
                )
                
                # Update LED matrix display
                await self.matrix_controller.display_contributions(contributions)
                
                # Wait for next update (15 minutes)
                await asyncio.sleep(15 * 60)
                
            except Exception as e:
                self.logger.error(f"Error updating contribution graph: {e}")
                await asyncio.sleep(60)  # Retry in 1 minute
    
    async def _monitor_pull_requests(self) -> None:
        """Background task to monitor pull request events."""
        while self.running:
            try:
                # Check for new PR events
                pr_events = await self.github_client.get_pr_events(
                    repositories=self.config.monitored_repositories
                )
                
                # Update notification bar
                for event in pr_events:
                    await self.matrix_controller.show_notification(event)
                
                # Wait for next check (2 minutes)
                await asyncio.sleep(2 * 60)
                
            except Exception as e:
                self.logger.error(f"Error monitoring pull requests: {e}")
                await asyncio.sleep(60)
    
    async def _run_web_server(self) -> None:
        """Run the web interface server."""
        from hypercorn.asyncio import serve
        from hypercorn.config import Config
        
        hypercorn_config = Config()
        hypercorn_config.bind = [f"0.0.0.0:{self.config.web_port}"]
        
        self.logger.info(f"Starting web server on port {self.config.web_port}")
        
        try:
            await serve(self.web_app, hypercorn_config)
        except Exception as e:
            self.logger.error(f"Web server error: {e}")
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        self.logger.info("Shutting down GitGlow...")
        self.running = False
        
        # Clean up components
        if self.matrix_controller:
            await self.matrix_controller.clear_display()
        
        if self.wifi_manager:
            await self.wifi_manager.cleanup()
        
        self.logger.info("GitGlow shutdown complete")


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitGlow - GitHub LED Matrix Display")
    parser.add_argument(
        "--config", 
        type=Path, 
        help="Path to configuration file"
    )
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Force setup mode"
    )
    
    args = parser.parse_args()
    
    app = GitGlowApp(args.config)
    
    if args.setup:
        # Force setup mode
        app.config.clear_configuration()
    
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nGitGlow stopped by user")
    except Exception as e:
        print(f"GitGlow error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()