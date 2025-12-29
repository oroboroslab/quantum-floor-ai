"""
AXIS-7B-C Public API
Quantum-Floor AI - Ultra-Fast Encrypted Language Model

This module provides the public interface for AXIS-7B-C.
Optimized for <20ms latency selection-to-speech.
"""

from .axis_api import AxisModel, AxisConfig, instant_speech, selection_to_speech

__version__ = "1.0.0"
__author__ = "Quantum-Floor AI"
__license__ = "Commercial - See LICENSE_COMMERCIAL.md"

__all__ = [
    "AxisModel",
    "AxisConfig",
    "instant_speech",
    "selection_to_speech",
]
