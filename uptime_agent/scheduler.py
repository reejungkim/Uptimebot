"""
Scheduler module for uptime monitoring.

This module handles the scheduling of uptime checks and manages
the timing of monitoring tasks.
"""

import schedule
import time
from typing import Callable, Dict, Any
from datetime import datetime


class UptimeScheduler:
    """Handles scheduling of uptime monitoring tasks."""
    
    def __init__(self):
        self.jobs = {}
        self.running = False
    
    def add_job(self, job_id: str, func: Callable, interval: int, **kwargs) -> None:
        """
        Add a scheduled job.
        
        Args:
            job_id: Unique identifier for the job
            func: Function to execute
            interval: Interval in minutes
            **kwargs: Additional arguments to pass to the function
        """
        self.jobs[job_id] = {
            'func': func,
            'interval': interval,
            'kwargs': kwargs,
            'last_run': None,
            'next_run': None
        }
        
        # Schedule the job
        schedule.every(interval).minutes.do(self._execute_job, job_id)
    
    def remove_job(self, job_id: str) -> None:
        """Remove a scheduled job."""
        if job_id in self.jobs:
            del self.jobs[job_id]
            schedule.clear(job_id)
    
    def _execute_job(self, job_id: str) -> None:
        """Execute a scheduled job."""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job['last_run'] = datetime.now()
            job['next_run'] = datetime.now() + time.timedelta(minutes=job['interval'])
            
            try:
                job['func'](**job['kwargs'])
            except Exception as e:
                print(f"Error executing job {job_id}: {e}")
    
    def start(self) -> None:
        """Start the scheduler."""
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self.running = False
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status information for a job."""
        if job_id in self.jobs:
            return self.jobs[job_id]
        return {}
    
    def list_jobs(self) -> Dict[str, Dict[str, Any]]:
        """List all scheduled jobs."""
        return self.jobs.copy()
