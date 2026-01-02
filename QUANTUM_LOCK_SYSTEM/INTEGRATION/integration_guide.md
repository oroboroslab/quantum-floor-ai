# Quantum Lock Integration Guide

This guide explains how to integrate Quantum Lock protection into your AI models.

## Overview

Quantum Lock provides:
- **Fernet encryption** for model files
- **License verification** with multiple tiers
- **Integrity checking** to detect tampering
- **Self-destruct** capability for security breaches

## Quick Start

### 1. Create a Lock

```python
from CORE_LOCK.quantum_lock import QuantumLock

# Generate a new lock file
key = QuantumLock.generate_lock("model_lock.bin")
```

### 2. Encrypt Your Model

```python
from CORE_LOCK.fernet_manager import encrypt_model

# Encrypt a model file
key = encrypt_model(
    "my_model.bin",           # Source
    "my_model.bin.enc",       # Encrypted output
)
```

### 3. Integrate License Checking

```python
from CORE_LOCK.quantum_lock import QuantumLock
from CORE_LOCK.license_check import LicenseChecker

# At runtime
lock = QuantumLock("model_lock.bin", "MyModel")
checker = LicenseChecker()

# Verify license
license_info = checker.check_license_key(user_license_key)
if not license_info.is_valid:
    raise RuntimeError(f"Invalid license: {license_info.error}")

# Verify lock and decrypt
if lock.verify_license(user_license_key):
    decrypted_model = lock.decrypt(encrypted_data)
```

## Components

### QuantumLock

The main lock class for encryption/decryption:

```python
lock = QuantumLock("path/to/lock.bin", "ModelName")

# Verify license before use
if lock.verify_license(license_key):
    # Encrypt data
    encrypted = lock.encrypt(data)

    # Decrypt data
    decrypted = lock.decrypt(encrypted)

# Check status
status = lock.get_status()
print(f"Valid: {status.is_valid}")
print(f"License type: {status.license_type}")
```

### FernetManager

Low-level encryption operations:

```python
from CORE_LOCK.fernet_manager import FernetManager

manager = FernetManager()
manager.generate_key()  # Or manager.load_key(existing_key)

# Encrypt/decrypt
encrypted = manager.encrypt(data)
decrypted = manager.decrypt(encrypted)

# File operations
manager.encrypt_file("input.bin", "output.enc")
decrypted_data = manager.decrypt_to_memory("output.enc")
```

### LicenseChecker

License validation:

```python
from CORE_LOCK.license_check import LicenseChecker

checker = LicenseChecker()

# Validate license key
info = checker.check_license_key("MODEL-LICENSE-STANDARD-2025")

print(f"Valid: {info.is_valid}")
print(f"Type: {info.license_type}")
print(f"Expires: {info.expires}")
print(f"Features: {info.features}")

# Check specific features
if checker.has_feature("voice"):
    # Enable voice features
    pass

# Rate limiting
can_proceed, reason = checker.can_make_request()
if can_proceed:
    checker.record_request()
    # Process request
```

### IntegrityVerifier

File integrity verification:

```python
from CORE_LOCK.integrity_verifier import IntegrityVerifier

verifier = IntegrityVerifier("/path/to/distribution")

# Create manifest
manifest = verifier.create_manifest([
    "model.enc",
    "weights.enc",
    "config.json"
])
verifier.save_manifest("integrity.json")

# Verify later
is_valid, results = verifier.verify_manifest("integrity.json")
for result in results:
    if not result.is_valid:
        print(f"Tampered: {result.file_path}")
```

### SelfDestruct

Anti-tampering protection:

```python
from CORE_LOCK.self_destruct import get_system

# Initialize
system = get_system(protected_paths=[
    "model.enc",
    "lock.bin"
])

# Arm the system
system.arm()

# Add callback for alerts
def on_tamper(event):
    print(f"ALERT: {event.event_type}")
    # Send to security server

system.add_callback(on_tamper)

# Check integrity periodically
if not system.check_integrity():
    # Tampering detected!
    pass

# Check for debuggers
if not system.check_debugger():
    # Debugger detected!
    pass
```

## License Types

### Trial
- 30 days or 1000 requests
- Basic API access only
- No commercial use

### Standard
- 1 year
- 100,000 requests/month
- Voice, batch processing
- Commercial use permitted

### Enterprise
- Custom duration
- Unlimited requests
- All features
- Priority support

## Command Line Tools

### Encrypt Model
```bash
python INTEGRATION/encrypt_model.py model.bin model.enc --lock lock.bin
```

### Create Lock
```bash
python INTEGRATION/create_lock.py lock.bin --name MyModel
```

### Generate License
```bash
python LICENSING/license_generator.py standard --model MYMODEL --customer customer123
```

### Test Lock
```bash
python INTEGRATION/test_lock.py
```

## Best Practices

1. **Never store keys in code** - Use environment variables or secure storage
2. **Verify before decrypt** - Always call `verify_license()` first
3. **Check integrity** - Verify file hashes on startup
4. **Handle errors gracefully** - Don't reveal security details in error messages
5. **Log security events** - Record all tampering attempts
6. **Rotate keys** - Support key rotation for long-lived deployments

## Security Notes

- Encrypted files should never be decrypted to disk
- Use `decrypt_to_memory()` for runtime decryption
- Enable self-destruct in production
- Monitor for debugger attachment
- Hash all distribution files

## Support

For integration support:
- Email: oroboros.lab.q@gmail.com
- Docs: https://oroboroslab.github.io/docs
