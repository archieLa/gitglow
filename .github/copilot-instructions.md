# GitGlow - Copilot Instructions

This is GitGlow, a GitHub LED matrix display project for Raspberry Pi Zero.

## Project Overview
- **Hardware**: 8x32 WS2812B LED matrix (showing 7x32 GitHub contribution graph)
- **Platform**: Raspberry Pi Zero with Python
- **Features**: GitHub API integration, web configuration interface, captive portal setup
- **Display**: GitHub contribution graph + LED notification bar for PR events

## Development Guidelines
- Use Python for all core functionality
- Follow Raspberry Pi GPIO best practices
- Implement smart GitHub API rate limiting (5000 req/hour limit)
- Create modular, testable code structure
- Include comprehensive documentation

## Key Components
- LED matrix controller (WS2812B)
- GitHub API client with rate limiting
- Web interface for configuration
- Captive portal for WiFi setup
- Systemd service for auto-start

## Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Include docstrings for all classes and functions
- Implement proper error handling and logging