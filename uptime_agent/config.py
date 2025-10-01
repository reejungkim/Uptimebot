"""
Configuration module for uptime monitoring.

This module handles configuration loading from environment variables
and configuration files.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import yaml


class Config:
    """Configuration manager for uptime monitoring."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to YAML configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Default configuration
        self.config = {
            'monitoring': {
                'check_interval': 5,  # minutes
                'timeout': 30,  # seconds
                'max_retries': 3,
                'urls': []
            },
            'logging': {
                'level': 'INFO',
                'file': 'uptime_monitor.log',
                'max_size': 10485760,  # 10MB
                'backup_count': 5
            },
            'notifications': {
                'enabled': False,
                'email': {
                    'smtp_server': '',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'from_email': '',
                    'to_emails': []
                },
                'webhook': {
                    'url': '',
                    'timeout': 10
                }
            },
            'database': {
                'type': 'sqlite',
                'path': 'uptime_monitor.db',
                'host': 'localhost',
                'port': 5432,
                'username': '',
                'password': '',
                'database': 'uptime_monitor'
            }
        }
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        # Override with environment variables
        self.load_from_env()
    
    def load_from_file(self, config_file: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_config(self.config, file_config)
        except Exception as e:
            print(f"Error loading config file {config_file}: {e}")
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            'UPTIME_CHECK_INTERVAL': ('monitoring', 'check_interval'),
            'UPTIME_TIMEOUT': ('monitoring', 'timeout'),
            'UPTIME_MAX_RETRIES': ('monitoring', 'max_retries'),
            'UPTIME_URLS': ('monitoring', 'urls'),
            'LOG_LEVEL': ('logging', 'level'),
            'LOG_FILE': ('logging', 'file'),
            'NOTIFICATIONS_ENABLED': ('notifications', 'enabled'),
            'SMTP_SERVER': ('notifications', 'email', 'smtp_server'),
            'SMTP_PORT': ('notifications', 'email', 'smtp_port'),
            'SMTP_USERNAME': ('notifications', 'email', 'username'),
            'SMTP_PASSWORD': ('notifications', 'email', 'password'),
            'FROM_EMAIL': ('notifications', 'email', 'from_email'),
            'TO_EMAILS': ('notifications', 'email', 'to_emails'),
            'WEBHOOK_URL': ('notifications', 'webhook', 'url'),
            'DB_TYPE': ('database', 'type'),
            'DB_PATH': ('database', 'path'),
            'DB_HOST': ('database', 'host'),
            'DB_PORT': ('database', 'port'),
            'DB_USERNAME': ('database', 'username'),
            'DB_PASSWORD': ('database', 'password'),
            'DB_DATABASE': ('database', 'database')
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(self.config, config_path, value)
    
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _set_nested_value(self, config: Dict[str, Any], path: tuple, value: Any) -> None:
        """Set a nested configuration value."""
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Convert value types
        if path[-1] in ['check_interval', 'timeout', 'max_retries', 'smtp_port', 'port', 'backup_count']:
            current[path[-1]] = int(value)
        elif path[-1] in ['max_size', 'webhook_timeout']:
            current[path[-1]] = int(value)
        elif path[-1] in ['enabled']:
            current[path[-1]] = value.lower() in ('true', '1', 'yes', 'on')
        elif path[-1] in ['urls', 'to_emails']:
            current[path[-1]] = [url.strip() for url in value.split(',') if url.strip()]
        else:
            current[path[-1]] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split('.')
        current = self.config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split('.')
        current = self.config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the complete configuration as a dictionary."""
        return self.config.copy()
