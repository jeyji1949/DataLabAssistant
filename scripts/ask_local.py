import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.storage import load_from_sqlite
from src.assistant_local import ask_question_local

table = load_from_sqlite("data/clean/lab.db")

question = input("Your question: ")
answer = ask_question_local(question, table)

print()
print("Answer:", answer)