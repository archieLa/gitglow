# GitGlow 🌟

A beautiful GitHub LED matrix display for Raspberry Pi Zero that shows your GitHub contribution graph and lights up with pull request notifications.

## ✨ Features

- **7x32 LED Matrix**: Displays GitHub contribution graph (like github.com)
- **LED Notification Bar**: Lights up for PR events (open, merge, comments)
- **Web Interface**: Easy configuration through captive portal
- **Smart Rate Limiting**: Stays within GitHub's 5,000 requests/hour limit
- **Auto-Setup**: Captive portal for WiFi and GitHub token configuration
- **Raspberry Pi Zero**: Optimized for minimal hardware

## 🛠 Hardware Requirements

- Raspberry Pi Zero W/WH
- 8x32 WS2812B LED Matrix (256 pixels)
- MicroSD card (16GB+)
- 5V power supply (3A recommended)
- Optional: LED strip for notification bar

## 📦 Installation

### Quick Setup
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/gitglow/main/scripts/install.sh | bash
```

### Manual Installation
1. Flash Raspberry Pi OS Lite to SD card
2. Enable SSH and WiFi
3. Clone this repository
4. Run installation script
5. Configure through web interface

## 🔧 Configuration

1. Connect to `GitGlow-Setup` WiFi network
2. Open browser (captive portal should appear)
3. Enter your WiFi credentials
4. Add GitHub personal access token
5. Select repositories to monitor

## 🎯 Project Structure

```
gitglow/
├── src/gitglow/           # Core application
│   ├── api/              # GitHub API client
│   ├── display/          # LED matrix control
│   ├── web/              # Web interface
│   └── config/           # Configuration management
├── docs/                 # Documentation
├── hardware/             # Wiring diagrams
├── scripts/              # Installation scripts
├── config/               # Configuration files
└── tests/                # Test suite
```

## 🚀 Development

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

### Hardware Testing
```bash
# Test LED matrix without GitHub API
python src/gitglow/display/test_matrix.py

# Test GitHub API integration
python src/gitglow/api/test_github.py
```

## 📊 GitHub API Usage

GitGlow uses a smart polling strategy to stay within rate limits:

- **Commits**: Every 15 minutes (4 requests/hour)
- **Pull Requests**: Every 2 minutes (30 requests/hour)
- **Review Comments**: Every 1-5 minutes (12-60 requests/hour)
- **Total**: ~94 requests/hour (well under 5,000 limit)

## 🎨 Customization

- **Colors**: Modify GitHub green gradient
- **Polling**: Adjust update frequencies
- **Repositories**: Select which repos to monitor
- **Display**: Configure brightness and effects

## 📋 License

GPL v3 License - see [LICENSE](LICENSE) for details.

**Commercial Use**: You can sell GitGlow hardware products! The GPL protects the software from being used in proprietary products while allowing you to build and sell complete devices.

**DIY Friendly**: Hobbyists and makers can freely use, modify, and share improvements to the code.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

- [Issues](https://github.com/yourusername/gitglow/issues)
- [Discussions](https://github.com/yourusername/gitglow/discussions)
- [Wiki](https://github.com/yourusername/gitglow/wiki)

---

*Built with AI assistance, guided by experienced human engineering.* 🤖⚡  
Made with ❤️ for developers who love to see their code come to life!