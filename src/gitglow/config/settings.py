"""
GitGlow Configuration Management
===============================

Handles application configuration, settings, and persistent storage.
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import logging


@dataclass
class GitGlowConfig:
    """GitGlow application configuration."""
    
    # GitHub Settings
    github_token: Optional[str] = None
    github_username: Optional[str] = None
    monitored_repositories: List[str] = None
    
    # WiFi Settings
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    
    # LED Matrix Settings
    led_pin: int = 18
    led_count: int = 256
    led_brightness: int = 128  # 0-255
    matrix_width: int = 32
    matrix_height: int = 8
    display_width: int = 32    # Visible area
    display_height: int = 7    # 7 days (top row covered)
    
    # Rate Limiting Settings
    rate_limit_strategy: str = "adaptive"
    commit_update_interval: int = 900    # 15 minutes
    pr_update_interval: int = 120        # 2 minutes
    review_update_interval: int = 60     # 1 minute (work hours)
    review_update_interval_off: int = 300  # 5 minutes (off hours)
    
    # Work Hours (for adaptive polling)
    work_start_hour: int = 9
    work_end_hour: int = 18
    
    # Web Interface Settings
    web_port: int = 8080
    setup_ssid: str = "GitGlow-Setup"
    setup_password: str = ""  # Open network for setup
    
    # Logging Settings
    log_level: str = "INFO"
    log_file: str = "/var/log/gitglow/gitglow.log"
    
    # File Paths
    config_file: Optional[Path] = None
    
    def __post_init__(self):
        """Post-initialization setup."""
        if self.monitored_repositories is None:
            self.monitored_repositories = []
        
        if self.config_file is None:
            self.config_file = Path.home() / ".config" / "gitglow" / "config.yaml"
        
        # Ensure config directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing configuration if available
        self.load_configuration()
    
    def is_configured(self) -> bool:
        """Check if GitGlow is properly configured."""
        return all([
            self.github_token,
            self.github_username,
            self.wifi_ssid,
            self.monitored_repositories
        ])
    
    def load_configuration(self) -> None:
        """Load configuration from file."""
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            if config_data:
                self._update_from_dict(config_data)
                
        except Exception as e:
            logging.warning(f"Failed to load configuration: {e}")
    
    def save_configuration(self) -> None:
        """Save current configuration to file."""
        try:
            config_data = asdict(self)
            
            # Convert Path objects to strings for YAML serialization
            config_data['config_file'] = str(self.config_file)
            
            with open(self.config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            raise
    
    def _update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                # Handle Path objects
                if key == 'config_file' and isinstance(value, str):
                    value = Path(value)
                setattr(self, key, value)
    
    def update_github_settings(self, token: str, username: str, 
                             repositories: List[str]) -> None:
        """Update GitHub-related settings."""
        self.github_token = token
        self.github_username = username
        self.monitored_repositories = repositories
        self.save_configuration()
    
    def update_wifi_settings(self, ssid: str, password: str) -> None:
        """Update WiFi settings."""
        self.wifi_ssid = ssid
        self.wifi_password = password
        self.save_configuration()
    
    def update_led_settings(self, brightness: Optional[int] = None,
                           pin: Optional[int] = None) -> None:
        """Update LED matrix settings."""
        if brightness is not None:
            self.led_brightness = max(0, min(255, brightness))
        if pin is not None:
            self.led_pin = pin
        self.save_configuration()
    
    def clear_configuration(self) -> None:
        """Clear all configuration (for setup mode)."""
        self.github_token = None
        self.github_username = None
        self.monitored_repositories = []
        self.wifi_ssid = None
        self.wifi_password = None
        
        # Remove config file
        if self.config_file.exists():
            self.config_file.unlink()
    
    @classmethod
    def from_environment(cls) -> 'GitGlowConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Load from environment variables
        config.github_token = os.getenv('GITGLOW_GITHUB_TOKEN')
        config.github_username = os.getenv('GITGLOW_GITHUB_USERNAME')
        config.wifi_ssid = os.getenv('GITGLOW_WIFI_SSID')
        config.wifi_password = os.getenv('GITGLOW_WIFI_PASSWORD')
        
        # LED settings
        if pin := os.getenv('GITGLOW_LED_PIN'):
            config.led_pin = int(pin)
        if brightness := os.getenv('GITGLOW_LED_BRIGHTNESS'):
            config.led_brightness = int(brightness)
        
        # Web settings
        if port := os.getenv('GITGLOW_WEB_PORT'):
            config.web_port = int(port)
        
        # Logging
        if log_level := os.getenv('GITGLOW_LOG_LEVEL'):
            config.log_level = log_level.upper()
        
        # Parse monitored repositories from comma-separated string
        if repos := os.getenv('GITGLOW_REPOSITORIES'):
            config.monitored_repositories = [r.strip() for r in repos.split(',')]
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        data = asdict(self)
        data['config_file'] = str(self.config_file)
        return data
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"GitGlowConfig(configured={self.is_configured()})"