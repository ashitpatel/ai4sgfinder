"""Chat with AI4SG Finder through the Anthropic API.

    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python3 examples/claude_chat.py
"""

import os
from pathlib import Path

import anthropic

SYSTEM = (Path(__file__).resolve().parent.parent / "dist" / "all-in-one.md").read_text()
MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

client = anthropic.Anthropic()
history = []

print("AI4SG Finder (Claude). Describe your allocation problem; Ctrl-D to quit.\n")
while True:
    try:
        user = input("you> ").strip()
    except EOFError:
        break
    if not user:
        continue
    history.append({"role": "user", "content": user})
    response = client.messages.create(
        model=MODEL, max_tokens=8000, system=SYSTEM, messages=history
    )
    reply = "".join(block.text for block in response.content if block.type == "text")
    history.append({"role": "assistant", "content": reply})
    print(f"\nfinder> {reply}\n")
