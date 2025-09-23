import argparse
from .ai_engine import load_commands, build_index, find_best_match, suggest_valid_command, fill_placeholders
import subprocess
from .executor import run_command_safe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+", help="Command you want to run in plain English")
    parser.add_argument("--run", action="store_true", help="Actually run the command")
    parser.add_argument("--simulate", action="store_true", help="Dry run, show command but don’t execute")
    parser.add_argument("--yes", action="store_true", help="Auto-confirm without asking")
    args = parser.parse_args()

    query_text = " ".join(args.query)

    # Step 1: Load commands + embeddings
    commands = load_commands("cli_assistant/commands.yaml")
    index = build_index(commands)

    # Step 2: Match intent
    match = find_best_match(query_text, index)
    if not match:
        print("❌ No match found.")
        return

    cmd_entry = match["entry"]
    template = cmd_entry["command_template"]

    # Step 3: Fill placeholders
    final_command = template
    for key in ["path", "file", "user"]:  # keeping it simple for now
        if "{" + key + "}" in final_command:
            val = input(f"value of '{key}': ").strip()
            final_command = final_command.replace("{" + key + "}", val or "")

    print(f"\nI think you want : {final_command}")
    print(f" (matched intent: {cmd_entry['id']}, score={match['score']:.2f})")

    # Step 4: Run safely if requested
    if args.run:
        run_command_safe(
            final_command,
            entry=cmd_entry,
            simulate=args.simulate,
            auto_confirm=args.yes
        )


""" def run_command(command_template):
    try:
        result = subprocess.run(
            command_template,
            shell= True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Error: ", result.stderr)
    except Exception as e:
        print(f" failed to run command: {e}")
    

def run_cli():
    cmds = load_commands()
    index = build_index(cmds)
    all_templates = [c["command_template"] for c in index]
    
    parser = argparse.ArgumentParser(
        description = " AI powered CLI Assistant (learn commands in plain English)"
    )
    parser.add_argument(
        "query",
        nargs = "+",
        help = "Your input (natural language or CLI commands)"
    )
    parser.add_argument(
        "--run",
        action = "store_true",
        help = "Execute the suggested command"
    )
    
    args= parser.parse_args()
    user_input = " ".join(args.query)
    
    matches = find_best_match(user_input, index, top_k=1)
    best_entry, score = matches[0]
    
    if score > 0.6 :
        print(f"\nI think you want : {best_entry["command_template"]}")
        print(f" (matched intent: {best_entry["id"]}, score={score:.2f})")
        if args.run:
            print("running command....")
            final_command = fill_placeholders(
                best_entry["command_template"],
                best_entry.get("defaults", {})
            )
            run_command(final_command)
    else: 
        correction = suggest_valid_command(user_input, all_templates)
        if correction:
            print("did you mean: {correction}")
            
            if args.run:
                print("running command....")
                run_command(correction)
        else:
            print("ah! please check ypur command, we couldn't find any suggestion :(")

# after you have best_entry, final_command (expanded with placeholders), and args
simulate = getattr(args, "simulate", False)
auto_confirm = getattr(args, "yes", False)  # --yes to skip confirmations

# Print suggestion+description
print(f"\nI think you want : {best_entry['command_template']}")
print(f" (matched intent: {best_entry['id']}, score={score:.2f})")
if best_entry.get("description"):
    print("Explanation:", best_entry["description"])

if args.run:
    final_command = fill_placeholders(best_entry["command_template"], best_entry.get("defaults", {}))
    run_command_safe(final_command, entry=best_entry, simulate=simulate, auto_confirm=auto_confirm)
"""    
if __name__ == "__main__":
    main()