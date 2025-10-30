/**
 * @file IMatrixWriter.h
 * @brief Abstract LED matrix interface for GitGlow
 * 
 * This interface allows GitGlow to work with different LED matrix
 * implementations, libraries, and hardware configurations.
 */

#ifndef IMATRIXWRITER_H
#define IMATRIXWRITER_H

#include <stdint.h>

namespace GitGlow {

/**
 * @brief RGB Color structure
 */
struct Color {
    uint8_t r, g, b;
    
    Color() : r(0), g(0), b(0) {}
    Color(uint8_t red, uint8_t green, uint8_t blue) : r(red), g(green), b(blue) {}
    
    // Convert to 32-bit color value
    uint32_t to32bit() const {
        return ((uint32_t)r << 16) | ((uint32_t)g << 8) | b;
    }
    
    // Create from 32-bit color value
    static Color from32bit(uint32_t color) {
        return Color((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF);
    }
};

/**
 * @brief Matrix dimensions structure
 */
struct MatrixDimensions {
    int width;
    int height;
    int totalPixels;
    
    MatrixDimensions(int w, int h) : width(w), height(h), totalPixels(w * h) {}
};

/**
 * @brief Abstract LED matrix writer interface
 * 
 * Different implementations can use various libraries:
 * - FastLED
 * - NeoPixelBus
 * - AdaFruit NeoPixel
 * - rpi_ws281x (Raspberry Pi)
 * - Custom implementations
 */
class IMatrixWriter {
public:
    virtual ~IMatrixWriter() = default;

    // Initialization
    virtual bool init(int dataPin, const MatrixDimensions& dimensions) = 0;
    virtual bool isInitialized() const = 0;

    // Pixel Control
    virtual void setPixel(int x, int y, const Color& color) = 0;
    virtual void setPixel(int index, const Color& color) = 0;
    virtual Color getPixel(int x, int y) const = 0;
    virtual Color getPixel(int index) const = 0;

    // Display Control
    virtual void show() = 0;
    virtual void clear() = 0;
    virtual void fill(const Color& color) = 0;

    // Brightness Control
    virtual void setBrightness(uint8_t brightness) = 0;
    virtual uint8_t getBrightness() const = 0;

    // Matrix Properties
    virtual MatrixDimensions getDimensions() const = 0;
    virtual int getWidth() const = 0;
    virtual int getHeight() const = 0;
    virtual int getTotalPixels() const = 0;

    // Coordinate Helpers
    virtual int coordsToIndex(int x, int y) const = 0;
    virtual void indexToCoords(int index, int& x, int& y) const = 0;
    virtual bool isValidCoord(int x, int y) const = 0;

    // Buffer Operations
    virtual void startFrame() = 0;
    virtual void endFrame() = 0;
    virtual void setFrameRate(int fps) = 0;

    // Advanced Features (optional)
    virtual void setGammaCorrection(bool enabled) = 0;
    virtual void setColorOrder(const std::string& order) = 0; // "RGB", "GRB", etc.
    
    // Information
    virtual std::string getDriverName() const = 0;
    virtual std::string getLibraryVersion() const = 0;
};

/**
 * @brief Common GitHub contribution colors
 */
namespace GitHubColors {
    const Color BACKGROUND(22, 27, 34);      // GitHub dark background
    const Color NO_CONTRIB(22, 27, 34);      // No contributions
    const Color LEVEL_1(14, 68, 41);         // 1-3 contributions
    const Color LEVEL_2(0, 109, 50);         // 4-6 contributions  
    const Color LEVEL_3(38, 166, 65);        // 7-9 contributions
    const Color LEVEL_4(57, 211, 83);        // 10+ contributions
    
    // Notification colors
    const Color PR_OPENED(33, 136, 255);     // Blue
    const Color PR_MERGED(40, 167, 69);      // Green
    const Color PR_CLOSED(220, 53, 69);      // Red
    const Color REVIEW_COMMENT(255, 193, 7); // Orange
}

} // namespace GitGlow

#endif // IMATRIXWRITER_H