import re
import program_closer
import opener_decision_maker

def open_or_close(command, args=None):
    if args is None:
        args = []

    # if .exe is found → close/kill the program
    if re.search(r"\.exe$", command):
        return program_closer.kill_program(command)
    else:
        # Otherwise, it's an open/system/info command
        return opener_decision_maker.opener(command, args)

