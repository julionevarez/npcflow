---
title: NPCFlow
layout: default            # this little header makes GitHub Pages render the file cleanly
---

# NPCFlow – a Tiny Dialogue Language

NPCFlow is my final‑project programming language.  
It lets you write **Skyrim‑style NPC conversations** in plain text and run them with Python.  
Some lines are static, others can be generated on‑the‑fly by OpenAI (so the dialogue feels alive).

---

## 1. Why I built it

* I love Skyrim and wanted a lightweight way to prototype NPC chatter.  
* Traditional dialogue trees are bulky; a mini DSL keeps the script readable.  
* Adding `@ai` hooks shows how a custom language can work with an API.

---

## 2. Quick Demo

```bash
# clone the repo
git clone https://github.com/<your‑user>/npcflow.git
cd npcflow

# (optional) create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# add your OpenAI key to a .env file
echo "OPENAI_API_KEY=sk‑..." > .env

# run the villager script
python interpreter.py scripts/villager.npcflow
