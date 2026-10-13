import json

from ollama import chat

from src.assistant import TOOLS, SYSTEM_PROMPT, run_tool

LOCAL_MODEL = "llama3.1"

def tools_for_ollama():
    converted = []
    for tool in TOOLS:
        converted.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"],
            },
        })
    return converted


def ask_question_local(question, table):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    tools = tools_for_ollama()

    for round_number in range(5):    
        response = chat(model=LOCAL_MODEL, messages=messages, tools=tools)

        if not response.message.tool_calls:
            return response.message.content

        messages.append(response.message)

        for call in response.message.tool_calls:
            name = call.function.name
            arguments = call.function.arguments
            print("  [tool called]", name, arguments)

            result = run_tool(name, arguments, table)
            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result),
            })

    return "Sorry, I could not finish answering this question."