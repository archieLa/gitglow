/**
 * @file IPlatform.h
 * @brief Abstract platform interface for GitGlow
 * 
 * This interface defines the abstraction layer that allows GitGlow
 * to run on multiple embedded platforms (ESP32, Raspberry Pi, etc.)
 * by implementing platform-specific functionality.
 */

#ifndef IPLATFORM_H
#define IPLATFORM_H

#include <stdint.h>
#include <string>
#include <functional>

namespace GitGlow {

/**
 * @brief Abstract platform interface
 * 
 * Each target platform must implement this interface to provide
 * platform-specific functionality for WiFi, LEDs, web server, etc.
 */
class IPlatform {
public:
    virtual ~IPlatform() = default;

    // WiFi Management
    virtual bool initWiFi() = 0;
    virtual bool connectToWiFi(const std::string& ssid, const std::string& password) = 0;
    virtual bool startHotspot(const std::string& ssid, const std::string& password = "") = 0;
    virtual bool isWiFiConnected() = 0;
    virtual std::string getIPAddress() = 0;

    // LED Control
    virtual bool initLEDs(int pin, int numPixels) = 0;
    virtual void setPixel(int index, uint32_t color) = 0;
    virtual void setPixel(int x, int y, uint32_t color) = 0;
    virtual void showLEDs() = 0;
    virtual void clearLEDs() = 0;
    virtual void setBrightness(uint8_t brightness) = 0;

    // Web Server
    virtual bool startWebServer(int port = 80) = 0;
    virtual void stopWebServer() = 0;
    virtual void handleWebRequest(const std::string& path, 
                                 std::function<std::string(const std::string&)> handler) = 0;

    // File System
    virtual bool initFileSystem() = 0;
    virtual bool writeFile(const std::string& path, const std::string& content) = 0;
    virtual std::string readFile(const std::string& path) = 0;
    virtual bool fileExists(const std::string& path) = 0;

    // HTTP Client
    virtual std::string httpGet(const std::string& url, 
                               const std::string& headers = "") = 0;
    virtual std::string httpPost(const std::string& url, 
                                const std::string& data,
                                const std::string& headers = "") = 0;

    // System Functions
    virtual void delay(uint32_t milliseconds) = 0;
    virtual uint32_t millis() = 0;
    virtual void restart() = 0;
    virtual void enterDeepSleep(uint32_t seconds) = 0;

    // Logging
    virtual void log(const std::string& level, const std::string& message) = 0;
    virtual void logInfo(const std::string& message) = 0;
    virtual void logError(const std::string& message) = 0;
    virtual void logDebug(const std::string& message) = 0;

    // Configuration
    virtual bool saveConfig(const std::string& key, const std::string& value) = 0;
    virtual std::string loadConfig(const std::string& key, 
                                  const std::string& defaultValue = "") = 0;
    virtual void clearConfig() = 0;

    // Hardware Info
    virtual std::string getPlatformName() = 0;
    virtual std::string getChipId() = 0;
    virtual uint32_t getFreeHeap() = 0;
    virtual float getCpuFrequency() = 0;
};

} // namespace GitGlow

#endif // IPLATFORM_H