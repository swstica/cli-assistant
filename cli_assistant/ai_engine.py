import yaml
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm
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


#quering pipeline

def find_best_match(user_input, index, top_k):
    
    query_vec = model.encode(user_input)
    
    #comparing with all vectors in index
    scores = []
    for entry in index:
        score = np.dot(query_vec, entry["vector"]) / (norm(query_vec)* (norm(entry["vector"])))
        scores.append((entry, score))
        
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    return scores[:top_k]


if __name__ == "__main__":
    cmds = load_commands()
    index = build_index(cmds)
    print(f"built index with {len(index)} commands.")
    print("example entry:", index[0]["id"], "->", index[0]["vector"][:5], ["..."]) 
    
    #sample query
    user_query = "stop the currently running process"
    matches = find_best_match(user_query, index, top_k=3)
    
    print(f"\nQuery: {user_query}")
    for entry, score in matches:
        print(f"\nmatch: {entry['id']} | score: {score:.3f} | template: {entry['command_template']}") 
