# CLI Assitant

**CLI Assistant** is your local AI-powered command-line assistant.  
Type what you want in **plain English** and it suggests the correct terminal command.  
It also fixes typos when you enter a wrong command.  

No need to memorize everything — just ask the CLI.


## Features (MVP)
- **Natural Language → Commands**  
  > Example: `show me hidden files` → `ls -a`

- **Typo Correction**  
  > Example: `git sttaus` → `git status`

- **Runs Locally**  
  No external API calls. Uses lightweight AI models (Sentence Transformers + RapidFuzz). 

- **Safe Execution**  
  Commands are suggested first, and run only after confirmation.

## Project Structure

```
cli-assistant
├── cli_assitant/
│   ├── main.py           # CLI entrypoint
│   ├── ai_engine.py      # AI model (embeddings, similarity search)
│   ├── kb_loader.py      # Loads commands.yml knowledge base
│   ├── suggester.py      # Typo correction logic
│   ├── executor.py       # Executes commands safely
│   ├── utils.py          # Helper functions
│   └── commands.yml      # Command database
├── tests/                # Unit tests
├── requirements.txt
├── README.md
└── .gitignore
```