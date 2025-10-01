# Uptimebot

A Python-based uptime monitoring system that continuously checks website availability and provides detailed monitoring reports.

## Features

- **HTTP/HTTPS Monitoring**: Check website availability with configurable intervals
- **Flexible Scheduling**: Schedule monitoring checks with custom intervals
- **Multiple Notification Methods**: Email and webhook notifications for downtime alerts
- **Structured Logging**: Comprehensive logging with rotation and structured output
- **Database Support**: SQLite, PostgreSQL, and MySQL support for storing monitoring data
- **RESTful API**: HTTP client with retry logic and timeout handling
- **Configuration Management**: Environment-based configuration with YAML support

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Uptimebot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Quick Start

1. **Basic Usage**:
   ```python
   from uptime_agent import UptimeMonitor
   
   # Create a monitor instance
   monitor = UptimeMonitor()
   
   # Add URLs to monitor
   monitor.add_target("https://example.com", "Example Site")
   monitor.add_target("https://google.com", "Google")
   
   # Start monitoring
   monitor.start()
   ```

2. **Configuration**:
   - Copy `.env.example` to `.env`
   - Configure monitoring intervals, timeouts, and notification settings
   - Add URLs to monitor via environment variables or configuration files

## Project Structure

```
uptime_agent/
├── __init__.py          # Package initialization
├── scheduler.py         # Task scheduling functionality
├── http_client.py       # HTTP client with retry logic
├── config.py           # Configuration management
├── models.py           # Data models and structures
└── logger.py           # Structured logging

tests/                  # Unit and integration tests
requirements.txt        # Python dependencies
.env.example           # Environment configuration template
README.md              # This file
```

## Configuration

The application can be configured through:

- **Environment Variables**: Set in `.env` file
- **YAML Configuration**: Create `config.yaml` for complex configurations
- **Code Configuration**: Direct configuration in Python code

### Key Configuration Options

- `UPTIME_CHECK_INTERVAL`: Check interval in minutes (default: 5)
- `UPTIME_TIMEOUT`: Request timeout in seconds (default: 30)
- `UPTIME_MAX_RETRIES`: Maximum retry attempts (default: 3)
- `UPTIME_URLS`: Comma-separated list of URLs to monitor
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Development

1. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Code formatting**:
   ```bash
   black uptime_agent/ tests/
   ```

4. **Type checking**:
   ```bash
   mypy uptime_agent/
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository or contact the development team.
