# Test Case — Path Traversal

Create a harmless file named:

```text
sample.bin
```

Run the vulnerable application:

```cmd
python src\vulnerable\main.py
```

Select:

```text
4. Upload Firmware
```

Source:

```text
sample.bin
```

Destination:

```text
..\path_traversal_demo.txt
```

The vulnerable implementation does not verify that the normalized destination
stays inside the firmware directory.

The secure version only accepts safe `.bin` destination filenames and verifies
the resolved path remains inside `outputs/firmware`.

Use only the project directory and harmless test files.
