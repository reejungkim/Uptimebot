"""
HTTP client module for uptime monitoring.

This module provides functionality to make HTTP requests
and check website availability.
"""

import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time


class UptimeHTTPClient:
    """HTTP client for uptime monitoring with retry logic."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the HTTP client.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def check_url(self, url: str, method: str = "GET", 
                  headers: Optional[Dict[str, str]] = None,
                  data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Check if a URL is accessible.
        
        Args:
            url: URL to check
            method: HTTP method to use
            headers: Optional headers to send
            data: Optional data to send with the request
            
        Returns:
            Dictionary containing check results
        """
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'success': 200 <= response.status_code < 400,
                'error': None,
                'timestamp': time.time()
            }
            
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                'url': url,
                'status_code': None,
                'response_time': response_time,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def check_multiple_urls(self, urls: list, method: str = "GET",
                           headers: Optional[Dict[str, str]] = None) -> list:
        """
        Check multiple URLs concurrently.
        
        Args:
            urls: List of URLs to check
            method: HTTP method to use
            headers: Optional headers to send
            
        Returns:
            List of check results
        """
        results = []
        for url in urls:
            result = self.check_url(url, method, headers)
            results.append(result)
        
        return results
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
