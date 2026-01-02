"""
Self-Destruct Protection System
===============================

Anti-tampering and self-destruct capabilities for Quantum Lock.
Activates when tampering is detected.
"""

import os
import sys
import hashlib
import shutil
from typing import Optional, List, Callable
from pathlib import Path
from dataclasses import dataclass
import logging


@dataclass
class TamperEvent:
    """Record of a tampering attempt."""
    timestamp: float
    event_type: str
    details: str
    severity: str  # "warning", "critical", "fatal"
    file_path: Optional[str] = None


class SelfDestructSystem:
    """
    Self-destruct and anti-tampering system.

    Monitors for:
    - File modifications
    - Debugger attachment
    - Memory inspection
    - Integrity violations

    Actions:
    - Log and alert
    - Invalidate session
    - Secure file deletion
    - Memory wipe
    """

    SEVERITY_WARNING = "warning"
    SEVERITY_CRITICAL = "critical"
    SEVERITY_FATAL = "fatal"

    def __init__(self, protected_paths: Optional[List[str]] = None):
        """
        Initialize self-destruct system.

        Args:
            protected_paths: Paths to monitor for tampering
        """
        self.protected_paths = protected_paths or []
        self._integrity_hashes: dict = {}
        self._tamper_events: List[TamperEvent] = []
        self._callbacks: List[Callable[[TamperEvent], None]] = []
        self._armed = False
        self._triggered = False

        self._logger = logging.getLogger("quantum_lock.self_destruct")

    def arm(self) -> None:
        """Arm the self-destruct system."""
        # Calculate initial integrity hashes
        for path in self.protected_paths:
            if os.path.exists(path):
                self._integrity_hashes[path] = self._calculate_hash(path)

        self._armed = True
        self._logger.info("Self-destruct system armed")

    def disarm(self) -> None:
        """Disarm the self-destruct system."""
        self._armed = False
        self._logger.info("Self-destruct system disarmed")

    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def check_integrity(self) -> bool:
        """
        Check integrity of all protected files.

        Returns:
            True if integrity is intact, False if tampering detected
        """
        if not self._armed:
            return True

        for path, expected_hash in self._integrity_hashes.items():
            if not os.path.exists(path):
                self._record_tamper(
                    "file_missing",
                    f"Protected file missing: {path}",
                    self.SEVERITY_CRITICAL,
                    path
                )
                return False

            current_hash = self._calculate_hash(path)
            if current_hash != expected_hash:
                self._record_tamper(
                    "file_modified",
                    f"Protected file modified: {path}",
                    self.SEVERITY_CRITICAL,
                    path
                )
                return False

        return True

    def check_debugger(self) -> bool:
        """
        Check if a debugger is attached.

        Returns:
            True if no debugger, False if debugger detected
        """
        try:
            # Check for common debugger indicators
            import ctypes

            # Windows: IsDebuggerPresent
            if sys.platform == "win32":
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    self._record_tamper(
                        "debugger_detected",
                        "Windows debugger detected",
                        self.SEVERITY_FATAL
                    )
                    return False

            # Linux: Check /proc/self/status for TracerPid
            if sys.platform.startswith("linux"):
                with open("/proc/self/status", "r") as f:
                    for line in f:
                        if line.startswith("TracerPid:"):
                            tracer_pid = int(line.split(":")[1].strip())
                            if tracer_pid != 0:
                                self._record_tamper(
                                    "debugger_detected",
                                    f"Linux debugger detected (PID: {tracer_pid})",
                                    self.SEVERITY_FATAL
                                )
                                return False
                            break

            return True

        except Exception:
            # If we can't check, assume it's fine
            return True

    def _record_tamper(
        self,
        event_type: str,
        details: str,
        severity: str,
        file_path: Optional[str] = None
    ) -> None:
        """Record a tampering event."""
        import time

        event = TamperEvent(
            timestamp=time.time(),
            event_type=event_type,
            details=details,
            severity=severity,
            file_path=file_path,
        )

        self._tamper_events.append(event)
        self._logger.warning(f"Tamper event: {event_type} - {details}")

        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(event)
            except Exception:
                pass

        # Auto-trigger on fatal events
        if severity == self.SEVERITY_FATAL:
            self.trigger()

    def add_callback(self, callback: Callable[[TamperEvent], None]) -> None:
        """Add a callback for tamper events."""
        self._callbacks.append(callback)

    def trigger(self) -> None:
        """
        Trigger self-destruct sequence.

        Actions:
        1. Log the event
        2. Clear sensitive data from memory
        3. Optionally delete encrypted files
        4. Exit the process
        """
        if self._triggered:
            return

        self._triggered = True
        self._logger.critical("SELF-DESTRUCT TRIGGERED")

        # Clear sensitive data
        self._clear_memory()

        # In production, could also:
        # - Send alert to security server
        # - Revoke license
        # - Delete encrypted files (commented out for safety)
        # self._secure_delete()

        # Exit process
        sys.exit(1)

    def _clear_memory(self) -> None:
        """Clear sensitive data from memory."""
        # Clear integrity hashes
        self._integrity_hashes.clear()

        # Force garbage collection
        import gc
        gc.collect()

    def _secure_delete(self) -> None:
        """Securely delete protected files."""
        for path in self.protected_paths:
            if os.path.exists(path):
                # Overwrite with random data before deletion
                size = os.path.getsize(path)
                with open(path, "wb") as f:
                    f.write(os.urandom(size))
                os.remove(path)

    def get_events(self) -> List[TamperEvent]:
        """Get all recorded tamper events."""
        return self._tamper_events.copy()

    @property
    def is_armed(self) -> bool:
        return self._armed

    @property
    def is_triggered(self) -> bool:
        return self._triggered


# Global instance
_system: Optional[SelfDestructSystem] = None


def get_system(protected_paths: Optional[List[str]] = None) -> SelfDestructSystem:
    """Get or create the global self-destruct system."""
    global _system
    if _system is None:
        _system = SelfDestructSystem(protected_paths)
    return _system
