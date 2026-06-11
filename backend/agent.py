import json
from openai import AzureOpenAI
from tools import TOOL_DEFINITIONS, handle_tool_call

SYSTEM_PROMPT = """You are a sports card break ROI analyst specialising in Topps Soccer and NFL cards.
When given a box break, you:
1. Research the value of each card using current eBay active listings sorted by lowest price — treat these as conservative market estimates since they are asking prices, not confirmed sold prices
2. Calculate the overall ROI of the break
3. Give clear recommendations on what to list now, what to hold, and what to bundle
4. Always caveat that valuations are based on active listings, not sold prices

Always be concise and practical. Work in GBP."""

def run_agent(client: AzureOpenAI, deployment: str, user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content 

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            result = handle_tool_call(tool_name, tool_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })