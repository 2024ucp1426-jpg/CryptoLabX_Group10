Lab Assignment 3 — IoT Device Management
Group: 10  
Application: IoT Device Management  
Language: Python 3  
SAST Tool: Semgrep  
Interface: Console
Objective
Develop a small IoT Device Management application demonstrating the required
core functionality and three intentionally vulnerable security cases.
Core functionality
Device registration
Device status monitoring
Firmware upload
Configuration management
A small ping/diagnostic feature is included to demonstrate Command Injection.
Vulnerabilities demonstrated
Command Injection
Path Traversal
Insecure File Upload
The project contains a deliberately vulnerable version and a secure/remediated
version for before/after SAST comparison.
Project structure
```text
secure\_application/
├── src/
│   ├── vulnerable/
│   │   └── main.py
│   └── secure/
│       └── main.py
├── reports/
│   ├── vulnerability\_report.md
│   └── final\_report.md
├── screenshots/
│   └── README.md
├── sast/
│   ├── semgrep-rules.yml
│   └── README.md
├── outputs/
│   └── firmware/
├── testcases/
│   ├── command\_injection.md
│   ├── path\_traversal.md
│   └── insecure\_file\_upload.md
└── README.md
```
Requirements
Python 3.10+ and Semgrep.
Check:
```cmd
python --version
semgrep --version
```
Run vulnerable application
From `secure\_application`:
```cmd
python src\\vulnerable\\main.py
```
Run secure application
```cmd
python src\\secure\\main.py
```
Semgrep SAST
Scan vulnerable source:
```cmd
semgrep --config sast\\semgrep-rules.yml src\\vulnerable
```
Save JSON:
```cmd
semgrep --config sast\\semgrep-rules.yml src\\vulnerable --json > sast\\semgrep-before.json
```
Scan secure source:
```cmd
semgrep --config sast\\semgrep-rules.yml src\\secure
```
Save JSON:
```cmd
semgrep --config sast\\semgrep-rules.yml src\\secure --json > sast\\semgrep-after.json
```
You can also try Semgrep's automatic rules:
```cmd
semgrep --config=auto src
```
Lab workflow
Run the vulnerable application.
Demonstrate each of the three vulnerabilities with harmless local test data.
Run Semgrep and save the findings.
Record screenshots.
Run the secure application.
Run Semgrep against the secure implementation.
Compare the before/after findings.
Complete the final report with the actual scan results.
Safety
The vulnerable code is intentionally insecure and is only for a controlled
laboratory environment. Use localhost and harmless files. Do not deploy it.