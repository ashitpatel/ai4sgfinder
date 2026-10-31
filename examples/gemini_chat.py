"""Chat with AI4SG Finder through the Gemini API.

    pip install google-genai
    export GEMINI_API_KEY=...
    python3 examples/gemini_chat.py
"""

import os
from pathlib import Path

from google import genai
from google.genai import types

SYSTEM = (Path(__file__).resolve().parent.parent / "dist" / "all-in-one.md").read_text()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

client = genai.Client()
chat = client.chats.create(
    model=MODEL, config=types.GenerateContentConfig(system_instruction=SYSTEM)
)

print("AI4SG Finder (Gemini). Describe your allocation problem; Ctrl-D to quit.\n")
while True:
    try:
        user = input("you> ").strip()
    except EOFError:
        break
    if not user:
        continue
    print(f"\nfinder> {chat.send_message(user).text}\n")
