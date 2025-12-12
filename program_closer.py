import psutil

def kill_program(program_name):
    response = ""
    found = False

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and program_name.lower() in proc.info['name'].lower():
            try:
                proc.kill()
                response += f"Killed {proc.info['name']} (PID {proc.info['pid']}) ✅\n"
                found = True
            except Exception as e:
                response += f"Error killing {proc.info['name']}: {e}\n"

    if not found:
        response += "Program not running ❌\n"
    else:
        response += "All matching programs killed ✅\n"

    return response
