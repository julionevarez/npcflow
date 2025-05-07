# NPCFlow – a Tiny Dialogue Language

**NPCFlow** is my final–project programming language.  
It lets you write simple NPC conversations in plain text and run
them with Python. In this case, I decided to do "Skyrim-Style" NPC conversations. Some lines are static, others can be generated on‑the‑fly by
OpenAI (so the dialogue feels alive).

---

## 1. Why I built it
* I love Skyrim and wanted a lightweight way to prototype NPC dialogue.  
* Traditional dialogue trees get bulky; a mini DSL keeps the script readable.  
* Adding **@ai** hooks shows how a custom language can call an external API.

---

## 2. Quick Demo

1. **Clone the repo**  
   `git clone https://github.com/julionevarez/npcflow`  
   `cd npcflow`

2. *(Optional)* **Create & activate a virtual environment**  
   `python -m venv .venv`  
   **Windows** → `.venv\Scripts\activate`  **macOS/Linux** → `source .venv/bin/activate`

3. **Install dependencies**  
   `pip install -r requirements.txt`

4. **Add your OpenAI key to a `.env` file**  
   `OPENAI_API_KEY=sk-...`

5. **Run an example script**  
   `python interpreter.py scripts/villager.npcflow`  

   You’ll be prompted with choices; the AI answers in character where the script uses **@ai**.

---

## 3. Language Cheat‑Sheet

*Program structure*

    npc "Name" {
        line "Static line." ;
        line "Ask the AI." @ai ;
        choice {
            "Player prompt?"   -> "Fixed reply." ;
            "Another prompt?"  -> @ai("dragon_whisper") ;
        }
    }

*Grammar summary*

    DialogueFile  : one or more NPC blocks
    NPC           : npc "Name" { Statement* }
    Statement     : Line | Choice
    Line          : line "text" [@ai] ;
    Choice        : choice { Option* }
    Option        : "player text" -> ("reply text" | @ai("key")) ;

---

## 4. Included Example Programs

| File | What it does |
|------|--------------|
| **villager.npcflow**   | Villager warns about dragons, bandits, and smithy tales (uses AI). |
| **blacksmith.npcflow** | Blacksmith tells a forge tale and sells items. |
| **merchant.npcflow**   | Merchant prices wares and shares rumors. |
| **guard.npcflow**      | City guard complains about duties and bandits. |
| **fizzbuzz.npcflow**   | Classic FizzBuzz (shows DSL can output non‑dialogue logic). |

---

## 5. How the Interpreter Works (high level)

1. **Parsing** – `textX` reads `grammar.npcflow` and turns your script into a Python object tree.  
2. **Walking** – `interpreter.py` walks that tree, printing each `line` or building a choice menu.  
3. **AI calls** – When it encounters `@ai("key")` it looks up the key in a small prompt registry and sends the prompt to the Chat Completions API.  
4. **Output** – The AI’s text (or fixed text) is printed back as the NPC’s reply.

---

## 6. Build & Run Your Own Script

1. Create a file in `scripts/`, for example:

        npc "Bard" {
            line "Care for a song?" ;
            choice {
                "Sure, sing!"  -> @ai("forge_tale") ;
                "Maybe later." -> "Very well, traveler." ;
            }
        }

2. Run it with:

        python interpreter.py scripts/bard.npcflow

