"""
Logging module for uptime monitoring.

This module provides structured logging functionality
for the uptime monitoring system.
"""

import logging
import logging.handlers
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class UptimeLogger:
    """Custom logger for uptime monitoring with structured logging."""
    
    def __init__(self, name: str = "uptime_monitor", 
                 log_file: str = "uptime_monitor.log",
                 level: str = "INFO",
                 max_size: int = 10485760,  # 10MB
                 backup_count: int = 5):
        """
        Initialize the uptime logger.
        
        Args:
            name: Logger name
            log_file: Log file path
            level: Logging level
            max_size: Maximum log file size in bytes
            backup_count: Number of backup files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        self.console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_size, backupCount=backup_count
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(self.file_formatter)
            self.logger.addHandler(file_handler)
    
    def _log_structured(self, level: str, message: str, **kwargs) -> None:
        """Log a structured message with additional context."""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level.upper(),
            'message': message,
            **kwargs
        }
        
        log_message = json.dumps(log_data, default=str)
        getattr(self.logger, level.lower())(log_message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        self._log_structured('info', message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log a debug message."""
        self._log_structured('debug', message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        self._log_structured('warning', message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        self._log_structured('error', message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log a critical message."""
        self._log_structured('critical', message, **kwargs)
    
    def log_check_result(self, url: str, success: bool, 
                        response_time: Optional[float] = None,
                        status_code: Optional[int] = None,
                        error: Optional[str] = None) -> None:
        """Log the result of an uptime check."""
        self.info(
            f"Uptime check completed for {url}",
            url=url,
            success=success,
            response_time=response_time,
            status_code=status_code,
            error=error,
            event_type="uptime_check"
        )
    
    def log_notification(self, notification_type: str, target: str, 
                        success: bool, message: str = "") -> None:
        """Log notification attempts."""
        self.info(
            f"Notification sent via {notification_type}",
            notification_type=notification_type,
            target=target,
            success=success,
            message=message,
            event_type="notification"
        )
    
    def log_scheduler_event(self, event: str, job_id: Optional[str] = None,
                           **kwargs) -> None:
        """Log scheduler events."""
        self.info(
            f"Scheduler event: {event}",
            event=event,
            job_id=job_id,
            event_type="scheduler",
            **kwargs
        )
    
    def log_config_change(self, config_key: str, old_value: Any, 
                         new_value: Any) -> None:
        """Log configuration changes."""
        self.info(
            f"Configuration changed: {config_key}",
            config_key=config_key,
            old_value=old_value,
            new_value=new_value,
            event_type="config_change"
        )
    
    def log_system_event(self, event: str, **kwargs) -> None:
        """Log system-level events."""
        self.info(
            f"System event: {event}",
            event=event,
            event_type="system",
            **kwargs
        )


# Global logger instance
logger = UptimeLogger()
