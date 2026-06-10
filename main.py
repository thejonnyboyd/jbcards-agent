import os
import json

from openai import AzureOpenAI
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview"
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def load_pulls(filepath="pulls.json"):
    with open(filepath, "r") as f:
        return json.load(f)
    
def format_prompt(data):
    pulls_list = "\n".join(
        f"- {p['player']} ({p['parallel']})" for p in data["pulls"]
    )
    return f"""
I just did a {data['box']} box break. I paid £{data['cost_gbp']} for the box
Here's what I pulled:
{pulls_list}

Give me a full ROI breakdown and recommendations on what to list, hold, or bundle.
"""

if __name__ == "__main__":
    data = load_pulls("pulls.json")
    prompt = format_prompt(data)
    run_agent(client, DEPLOYMENT, prompt)