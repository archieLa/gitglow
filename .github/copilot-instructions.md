# GitGlow - Copilot Instructions

This is GitGlow, a GitHub LED matrix display project for embedded platforms.

## Project Overview
- **Hardware**: 8x32 WS2812B LED matrix (showing 7x32 GitHub contribution graph)
- **Platforms**: ESP32 (primary) and Raspberry Pi Zero (backup)
- **Language**: C++ with multi-platform abstraction layers
- **Features**: GitHub API integration, web configuration interface, captive portal setup
- **Display**: GitHub contribution graph + LED notification bar for PR events

## Development Guidelines
- Use C++ for all core functionality with platform abstraction
- Follow embedded best practices for both ESP32 and Raspberry Pi
- Implement smart GitHub API rate limiting (5000 req/hour limit)
- Create modular, testable code structure with clear interfaces
- Include comprehensive documentation

## Key Components
- Abstract platform interface (IPlatform)
- Abstract LED matrix interface (IMatrixWriter)
- GitHub API client with rate limiting
- Web interface for configuration
- Captive portal for WiFi setup
- CMake build system with ESP-IDF integration

## Code Style
- Follow modern C++ best practices (C++17)
- Use RAII and smart pointers where appropriate
- Include comprehensive comments and documentation
- Implement proper error handling and logging
- Use consistent naming conventions across platforms