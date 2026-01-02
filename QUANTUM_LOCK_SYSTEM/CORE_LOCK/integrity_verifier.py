"""
Integrity Verification System
=============================

Verifies integrity of model files and distributions.
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class IntegrityResult:
    """Result of integrity verification."""
    is_valid: bool
    file_path: str
    expected_hash: Optional[str]
    actual_hash: Optional[str]
    error: Optional[str] = None


class IntegrityVerifier:
    """
    Verifies file integrity using cryptographic hashes.

    Supports:
    - Individual file verification
    - Manifest-based verification
    - Directory verification
    """

    ALGORITHM = "sha256"
    MANIFEST_FILE = "integrity.json"

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize verifier.

        Args:
            base_path: Base path for relative file paths
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self._manifest: Dict[str, str] = {}

    def calculate_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file.

        Args:
            file_path: Path to file

        Returns:
            Hex-encoded hash string
        """
        path = self._resolve_path(file_path)

        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _resolve_path(self, file_path: str) -> Path:
        """Resolve file path relative to base path."""
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path
        return path

    def verify_file(self, file_path: str, expected_hash: str) -> IntegrityResult:
        """
        Verify a single file.

        Args:
            file_path: Path to file
            expected_hash: Expected SHA-256 hash

        Returns:
            IntegrityResult with verification status
        """
        try:
            path = self._resolve_path(file_path)

            if not path.exists():
                return IntegrityResult(
                    is_valid=False,
                    file_path=str(path),
                    expected_hash=expected_hash,
                    actual_hash=None,
                    error="File not found"
                )

            actual_hash = self.calculate_hash(str(path))

            return IntegrityResult(
                is_valid=(actual_hash == expected_hash),
                file_path=str(path),
                expected_hash=expected_hash,
                actual_hash=actual_hash
            )

        except Exception as e:
            return IntegrityResult(
                is_valid=False,
                file_path=file_path,
                expected_hash=expected_hash,
                actual_hash=None,
                error=str(e)
            )

    def create_manifest(self, file_paths: List[str]) -> Dict[str, str]:
        """
        Create integrity manifest for files.

        Args:
            file_paths: List of file paths to include

        Returns:
            Dictionary mapping file paths to hashes
        """
        manifest = {}

        for file_path in file_paths:
            try:
                hash_value = self.calculate_hash(file_path)
                manifest[file_path] = hash_value
            except Exception as e:
                print(f"Warning: Could not hash {file_path}: {e}")

        self._manifest = manifest
        return manifest

    def save_manifest(self, output_path: Optional[str] = None) -> None:
        """
        Save manifest to file.

        Args:
            output_path: Path for manifest file
        """
        if output_path is None:
            output_path = str(self.base_path / self.MANIFEST_FILE)

        with open(output_path, "w") as f:
            json.dump({
                "algorithm": self.ALGORITHM,
                "files": self._manifest
            }, f, indent=2)

    def load_manifest(self, manifest_path: Optional[str] = None) -> Dict[str, str]:
        """
        Load manifest from file.

        Args:
            manifest_path: Path to manifest file

        Returns:
            Dictionary of file hashes
        """
        if manifest_path is None:
            manifest_path = str(self.base_path / self.MANIFEST_FILE)

        with open(manifest_path, "r") as f:
            data = json.load(f)

        self._manifest = data.get("files", {})
        return self._manifest

    def verify_manifest(
        self,
        manifest_path: Optional[str] = None
    ) -> Tuple[bool, List[IntegrityResult]]:
        """
        Verify all files in manifest.

        Args:
            manifest_path: Path to manifest file

        Returns:
            Tuple of (all_valid, list of results)
        """
        manifest = self.load_manifest(manifest_path)
        results = []
        all_valid = True

        for file_path, expected_hash in manifest.items():
            result = self.verify_file(file_path, expected_hash)
            results.append(result)
            if not result.is_valid:
                all_valid = False

        return all_valid, results

    def verify_directory(
        self,
        directory: str,
        patterns: Optional[List[str]] = None
    ) -> Tuple[bool, List[IntegrityResult]]:
        """
        Verify all files in a directory.

        Args:
            directory: Directory to verify
            patterns: Optional glob patterns to match

        Returns:
            Tuple of (all_valid, list of results)
        """
        import glob

        dir_path = self._resolve_path(directory)

        if patterns is None:
            patterns = ["**/*"]

        files = []
        for pattern in patterns:
            files.extend(glob.glob(str(dir_path / pattern), recursive=True))

        # Filter to actual files
        files = [f for f in files if os.path.isfile(f)]

        results = []
        all_valid = True

        for file_path in files:
            if file_path in self._manifest:
                result = self.verify_file(file_path, self._manifest[file_path])
                results.append(result)
                if not result.is_valid:
                    all_valid = False

        return all_valid, results


def create_distribution_manifest(
    dist_path: str,
    output_path: Optional[str] = None
) -> Dict[str, str]:
    """
    Create integrity manifest for a distribution.

    Args:
        dist_path: Path to distribution directory
        output_path: Where to save manifest

    Returns:
        The manifest dictionary
    """
    verifier = IntegrityVerifier(dist_path)

    # Find all files
    import glob
    files = glob.glob(f"{dist_path}/**/*", recursive=True)
    files = [f for f in files if os.path.isfile(f)]

    # Create manifest
    manifest = verifier.create_manifest(files)

    # Save
    if output_path:
        verifier.save_manifest(output_path)
    else:
        verifier.save_manifest()

    return manifest


def verify_distribution(dist_path: str) -> Tuple[bool, List[IntegrityResult]]:
    """
    Verify a distribution against its manifest.

    Args:
        dist_path: Path to distribution

    Returns:
        Tuple of (is_valid, results)
    """
    verifier = IntegrityVerifier(dist_path)
    return verifier.verify_manifest()
