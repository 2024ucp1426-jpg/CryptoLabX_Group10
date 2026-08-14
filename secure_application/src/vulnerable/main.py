import os
import shutil

devices = []
FIRMWARE_DIR = "outputs/firmware"


def register_device():
    device_id = input("Device ID: ")
    name = input("Device name: ")
    device_type = input("Device type: ")
    ip = input("IP address: ")

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
    device_id = input("Device ID: ")

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
    status = input("Set status (ONLINE/OFFLINE): ")

    device["status"] = status
    print("Status updated.")


# VULNERABILITY 1: COMMAND INJECTION
# User input is directly concatenated into a shell command.
def ping_device():
    host = input("Enter IP/host to ping: ")

    command = "ping -n 1 " + host if os.name == "nt" else "ping -c 1 " + host

    print("Executing ping...")
    os.system(command)


# VULNERABILITY 2: PATH TRAVERSAL
# User-controlled filename is directly joined to the firmware directory.
#
# VULNERABILITY 3: INSECURE FILE UPLOAD
# No extension, type, size, or destination validation is performed.
def upload_firmware():
    source = input("Source firmware file: ")
    filename = input("Destination filename: ")

    destination = os.path.join(FIRMWARE_DIR, filename)

    try:
        shutil.copyfile(source, destination)
        print("Firmware uploaded to:", destination)
    except OSError as error:
        print("Upload failed:", error)


def configure_device():
    device = find_device()
    if device is None:
        return

    print("Current configuration:", device["configuration"])
    config = input("New configuration: ")

    device["configuration"] = config
    print("Configuration updated.")


def main():
    os.makedirs(FIRMWARE_DIR, exist_ok=True)

    while True:
        print("\n================================")
        print("       IoT DEVICE MANAGER")
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
