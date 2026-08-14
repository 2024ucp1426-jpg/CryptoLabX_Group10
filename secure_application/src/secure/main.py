import ipaddress
import os
import re
import shutil
import subprocess
from pathlib import Path

devices = []

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIRMWARE_DIR = (PROJECT_ROOT / "outputs" / "firmware").resolve()

SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,32}$")
SAFE_FILENAME = re.compile(r"^[A-Za-z0-9_-]{1,64}\.bin$")
MAX_FIRMWARE_SIZE = 10 * 1024 * 1024


def valid_device_id(value):
    return SAFE_ID.fullmatch(value) is not None


def valid_host(value):
    if len(value) > 253 or not re.fullmatch(r"[A-Za-z0-9.-]+", value):
        return False

    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        # A simple hostname allowlist for the lab.
        return all(
            0 < len(part) <= 63
            for part in value.split(".")
        )


def register_device():
    device_id = input("Device ID: ").strip()

    if not valid_device_id(device_id):
        print("Invalid device ID.")
        return

    if any(d["id"] == device_id for d in devices):
        print("Device ID already exists.")
        return

    name = input("Device name: ").strip()
    device_type = input("Device type: ").strip()
    ip = input("IP address/host: ").strip()

    if not valid_host(ip):
        print("Invalid IP/host.")
        return

    device = {
        "id": device_id,
        "name": name,
        "type": device_type,
        "ip": ip,
        "status": "OFFLINE",
        "configuration": "mode=normal;interval=60"
    }

    devices.append(device)
    print("Device registered.")


def view_devices():
    if not devices:
        print("No devices registered.")
        return

    for device in devices:
        print(
            f"ID={device['id']}, "
            f"Name={device['name']}, "
            f"Type={device['type']}, "
            f"IP={device['ip']}, "
            f"Status={device['status']}, "
            f"Configuration={device['configuration']}"
        )


def find_device():
    device_id = input("Device ID: ").strip()

    if not valid_device_id(device_id):
        print("Invalid device ID.")
        return None

    for device in devices:
        if device["id"] == device_id:
            return device

    print("Device not found.")
    return None


def check_status():
    device = find_device()
    if device is None:
        return

    print("Current status:", device["status"])
    status = input("Set status (ONLINE/OFFLINE): ").strip().upper()

    if status not in {"ONLINE", "OFFLINE"}:
        print("Invalid status.")
        return

    device["status"] = status
    print("Status updated.")


# FIX 1: COMMAND INJECTION
# Input is validated and passed as a separate subprocess argument.
# No shell is used.
def ping_device():
    host = input("Enter IP/host to ping: ").strip()

    if not valid_host(host):
        print("Invalid IP/host.")
        return

    try:
        if os.name == "nt":
            result = subprocess.run(
                ["ping", "-n", "1", host],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
        else:
            result = subprocess.run(
                ["ping", "-c", "1", host],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )

        print(result.stdout)
    except (OSError, subprocess.SubprocessError):
        print("Ping operation failed.")


# FIX 2 + FIX 3: PATH TRAVERSAL + INSECURE FILE UPLOAD
def upload_firmware():
    source_text = input("Source firmware file: ").strip()
    filename = input("Destination filename (.bin): ").strip()

    if SAFE_FILENAME.fullmatch(filename) is None:
        print("Only safe .bin firmware filenames are allowed.")
        return

    try:
        source = Path(source_text).expanduser().resolve()

        if not source.is_file():
            print("Source is not a regular file.")
            return

        if source.stat().st_size > MAX_FIRMWARE_SIZE:
            print("Firmware file is too large.")
            return

        destination = (FIRMWARE_DIR / filename).resolve()

        # Ensure the resolved destination remains inside the firmware root.
        destination.relative_to(FIRMWARE_DIR)

        shutil.copyfile(source, destination)
        print("Firmware uploaded successfully.")

    except (OSError, ValueError):
        print("Firmware upload failed.")


def configure_device():
    device = find_device()
    if device is None:
        return

    print("Current configuration:", device["configuration"])
    config = input("New configuration: ").strip()

    if len(config) > 200 or "\n" in config or "\r" in config:
        print("Invalid configuration.")
        return

    device["configuration"] = config
    print("Configuration updated.")


def main():
    FIRMWARE_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        print("\n================================")
        print("     SECURE IoT DEVICE MANAGER")
        print("================================")
        print("1. Register Device")
        print("2. View Devices")
        print("3. Check Device Status")
        print("4. Upload Firmware")
        print("5. Configure Device")
        print("6. Ping Device")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register_device()
        elif choice == "2":
            view_devices()
        elif choice == "3":
            check_status()
        elif choice == "4":
            upload_firmware()
        elif choice == "5":
            configure_device()
        elif choice == "6":
            ping_device()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
