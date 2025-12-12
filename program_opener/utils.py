import platform
import subprocess
import shlex
import sys

def get_os():
    """Returns 'windows', 'linux', or 'darwin' (for macOS)."""
    system = platform.system().lower()
    return system if system in ['windows', 'linux', 'darwin'] else 'unknown'

def run_os_command(command_dict, *args):
    """
    Runs a command based on the detected OS.
    
    :param command_dict: A dict with keys 'windows', 'linux', 'darwin'.
                         The value can be a string or a list of strings.
    :param args: Additional arguments to be appended to the command.
    """
    os_name = get_os()
    command_base = command_dict.get(os_name)
    
    if not command_base:
        print(f"No command specified for OS: {os_name}")
        return
        
    # Ensure command_base is a list
    if isinstance(command_base, str):
        command_list = shlex.split(command_base)
    else:
        command_list = list(command_base) # Make a copy
        
    # Add any extra arguments
    command_list.extend(args)
    
    print(f"Executing ({os_name}): {' '.join(command_list)}")
    
    try:
        if os_name == 'windows':
            # Use Popen for 'start' commands to run asynchronously
            # and avoid blocking the main thread.
            if command_list[0] == 'start':
                subprocess.Popen(command_list, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            # For other commands like 'control', run and wait
            else:
                subprocess.run(command_list, check=True, shell=True)
        else:
            # Linux/macOS are safer without shell=True and Popen is good
            subprocess.Popen(command_list)
            
    except Exception as e:
        print(f"Failed to execute command: {e}")