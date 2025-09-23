import re
import shlex
import subprocess

SHELL_OPS_RE = re.compile(r'[|&;<>()$`]')
DANGEROUS_CMD_RE = re.compile(r'\b(rm|dd|mkfs|chmod|chown|truncate|shred)\b', re.I)
RM_RFR_RE = re.compile(r'\brm\s+-rf\b', re.I)

def confirm(prompt: str, default: bool = False) -> bool:
    hint = " [Y/n]: " if default else " [y/N]: "
    ans = input(prompt + hint).strip().lower()
    if not ans:
        return default
    return ans in ("y", "yes")

def is_high_risk(command: str, entry: dict | None = None) -> bool:
    if entry and entry.get("safety_level", "").lower() == "high":
        return True
    if RM_RFR_RE.search(command):
        return True
    if DANGEROUS_CMD_RE.search(command):
        return True
    return False

def needs_shell(command: str) -> bool:
    return bool(SHELL_OPS_RE.search(command))

def run_command_safe(final_command: str, entry: dict | None = None,
                     simulate: bool = False, auto_confirm: bool = False):
    print("final command:", final_command)

    if simulate:
        print("simulation mode — not executing.")
        return

    if is_high_risk(final_command, entry):
        print("⚠️ high-risk command detected.")
        if not auto_confirm and not confirm("are you absolutely sure?", default=False):
            print("cancelled by user.")
            return

    if needs_shell(final_command):
        print("⚠️ command contains shell operators (pipes/redirects).")
        if not auto_confirm and not confirm("this requires shell=True. continue?", default=False):
            print("cancelled by user.")
            return

    if not auto_confirm and not confirm("run this command now?", default=False):
        print("cancelled.")
        return

    try:
        if needs_shell(final_command):
            proc = subprocess.run(final_command, shell=True, capture_output=True, text=True)
        else:
            args = shlex.split(final_command)
            proc = subprocess.run(args, shell=False, capture_output=True, text=True)

        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print("⚠️ stderr:", proc.stderr)
    except Exception as e:
        print("failed to run command:", e)
