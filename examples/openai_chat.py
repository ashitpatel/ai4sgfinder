"""Chat with AI4SG Finder through the OpenAI Responses API.

    pip install openai
    export OPENAI_API_KEY=...
    python3 examples/openai_chat.py
"""

import os
from pathlib import Path

from openai import OpenAI

SYSTEM = (Path(__file__).resolve().parent.parent / "dist" / "all-in-one.md").read_text()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")

client = OpenAI()
history = []

print("AI4SG Finder (OpenAI). Describe your allocation problem; Ctrl-D to quit.\n")
while True:
    try:
        user = input("you> ").strip()
    except EOFError:
        break
    if not user:
        continue
    history.append({"role": "user", "content": user})
    response = client.responses.create(model=MODEL, instructions=SYSTEM, input=history)
    reply = response.output_text
    history.append({"role": "assistant", "content": reply})
    print(f"\nfinder> {reply}\n")
