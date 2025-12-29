# Commercial License

## QUANTUM-FLOOR AI COMMERCIAL LICENSE AGREEMENT

**Version 1.0 | Effective Date: January 1, 2025**

### Summary

This license covers **REGIS-7B-C** and **AXIS-7B-C** models. Connection-Core is separately licensed under MIT (see CONNECTION-CORE_PUBLIC/DOCUMENTATION/LICENSE_MIT.txt).

| License Type | Duration | Requests | Price |
|--------------|----------|----------|-------|
| **Trial** | 30 days | 1,000 | Free |
| **Standard** | 1 year | 100K/month | Contact |
| **Enterprise** | Custom | Unlimited | Contact |

### 1. License Grant

Subject to the terms of this Agreement, Quantum-Floor AI grants you a non-exclusive, non-transferable license to:

- Install and use the Software on your systems
- Use the Software for commercial purposes within license scope
- Create derivative works using the Software's API outputs

### 2. Restrictions

You SHALL NOT:

- **Reverse engineer**, decompile, or attempt to extract source code
- **Remove** security features including Quantum Lock protection
- **Distribute** the Software without written authorization
- **Create** competing products based on the Software
- **Circumvent** licensing or encryption mechanisms
- **Extract** model weights or architecture details

### 3. Intellectual Property

The Software, including the proprietary 7-level architecture, compression technology, and Quantum Lock system, is protected intellectual property of Quantum-Floor AI.

### 4. Quantum Lock Protection

The Software includes Quantum Lock protection technology. You acknowledge:

- Tampering attempts may trigger automatic deactivation
- Anonymous usage data may be collected for license verification
- Violations may result in immediate license termination

### 5. Trial License Terms

Trial licenses:
- Valid for 30 days from activation
- Limited to 1,000 API calls
- For evaluation purposes only
- No commercial use permitted

### 6. Support

| License | Support Level |
|---------|---------------|
| Trial | Community only |
| Standard | Email support, response within 48 hours |
| Enterprise | Priority support, response within 4 hours |

### 7. Warranty Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. QUANTUM-FLOOR AI DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED.

### 8. Limitation of Liability

IN NO EVENT SHALL QUANTUM-FLOOR AI BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.

### 9. Termination

This Agreement terminates immediately upon:
- Expiration of license period
- Breach of any provision
- Written notice from either party

Upon termination, you must destroy all copies of the Software.

### 10. Contact

**Licensing Inquiries:**
- Email: oroboros.lab.q@gmail.com
- Web: https://oroboroslab.github.io

**Technical Support:**
- Email: oroboros.lab.q@gmail.com
- Docs: https://oroboroslab.github.io/docs

---

## Quick Reference

### License Key Format

```
MODEL-LICENSE-TYPE-YEAR
```

Examples:
- `REGIS-7B-C-LICENSE-TRIAL-2025` (Trial)
- `REGIS-7B-C-LICENSE-STANDARD-2025` (Standard)
- `AXIS-7B-C-LICENSE-ENTERPRISE-2025` (Enterprise)

### Setting License Key

```bash
# Environment variable
export REGIS_LICENSE_KEY="your-key-here"
export AXIS_LICENSE_KEY="your-key-here"

# Or universal key for both
export QUANTUM_FLOOR_LICENSE="your-key-here"
```

```python
# In code
from regis_api import RegisModel

model = RegisModel(license_key="your-key-here")
```

### Checking License Status

```python
from quantum_lock import LicenseChecker

checker = LicenseChecker()
info = checker.check_license_key("your-key-here")

print(f"Valid: {info.is_valid}")
print(f"Type: {info.license_type}")
print(f"Expires: {info.expires}")
print(f"Features: {info.features}")
```

---

**Copyright (c) 2024-2025 Oroboros Labs. All Rights Reserved.**

*By using this Software, you agree to be bound by the terms of this Agreement.*
