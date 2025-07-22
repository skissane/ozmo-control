#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

SERVICE_NAME = "kid_manager.service"
SERVICE_DIR = Path.home() / ".config/systemd/user"
SERVICE_FILE = SERVICE_DIR / SERVICE_NAME

PYTHON_PATH = subprocess.run(["which", "python3"], capture_output=True, text=True).stdout.strip()
SCRIPT_PATH = "/home/taba/ozmo-control/kid_manager.py"

SERVICE_CONTENT = f"""\
[Unit]
Description=Kid Manager Script
After=network.target

[Service]
Type=simple
ExecStart={PYTHON_PATH} {SCRIPT_PATH}
WorkingDirectory=/home/taba/ozmo-control
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
"""

def run(cmd):
    print(f"+ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    print("Creating systemd user service...")

    # Ensure service directory exists
    SERVICE_DIR.mkdir(parents=True, exist_ok=True)

    # Write service file
    SERVICE_FILE.write_text(SERVICE_CONTENT)
    print(f"Wrote service file to {SERVICE_FILE}")

    # Reload systemd user daemon
    run("systemctl --user daemon-reload")

    # Enable and start the service
    run(f"systemctl --user enable {SERVICE_NAME}")
    run(f"systemctl --user start {SERVICE_NAME}")

    print(f"Service '{SERVICE_NAME}' enabled and started successfully.")

if __name__ == "__main__":
    main()
