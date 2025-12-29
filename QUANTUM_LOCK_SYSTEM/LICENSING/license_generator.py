#!/usr/bin/env python3
"""
License Generator
=================

Generates license keys for Quantum-Floor AI models.
Internal use only.
"""

import os
import sys
import hashlib
import base64
import secrets
import argparse
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass


@dataclass
class LicenseConfig:
    """License configuration."""
    model: str = "QUANTUM-FLOOR"
    license_type: str = "trial"  # trial, standard, enterprise
    duration_days: int = 365
    max_requests: int = 1000
    features: list = None
    customer_id: Optional[str] = None

    def __post_init__(self):
        if self.features is None:
            self.features = ["api"]


class LicenseGenerator:
    """
    Generates and validates license keys.

    Key Format: MODEL-TYPE-YEAR[-CUSTOMER_HASH]
    Example: REGIS-7B-C-LICENSE-STANDARD-2025-ABC123
    """

    SECRET_SALT = b"quantum_floor_license_salt_v1"  # In production, use secure storage

    def __init__(self, secret_key: Optional[bytes] = None):
        """
        Initialize generator.

        Args:
            secret_key: Secret key for signing (uses default if not provided)
        """
        self.secret_key = secret_key or self.SECRET_SALT

    def generate(self, config: LicenseConfig) -> str:
        """
        Generate a license key.

        Args:
            config: License configuration

        Returns:
            License key string
        """
        # Calculate expiration year
        expire_date = datetime.now() + timedelta(days=config.duration_days)
        expire_year = expire_date.year

        # Build base key
        parts = [
            config.model.upper(),
            "LICENSE",
            config.license_type.upper(),
            str(expire_year),
        ]

        # Add customer hash if provided
        if config.customer_id:
            customer_hash = self._hash_customer(config.customer_id)
            parts.append(customer_hash)

        license_key = "-".join(parts)

        return license_key

    def _hash_customer(self, customer_id: str) -> str:
        """Generate short hash for customer ID."""
        data = customer_id.encode() + self.secret_key
        hash_bytes = hashlib.sha256(data).digest()[:4]
        return base64.b32encode(hash_bytes).decode()[:6]

    def generate_trial(self, model: str = "QUANTUM-FLOOR") -> str:
        """Generate a trial license."""
        config = LicenseConfig(
            model=model,
            license_type="trial",
            duration_days=30,
            max_requests=1000,
            features=["api"]
        )
        return self.generate(config)

    def generate_standard(
        self,
        model: str = "QUANTUM-FLOOR",
        customer_id: Optional[str] = None
    ) -> str:
        """Generate a standard license."""
        config = LicenseConfig(
            model=model,
            license_type="standard",
            duration_days=365,
            max_requests=100000,
            features=["api", "voice", "batch"],
            customer_id=customer_id
        )
        return self.generate(config)

    def generate_enterprise(
        self,
        model: str = "QUANTUM-FLOOR",
        customer_id: str = None,
        duration_days: int = 365
    ) -> str:
        """Generate an enterprise license."""
        config = LicenseConfig(
            model=model,
            license_type="enterprise",
            duration_days=duration_days,
            max_requests=-1,  # Unlimited
            features=["api", "voice", "batch", "unlimited", "priority_support"],
            customer_id=customer_id
        )
        return self.generate(config)

    def create_license_file(
        self,
        license_key: str,
        output_path: str,
        config: Optional[LicenseConfig] = None
    ) -> None:
        """
        Create a license file.

        Args:
            license_key: The license key
            output_path: Where to save the file
            config: Optional config for additional info
        """
        # Parse key to extract info
        parts = license_key.split("-")
        license_type = parts[3].lower() if len(parts) > 3 else "trial"
        expire_year = int(parts[4]) if len(parts) > 4 else 2025

        content = f"""{license_key}
Expires: {expire_year}-12-31
Type: {license_type}
"""

        if config:
            content += f"Requests: {config.max_requests}\n"
            content += f"Features: {', '.join(config.features)}\n"

        content += """
---
Quantum-Floor AI License
https://quantum-floor.ai
"""

        with open(output_path, "w") as f:
            f.write(content)


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Generate Quantum-Floor AI licenses")
    parser.add_argument(
        "type",
        choices=["trial", "standard", "enterprise"],
        help="License type"
    )
    parser.add_argument(
        "--model",
        default="QUANTUM-FLOOR",
        help="Model name (default: QUANTUM-FLOOR)"
    )
    parser.add_argument(
        "--customer",
        help="Customer ID for standard/enterprise licenses"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=365,
        help="Duration in days (enterprise only)"
    )
    parser.add_argument(
        "--output",
        help="Output file path for license file"
    )

    args = parser.parse_args()

    generator = LicenseGenerator()

    if args.type == "trial":
        key = generator.generate_trial(args.model)
    elif args.type == "standard":
        key = generator.generate_standard(args.model, args.customer)
    else:
        key = generator.generate_enterprise(args.model, args.customer, args.duration)

    print(f"License Key: {key}")

    if args.output:
        generator.create_license_file(key, args.output)
        print(f"License file saved to: {args.output}")


if __name__ == "__main__":
    main()
