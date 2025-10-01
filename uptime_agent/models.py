"""
Data models for uptime monitoring.

This module defines the data structures used throughout
the uptime monitoring system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CheckStatus(Enum):
    """Status of an uptime check."""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    ERROR = "error"


class NotificationType(Enum):
    """Type of notification to send."""
    EMAIL = "email"
    WEBHOOK = "webhook"
    CONSOLE = "console"


@dataclass
class UptimeCheck:
    """Represents a single uptime check result."""
    url: str
    status: CheckStatus
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'url': self.url,
            'status': self.status.value,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat(),
            'retry_count': self.retry_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UptimeCheck':
        """Create from dictionary."""
        return cls(
            url=data['url'],
            status=CheckStatus(data['status']),
            status_code=data.get('status_code'),
            response_time=data.get('response_time'),
            error_message=data.get('error_message'),
            timestamp=datetime.fromisoformat(data['timestamp']),
            retry_count=data.get('retry_count', 0)
        )


@dataclass
class MonitoringTarget:
    """Represents a URL to monitor."""
    url: str
    name: str
    enabled: bool = True
    check_interval: int = 5  # minutes
    timeout: int = 30  # seconds
    max_retries: int = 3
    expected_status_codes: List[int] = field(default_factory=lambda: [200])
    headers: Dict[str, str] = field(default_factory=dict)
    method: str = "GET"
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'url': self.url,
            'name': self.name,
            'enabled': self.enabled,
            'check_interval': self.check_interval,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'expected_status_codes': self.expected_status_codes,
            'headers': self.headers,
            'method': self.method,
            'data': self.data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MonitoringTarget':
        """Create from dictionary."""
        return cls(
            url=data['url'],
            name=data['name'],
            enabled=data.get('enabled', True),
            check_interval=data.get('check_interval', 5),
            timeout=data.get('timeout', 30),
            max_retries=data.get('max_retries', 3),
            expected_status_codes=data.get('expected_status_codes', [200]),
            headers=data.get('headers', {}),
            method=data.get('method', 'GET'),
            data=data.get('data')
        )


@dataclass
class NotificationConfig:
    """Configuration for notifications."""
    type: NotificationType
    enabled: bool = True
    email_config: Optional[Dict[str, Any]] = None
    webhook_config: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'type': self.type.value,
            'enabled': self.enabled,
            'email_config': self.email_config,
            'webhook_config': self.webhook_config
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NotificationConfig':
        """Create from dictionary."""
        return cls(
            type=NotificationType(data['type']),
            enabled=data.get('enabled', True),
            email_config=data.get('email_config'),
            webhook_config=data.get('webhook_config')
        )


@dataclass
class UptimeStats:
    """Statistics for uptime monitoring."""
    url: str
    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    average_response_time: float = 0.0
    uptime_percentage: float = 0.0
    last_check: Optional[datetime] = None
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    
    def update(self, check: UptimeCheck) -> None:
        """Update stats with a new check result."""
        self.total_checks += 1
        self.last_check = check.timestamp
        
        if check.status == CheckStatus.SUCCESS:
            self.successful_checks += 1
            self.last_success = check.timestamp
        else:
            self.failed_checks += 1
            self.last_failure = check.timestamp
        
        # Update average response time
        if check.response_time is not None:
            if self.average_response_time == 0.0:
                self.average_response_time = check.response_time
            else:
                self.average_response_time = (
                    (self.average_response_time * (self.total_checks - 1) + check.response_time) 
                    / self.total_checks
                )
        
        # Update uptime percentage
        if self.total_checks > 0:
            self.uptime_percentage = (self.successful_checks / self.total_checks) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'url': self.url,
            'total_checks': self.total_checks,
            'successful_checks': self.successful_checks,
            'failed_checks': self.failed_checks,
            'average_response_time': self.average_response_time,
            'uptime_percentage': self.uptime_percentage,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'last_success': self.last_success.isoformat() if self.last_success else None,
            'last_failure': self.last_failure.isoformat() if self.last_failure else None
        }
