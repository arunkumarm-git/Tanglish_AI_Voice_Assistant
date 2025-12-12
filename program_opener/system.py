from .utils import run_os_command
import pyautogui # Using pyautogui for media keys is the most reliable cross-OS method

# --- WiFi / Bluetooth ---
# These are complex, admin-level tasks that vary wildly.
# The previous Windows-only code was good, but cross-platform is harder.
# We'll provide the cross-platform commands but warn they may need sudo/admin.
CMD_WIFI_OFF = {
    "windows": "netsh interface set interface name=\"Wi-Fi\" admin=disabled",
    "darwin": "networksetup -setnetworkserviceenabled Wi-Fi off",
    "linux": "nmcli radio wifi off"
}
CMD_WIFI_ON = {
    "windows": "netsh interface set interface name=\"Wi-Fi\" admin=enabled",
    "darwin": "networksetup -setnetworkserviceenabled Wi-Fi on",
    "linux": "nmcli radio wifi on"
}
# Bluetooth is even less standardized. We'll skip implementation for now.

def disable_wifi():
    print("WARNING: Disabling WiFi. May require admin privileges.")
    run_os_command(CMD_WIFI_OFF)

def enable_wifi():
    print("WARNING: Enabling WiFi. May require admin privileges.")
    run_os_command(CMD_WIFI_ON)

def disable_bluetooth():
    print("Bluetooth control is highly platform-specific and not implemented.")

def enable_bluetooth():
    print("Bluetooth control is highly platform-specific and not implemented.")

# --- Volume and Brightness ---
# Using pyautogui to press media keys is the simplest cross-platform solution.
# This assumes the user has a keyboard with these keys.

def mute_volume():
    pyautogui.press('volumemute')

def unmute_volume():
    pyautogui.press('volumemute') # Toggles

def increase_volume():
    pyautogui.press('volumeup')

def decrease_volume():
    pyautogui.press('volumedown')

def increase_brightness():
    try:
        pyautogui.press('brightnessup')
    except Exception as e:
        print(f"Could not press brightness key: {e}")

def decrease_brightness():
    try:
        pyautogui.press('brightnessdown')
    except Exception as e:
        print(f"Could not press brightness key: {e}")