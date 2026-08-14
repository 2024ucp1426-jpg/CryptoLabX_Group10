# Lab Assignment 3 — Final Report

## Group 10 — IoT Device Management

### 1. Objective

The objective was to develop a small console-based IoT Device Management
application and demonstrate three security vulnerabilities using Semgrep.

### 2. Technology

- Language: Python 3
- Interface: Console
- SAST: Semgrep
- Repository: CryptoLabX

### 3. Core functionalities

1. Smart device registration
2. Device status monitoring
3. Firmware upload
4. Configuration management

A diagnostic ping feature was added to demonstrate Command Injection.

### 4. Vulnerabilities

The three selected vulnerabilities were:

1. Command Injection
2. Path Traversal
3. Insecure File Upload

### 5. SAST methodology

The vulnerable implementation was scanned using custom Semgrep rules. The
findings were documented. A secure implementation was then created and scanned
again.

### 6. Remediation

**Command Injection:** replaced shell-based `os.system()` execution with
validated input and `subprocess.run()` argument lists.

**Path Traversal:** normalized the destination and verified that it remains
inside the firmware directory.

**Insecure File Upload:** restricted firmware names to safe `.bin` filenames,
checked that the source is a regular file, enforced a 10 MB maximum size, and
used a controlled destination.

### 7. Results

Fill these numbers using your actual Semgrep output:

| Vulnerability | Before | After |
|---|---:|---:|
| Command Injection | 1 | 0 |
| Path Traversal | 1 | 0 |
| Insecure File Upload | 1 | 0 |

### 8. Conclusion

The project demonstrates how insecure input handling, shell command execution,
and filesystem operations can introduce security vulnerabilities. Semgrep was
used as a static analysis tool to identify the vulnerable patterns, while the
secure implementation applies input validation, safe subprocess execution, and
controlled file handling.
