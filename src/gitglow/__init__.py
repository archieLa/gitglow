"""
GitGlow - GitHub LED Matrix Display
===================================

A beautiful GitHub activity visualizer for Raspberry Pi Zero using
an 8x32 WS2812B LED matrix to display contribution graphs and 
real-time pull request notifications.

Author: GitGlow Team
License: MIT
"""

__version__ = "0.1.0"
__author__ = "GitGlow Team"
__license__ = "MIT"

from .main import GitGlowApp

__all__ = ["GitGlowApp"]