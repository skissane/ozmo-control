#!/usr/bin/env python3
import subprocess
from time import sleep
from datetime import datetime, time

def run_script(script_name):
    """Run a shell script and return its output as a string."""
    try:
        result = subprocess.run(['./' + script_name], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run {script_name}: {e}")
        return None

def run_script_action(script_name):
    """Run a shell script, without capturing output."""
    try:
        subprocess.run(['./' + script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run {script_name}: {e}")

def get_expected_status():
    """Determine whether the account should be LOCKED or UNLOCKED based on time."""
    now = datetime.now()
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    current_time = now.time()

    # Weekday (Mon–Fri) before 13:00 → LOCKED
    if 0 <= weekday <= 4 and current_time < time(13, 0):
        return "LOCKED"

    # School night (Sun–Thu) after 21:15 → LOCKED
    if 0 <= weekday <= 4 or weekday == 6:  # Sunday is 6
        if current_time >= time(21, 15):
            return "LOCKED"

    # Weekend night (Fri–Sat) after 22:15 → LOCKED
    if weekday in (4,5): # Friday is 4, Saturday is 5
        if current_time >= time(22, 15):
            return "LOCKED"

    return "UNLOCKED"

def main():
    while True:
        try:
            actual_status = run_script("status.sh")
            if actual_status is None:
                raise RuntimeError("Could not get actual status")

            expected_status = get_expected_status()

            if actual_status == expected_status:
                print(f"OK: status is {actual_status} as expected")
            else:
                print(f"Changing status from {actual_status} to {expected_status}")
                if expected_status == "LOCKED":
                    run_script_action("lock.sh")
                else:
                    run_script_action("unlock.sh")

                # Re-check the status
                new_status = run_script("status.sh")
                if new_status == expected_status:
                    print(f"SUCCESS: changed status to {expected_status}")
                else:
                    print(f"ERROR: failed to change status to {expected_status}, current status is {new_status}")
        except Exception as e:
            print(f"ERROR: {e}")

        sleep(60)

if __name__ == "__main__":
    main()
