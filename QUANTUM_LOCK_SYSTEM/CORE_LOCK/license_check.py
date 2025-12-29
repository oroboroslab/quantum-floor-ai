"""
License Verification System
===========================

Runtime license validation for Quantum-Floor AI models.
"""

import os
import re
import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LicenseInfo:
    """License information."""
    is_valid: bool = False
    license_type: str = "unknown"  # trial, standard, enterprise
    model: str = "unknown"
    expires: Optional[datetime] = None
    features: list = None
    max_requests: int = 0
    hardware_locked: bool = False
    error: Optional[str] = None

    def __post_init__(self):
        if self.features is None:
            self.features = []


class LicenseChecker:
    """
    License verification and enforcement.

    Validates license keys and enforces usage limits.
    """

    # License types
    TRIAL = "trial"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"

    # Feature flags
    FEATURE_VOICE = "voice"
    FEATURE_API = "api"
    FEATURE_BATCH = "batch"
    FEATURE_UNLIMITED = "unlimited"

    def __init__(self, license_path: Optional[str] = None):
        """
        Initialize license checker.

        Args:
            license_path: Path to license file (optional)
        """
        self.license_path = Path(license_path) if license_path else None
        self._license_info: Optional[LicenseInfo] = None
        self._request_count = 0
        self._last_check = None

    def check_license_key(self, license_key: str) -> LicenseInfo:
        """
        Validate a license key.

        Args:
            license_key: The license key to validate

        Returns:
            LicenseInfo with validation results
        """
        try:
            # Parse license key format
            # Format: MODEL-TYPE-EXPIRY-CHECKSUM
            # Example: REGIS-7B-C-LICENSE-TRIAL-2025
            parts = license_key.split("-")

            if len(parts) < 3:
                return LicenseInfo(
                    is_valid=False,
                    error="Invalid license key format"
                )

            model = "-".join(parts[:3]) if len(parts) >= 3 else parts[0]
            license_type = parts[3].lower() if len(parts) > 3 else "trial"
            year = int(parts[-1]) if parts[-1].isdigit() else 2025

            # Check expiration
            expires = datetime(year, 12, 31, 23, 59, 59)
            if datetime.now() > expires:
                return LicenseInfo(
                    is_valid=False,
                    license_type=license_type,
                    model=model,
                    expires=expires,
                    error="License has expired"
                )

            # Determine features based on license type
            features = self._get_features(license_type)
            max_requests = self._get_request_limit(license_type)

            info = LicenseInfo(
                is_valid=True,
                license_type=license_type,
                model=model,
                expires=expires,
                features=features,
                max_requests=max_requests,
            )

            self._license_info = info
            return info

        except Exception as e:
            return LicenseInfo(
                is_valid=False,
                error=f"License validation error: {str(e)}"
            )

    def _get_features(self, license_type: str) -> list:
        """Get features for license type."""
        base_features = [self.FEATURE_API]

        if license_type == self.TRIAL:
            return base_features

        if license_type == self.STANDARD:
            return base_features + [self.FEATURE_VOICE, self.FEATURE_BATCH]

        if license_type == self.ENTERPRISE:
            return base_features + [
                self.FEATURE_VOICE,
                self.FEATURE_BATCH,
                self.FEATURE_UNLIMITED,
            ]

        return base_features

    def _get_request_limit(self, license_type: str) -> int:
        """Get request limit for license type."""
        limits = {
            self.TRIAL: 1000,
            self.STANDARD: 100000,
            self.ENTERPRISE: -1,  # Unlimited
        }
        return limits.get(license_type, 100)

    def check_license_file(self) -> LicenseInfo:
        """Check license from file."""
        if self.license_path is None or not self.license_path.exists():
            return LicenseInfo(
                is_valid=False,
                error="License file not found"
            )

        with open(self.license_path, "r") as f:
            content = f.read().strip()

        # Parse file format
        # Line 1: License key
        # Line 2: Expires: YYYY-MM-DD
        # Line 3: Type: trial/standard/enterprise
        lines = content.split("\n")

        if len(lines) < 1:
            return LicenseInfo(is_valid=False, error="Empty license file")

        license_key = lines[0].strip()
        return self.check_license_key(license_key)

    def check_env_license(self, env_var: str = "QUANTUM_FLOOR_LICENSE") -> LicenseInfo:
        """Check license from environment variable."""
        license_key = os.environ.get(env_var)

        if not license_key:
            return LicenseInfo(
                is_valid=False,
                error=f"Environment variable {env_var} not set"
            )

        return self.check_license_key(license_key)

    def has_feature(self, feature: str) -> bool:
        """Check if license has a specific feature."""
        if self._license_info is None:
            return False
        return feature in self._license_info.features

    def can_make_request(self) -> Tuple[bool, str]:
        """
        Check if a request can be made under current license.

        Returns:
            Tuple of (allowed, reason)
        """
        if self._license_info is None or not self._license_info.is_valid:
            return False, "No valid license"

        if self._license_info.expires and datetime.now() > self._license_info.expires:
            return False, "License expired"

        if self._license_info.max_requests > 0:
            if self._request_count >= self._license_info.max_requests:
                return False, "Request limit exceeded"

        return True, "OK"

    def record_request(self) -> None:
        """Record a request for rate limiting."""
        self._request_count += 1

    def get_usage(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "requests_made": self._request_count,
            "requests_limit": self._license_info.max_requests if self._license_info else 0,
            "requests_remaining": (
                self._license_info.max_requests - self._request_count
                if self._license_info and self._license_info.max_requests > 0
                else -1
            ),
        }

    def reset_usage(self) -> None:
        """Reset usage counters (called on license renewal)."""
        self._request_count = 0


# Convenience functions
def verify_license(license_key: str) -> bool:
    """Quick license verification."""
    checker = LicenseChecker()
    info = checker.check_license_key(license_key)
    return info.is_valid


def get_license_info(license_key: str) -> LicenseInfo:
    """Get detailed license information."""
    checker = LicenseChecker()
    return checker.check_license_key(license_key)
