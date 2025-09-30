import shlex
import subprocess

def run_command_safe (final_cmd):
    print(f"\n final command: {final_cmd}")
    confirm = input("do you want to run this command? [y/N]").strip().lower()
    if confirm not in ("y" or "yes"):
        print("command cancelled")
        return
    
    try :
        args = shlex.split(final_cmd)
        result = subprocess.run(args, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("stredd: ", result.stderr)
            
    except Exception as e:
        print("error while running the command: ", e)