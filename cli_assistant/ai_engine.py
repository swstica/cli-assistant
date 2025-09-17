import yaml
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path

def load_commands(yaml_path: str = "cli_assistant/commands.yml"):
    """Loads commands from a YAML file and returns them as a list of dicts."""
    with open(yaml_path, 'r') as file:
        commands = yaml.safe_load(file)
    return commands
    

model = SentenceTransformer("all-MiniLM-L6-v2")

# building embeddings for commands

def build_index(commands):
    index = []
    
    for cmd in commands:
        texts= [cmd["intent"]]
        
        if "aliases" in cmd and cmd["aliases"]:
            texts.extend(cmd["aliases"])
            
        if "examples" in cmd and cmd["examples"]:
            texts.extend(cmd["examples"])
            
        combined_text = "".join(texts)
        
        vector = model.encode(combined_text)
        
        index.append({
            "id": cmd["id"],
            "vector": vector,
            "command_template": cmd["command_template"],
            "descrption": cmd.get("description", "")
        })
        
    return index
        
# save and load inde for speed 

def save_index(index, file_path="cli_assistant/command_index.npy"):
    vectors = np.array([entry["vector"] for entry in index])
    np.save(file_path, vectors)

def load_index(file_path="cli_assistant/command_index.npy"):
    return np.load(file_path)

if __name__ == "__main__":
    cmds = load_commands()
    index = build_index(cmds)
    print(f"built index with {len(index)} commands.")
    print("example entry:", index[0]["id"], "->", index[0]["vector"][:5], ["..."]) 
