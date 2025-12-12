from .utils import run_os_command

CMD_SHUTDOWN = {
    "windows": "shutdown /s /t 1",
    "darwin": "sudo shutdown -h now",
    "linux": "sudo shutdown -h now"
}
CMD_RESTART = {
    "windows": "shutdown /r /t 1",
    "darwin": "sudo shutdown -r now",
    "linux": "sudo shutdown -r now"
}
CMD_LOCK = {
    "windows": ["rundll32.exe", "user32.dll,LockWorkStation"],
    "darwin": "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend",
    "linux": "xdg-screensaver lock"
}
CMD_SIGN_OUT = {
    "windows": "shutdown /l",
    "darwin": "sudo pkill loginwindow", # Forceful
    "linux": "gnome-session-quit --logout --no-prompt" # GNOME specific
}


def shutdown_system():
    print("Executing shutdown. May require admin privileges (sudo) on Linux/macOS.")
    run_os_command(CMD_SHUTDOWN)

def restart_system():
    print("Executing restart. May require admin privileges (sudo) on Linux/macOS.")
    run_os_command(CMD_RESTART)

def lock_screen():
    run_os_command(CMD_LOCK)

def sign_out():
    run_os_command(CMD_SIGN_OUT)