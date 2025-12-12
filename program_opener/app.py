from .utils import run_os_command
import urllib.parse
import pyautogui  
import time

# Define cross-platform commands
CMD_NOTEPAD = {
    "windows": "start notepad",
    "darwin": "open -a TextEdit",
    "linux": "gedit" # 'gedit' or 'kate' or 'xdg-open' for default
}
CMD_CHROME = {
    "windows": "start chrome",
    "darwin": "open -a 'Google Chrome'",
    "linux": "google-chrome" # or 'chromium-browser'
}
CMD_CALCULATOR = {
    "windows": "start calc",
    "darwin": "open -a Calculator",
    "linux": "gnome-calculator" # or 'kcalc'
}
CMD_FILE_EXPLORER = {
    "windows": "start explorer",
    "darwin": "open .",
    "linux": "xdg-open ."
}
CMD_CMD = {
    "windows": "start cmd",
    "darwin": "open -a Terminal",
    "linux": "gnome-terminal" # or 'konsole'
}
CMD_TASK_MANAGER = {
    "windows": "start taskmgr",
    "darwin": "open -a 'Activity Monitor'",
    "linux": "gnome-system-monitor"
}
CMD_MEDIA_PLAYER = {
    "windows": "start wmplayer",
    "darwin": "open -a 'Music'", # or QuickTime Player
    "linux": "rhythmbox" # or vlc
}
CMD_CONTROL_PANEL = {
    "windows": "control",
    "darwin": "open -a 'System Settings'",
    "linux": "gnome-control-center"
}
CMD_SETTINGS = {
    "windows": "start ms-settings:",
    "darwin": "open -a 'System Settings'",
    "linux": "gnome-control-center"
}

def write_in_notepad(text: str):
    """Opens a text editor and types the given text into it."""
    run_os_command(CMD_NOTEPAD)
    time.sleep(2) # Wait for app to focus
    pyautogui.typewrite(text)

def open_google_chrome():
    run_os_command(CMD_CHROME)

def google_search(query: str):
    """Opens Google Chrome and searches for the given query."""
    if not query:
        open_google_chrome()
        return
    
    search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    
    # We need to pass the URL as an argument to the base command
    run_os_command(CMD_CHROME, search_url)
    
def open_notepad():
    run_os_command(CMD_NOTEPAD)

def open_calculator():
    run_os_command(CMD_CALCULATOR)

def open_file_explorer():
    run_os_command(CMD_FILE_EXPLORER)

def open_cmd():
    run_os_command(CMD_CMD)

def open_task_manager():
    run_os_command(CMD_TASK_MANAGER)

def open_windows_media_player():
    run_os_command(CMD_MEDIA_PLAYER)

def open_control_panel():
    run_os_command(CMD_CONTROL_PANEL)

def open_settings():
    run_os_command(CMD_SETTINGS)