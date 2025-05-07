import os
import sys
import argparse
from textx import metamodel_from_file   # DSL parsing helper
from dotenv import load_dotenv          # grabs API from .env
import openai                           


# Read the .env file automatically so OPENAI_API_KEY is available
load_dotenv()


# prompt registry
PROMPTS = {
    "forge_tale": (
        "Tell a short story a Nord blacksmith in Whiterun might share while "
        "hammering at the Skyforge. It should feel gritty and authentic, with "
        "references to Nordic smithing traditions."
    ),
    "dragon_whisper": (
        "Describe a recent dragon sighting near Skyrim’s holds as though a "
        "panicked villager is warning the Dragonborn. Include the dragon’s "
        "name in Dovahzul and the hold it attacked."
    ),
    "bandit_rumor": (
        "Share a rumor about bandit activity along one of Skyrim’s major roads "
        "that a town guard might mention while on patrol."
    ),
    "fizzbuzz": "Print FizzBuzz from 1‑100, comma‑separated."
}


#
# this is where we "talk" to the OpenAI API
def ask_openai(prompt):
    # Send a prompt to chat completions and return the reply text
    print(f"-- sending to OpenAI => {prompt[:50]}…")

    client = openai.OpenAI()   # reads OPENAI_API_KEY from the environment
    reply = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": prompt}]
    )

    return reply.choices[0].message.content.strip()


def run_dialogue(model):
    # this is the main loop where we iterate over NPC blocks and interact
    for npc in model.npcs:
        print(f"\n=== NPC: {npc.name} ===")

        # step through everything written inside the NPC block
        for stmt in npc.statements:

            # simple “line” (no api call)
            if stmt.__class__.__name__ == "Line":
                if getattr(stmt, "aiFlag", False):         # was the line marked @ai?
                    print(ask_openai(stmt.text))           # dynamic answer
                else:
                    print(stmt.text)                       # plain text
                continue                                   # next statement

            # choice block
            if stmt.__class__.__name__ == "Choice":
                # show menu
                for index, opt in enumerate(stmt.options, start=1):
                    print(f"{index}. {opt.display}")

                # keep asking until we get a valid number
                while True:
                    try:
                        sel_index = int(input("Select option: ")) - 1
                        chosen = stmt.options[sel_index]
                        break
                    except (ValueError, IndexError):
                        print("Please enter a valid number.")

                # decide what to print back to the user
                if getattr(chosen, "aiCall", None):
                    # dynamic AI response
                    key = (getattr(chosen.aiCall, "promptKey", None)
                           or getattr(chosen.aiCall, "key", None))
                    if key in PROMPTS:
                        print(ask_openai(PROMPTS[key]))
                    else:
                        print(f"(Unknown prompt key '{key}'.)")

                elif getattr(chosen, "target", ""):
                    # hard‑wired reply ─
                    print(chosen.target)

                else:
                    print("(No response defined.)")


def main():
    parser = argparse.ArgumentParser(description="Run an .npcflow script")
    parser.add_argument("script", help="Path to .npcflow file")
    args = parser.parse_args()

    # make sure we actually have an API key
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY missing – add it to .env")
        sys.exit(1)

    mm = metamodel_from_file("grammar.npcflow")

    # parse the user supplied script into a model object
    model = mm.model_from_file(args.script)

    run_dialogue(model)


if __name__ == "__main__":
    main()
