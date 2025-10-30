WIP

# GitGlow 🌟

A beautiful GitHub LED matrix display for embedded platforms that shows your GitHub contribution graph and lights up with pull request notifications.

## ✨ Features

- **7x32 LED Matrix**: Displays GitHub contribution graph (like github.com)
- **LED Notification Bar**: Lights up for PR events (open, merge, comments)
- **Multi-Platform Support**: ESP32 and Raspberry Pi Zero targets
- **Web Interface**: Easy configuration through captive portal
- **Smart Rate Limiting**: Stays within GitHub's 5,000 requests/hour limit
- **Auto-Setup**: Captive portal for WiFi and GitHub token configuration
- **Cross-Platform**: Single C++ codebase for multiple embedded platforms

## 🛠 Hardware Requirements

### ESP32 Target (Recommended)
- ESP32 development board (ESP32-WROOM, NodeMCU, etc.)
- 8x32 WS2812B LED Matrix (256 pixels)
- MicroSD card (optional, for configuration storage)
- 5V power supply (3A recommended)

### Raspberry Pi Target
- Raspberry Pi Zero W/WH
- 8x32 WS2812B LED Matrix (256 pixels)
- MicroSD card (16GB+)
- 5V power supply (3A recommended)

## 📦 Installation

### Quick Setup (ESP32)
```bash
# Install ESP-IDF
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && ./install.sh && source ./export.sh

# Clone and build for ESP32
git clone https://github.com/archieLa/gitglow.git
cd gitglow
mkdir build && cd build
cmake -DTARGET_PLATFORM=ESP32 ..
make -j4
make flash
```

### Quick Setup (Raspberry Pi)
```bash
# Install dependencies
sudo apt update && sudo apt install cmake build-essential

# Clone and build for Pi
git clone https://github.com/archieLa/gitglow.git
cd gitglow
mkdir build && cd build
cmake -DTARGET_PLATFORM=RASPBERRY_PI ..
make
sudo ./gitglow
```

## 🔧 Configuration

1. Connect to `GitGlow-Setup` WiFi network
2. Open browser (captive portal should appear)
3. Enter your WiFi credentials
4. Add GitHub personal access token
5. Select repositories to monitor

## 🎯 Project Structure

```
gitglow/
├── src/
│   ├── common/              # Shared application logic
│   │   ├── github_api.cpp   # GitHub API client
│   │   ├── led_controller.cpp # LED matrix control
│   │   └── web_server.cpp   # Configuration interface
│   ├── platforms/           # Platform-specific implementations
│   │   ├── esp32/           # ESP32 platform layer
│   │   └── raspberry_pi/    # Raspberry Pi platform layer
│   └── interfaces/          # Abstract platform interfaces
├── build_configs/           # Platform build configurations
├── docs/                    # Documentation
├── hardware/                # Wiring diagrams
└── examples/                # Platform-specific examples
```

## 🚀 Development

### Build for ESP32
```bash
# Using ESP-IDF + CMake
source $IDF_PATH/export.sh
mkdir build && cd build
cmake -DTARGET_PLATFORM=ESP32 ..
make -j4
make flash monitor
```

### Build for Raspberry Pi
```bash
# Cross-platform C++ build
mkdir build && cd build
cmake -DTARGET_PLATFORM=RASPBERRY_PI ..
make -j4

# Install system service
sudo make install
```

### Adding New Platforms
1. Create new platform directory in `src/platforms/your_platform/`
2. Implement the `IPlatform` interface
3. Add build configuration in `build_configs/`
4. Update CMakeLists.txt or platformio.ini

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

- **Issues**: [GitHub Issues](https://github.com/archieLa/gitglow/issues) - Report bugs or request features
- **Email**: Create an issue for now, direct contact coming soon
- **Documentation**: Check the `docs/` folder and `CONTEXT.md` for detailed information

*Community discussions and wiki will be added once the project gains traction!*

---

*Built with AI assistance, guided by experienced human engineering.* 🤖⚡  
Made with ❤️ for developers who love to see their code come to life!