from program_opener import app, system, power, info, news

def opener(command, args=None):
    """
    Executes a command based on the command string and arguments.
    Returns a result string if the command produces one (e.g., getting the time).
    """
    if args is None:
        args = []
    
    # Helper to safely get the first argument
    first_arg = args[0] if args else None
    
    # ---------------- Apps ----------------
    if command == "open_google_chrome": app.open_google_chrome()
    elif command == "google_search": app.google_search(query=first_arg)
    elif command == "open_calculator": app.open_calculator()
    elif command == "open_notepad": app.open_notepad()
    elif command == "open_file_explorer": app.open_file_explorer()
    elif command == "open_cmd": app.open_cmd()
    elif command == "open_task_manager": app.open_task_manager()
    elif command == "open_windows_media_player": app.open_windows_media_player()
    elif command == "open_control_panel": app.open_control_panel()
    elif command == "open_settings": app.open_settings()
    elif command == "write_in_notepad": app.write_in_notepad(text=first_arg)
    # ---------------- System ----------------
    elif command == "disable_wifi": system.disable_wifi()
    elif command == "enable_wifi": system.enable_wifi()
    elif command == "disable_bluetooth": system.disable_bluetooth()
    elif command == "enable_bluetooth": system.enable_bluetooth()
    elif command == "mute_volume": system.mute_volume()
    elif command == "unmute_volume": system.unmute_volume()
    elif command == "increase_volume": system.increase_volume()
    elif command == "decrease_volume": system.decrease_volume()
    elif command == "increase_brightness": system.increase_brightness()
    elif command == "decrease_brightness": system.decrease_brightness()

    # ---------------- Power / Session ----------------
    elif command == "shutdown_system": power.shutdown_system()
    elif command == "restart_system": power.restart_system()
    # ... (rest of your power commands)
    elif command == "lock_screen": power.lock_screen()
    elif command == "sign_out": power.sign_out()

    # ---------------- Base Use ----------------
    elif command == "get_time":
        return info.get_current_time() # Return the result
    
    # ---------------- Base Use ----------------
    elif command == "get_news":
        # Ensure a topic was provided before calling the function
        if first_arg:
            return news.get_news(topic=first_arg)
        else:
            return "Please specify a topic for the news."

    # ---------------- Fallback ----------------
    else: 
        print(f"⚠️ Unknown command: {command}")
        return "Sorry, I don't know how to do that."

    return None # Return None for commands that don't produce a direct text result