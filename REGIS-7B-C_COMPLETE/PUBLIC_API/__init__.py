"""
REGIS-7B-C Public API
Quantum-Floor AI - Encrypted Language Model

This module provides the public interface for REGIS-7B-C.
The model core is encrypted and protected by quantum lock.
"""

from .regis_api import RegisModel, RegisConfig, generate, chat, text_to_speech

__version__ = "1.0.0"
__author__ = "Quantum-Floor AI"
__license__ = "Commercial - See LICENSE_COMMERCIAL.md"

__all__ = [
    "RegisModel",
    "RegisConfig",
    "generate",
    "chat",
    "text_to_speech",
]
