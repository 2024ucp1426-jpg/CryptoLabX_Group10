# Test Case — Insecure File Upload

Create a harmless file:

```text
sample.txt
```

Run:

```cmd
python src\vulnerable\main.py
```

Select:

```text
4. Upload Firmware
```

Source:

```text
sample.txt
```

Destination:

```text
sample.txt
```

The vulnerable implementation accepts the non-firmware file.

The secure version rejects the destination because only safe `.bin` firmware
filenames are accepted.

No malicious executable is needed for this test.
