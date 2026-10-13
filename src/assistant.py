import json


from src.analysis import peak_od, max_growth_rate, fastest_strain




MODEL = "claude-sonnet-5-5"

SYSTEM_PROMPT = (
    "You are a lab data assistant. "
    "Answer ONLY with numbers returned by your tools. "
    "Never invent values or units. "
    "Never do calculations yourself: quote the values from the tools. "
    "Always answer in a complete sentence that names each strain "
    "and gives each value with its unit. "
    "If the tools cannot answer a question, say so clearly."
)

TOOLS = [
    {
        "name": "list_strains",
        "description": "List the names of all yeast strains in the experiment.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_strain_summary",
        "description": "Get the peak OD600 and the maximum growth rate of one strain.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strain": {
                    "type": "string",
                    "description": "Strain name, for example strain_a",
                },
            },
            "required": ["strain"],
        },
    },
    {
        "name": "get_fastest_strain",
        "description": "Find which strain has the highest maximum growth rate.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def run_tool(tool_name, tool_input, table):
    if tool_name == "list_strains":
        strains = sorted(table["strain"].unique())
        return {"strains": [str(s) for s in strains]}

    if tool_name == "get_strain_summary":
        strain = tool_input.get("strain")
        if strain not in table["strain"].values:
            return {"error": "Unknown strain: " + str(strain)}
        return {
            "strain": strain,
            "peak_od": round(peak_od(table, strain), 3),
            "max_growth_rate": round(max_growth_rate(table, strain), 3),
            "growth_rate_unit": "OD600 per hour",
        }

    if tool_name == "get_fastest_strain":
        best = str(fastest_strain(table))
        return {
            "fastest_strain": best,
            "max_growth_rate": round(max_growth_rate(table, best), 3),
            "unit": "OD600 per hour",
        }

    return {"error": "Unknown tool: " + str(tool_name)}


def ask_question(question, table):
    import anthropic  
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    for round_number in range(5):    # safety limit: at most 5 rounds
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            answer = ""
            for block in response.content:
                if block.type == "text":
                    answer = answer + block.text
            return answer

        messages.append({"role": "assistant", "content": response.content})

        # run every tool it asked for
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print("  [tool called]", block.name, block.input)
                result = run_tool(block.name, block.input, table)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,        
                    "content": json.dumps(result),
                })

        messages.append({"role": "user", "content": results})

    return "Sorry, I could not finish answering this question."