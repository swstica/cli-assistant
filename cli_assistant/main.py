import argparse
from .ai_engine import load_commands, build_index, find_best_match, suggest_valid_command

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
    
    args= parser.parse_args()
    user_input = " ".join(args.query)
    
    matches = find_best_match(user_input, index, top_k=1)
    best_entry, score = matches[0]
    
    if score > 0.6 :
        print(f"\nI think you want : {best_entry["command_template"]}")
        print(f" (matched intent: {best_entry["id"]}, score={score:.2f})")
    else: 
        correction = suggest_valid_command(user_input, all_templates)
        if correction:
            print("did you mean: {correction}")
        else:
            print("ah! please check ypur command, we couldn't find any suggestion :(")
    
if __name__ == "__main__":
    run_cli()