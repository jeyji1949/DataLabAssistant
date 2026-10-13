import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.storage import load_from_sqlite
from src.assistant import ask_question

table = load_from_sqlite("data/clean/lab.db")

question = input("Your question: ")
answer = ask_question(question, table)

print()
print("Answer:", answer)