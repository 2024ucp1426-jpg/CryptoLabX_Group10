# Test Case — Command Injection

## Vulnerable version

Run:

```cmd
python src\vulnerable\main.py
```

Select:

```text
6. Ping Device
```

For a harmless Windows laboratory demonstration, enter:

```text
127.0.0.1 & echo COMMAND_INJECTION_DEMO
```

The vulnerable application passes the constructed command to `os.system()`.

Expected result: the additional `echo` command may execute.

## Secure version

Run:

```cmd
python src\secure\main.py
```

Use the same input.

The secure version rejects it because the host contains characters outside the
allowed host/IP pattern.

Use localhost-only, harmless test input.
