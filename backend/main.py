import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from openai import AzureOpenAI
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

class Pull(BaseModel):
    player: str
    parallel: str

class BreakRequest(BaseModel):
    box: str
    cost_gbp: float
    pulls: List[Pull]

@app.post("/analyse")
async def analyse_break(request: BreakRequest):
    pulls_list = "\n".join(
        f"- {p.player} ({p.parallel})" for p in request.pulls
    )
    prompt = f"""
I just did a {request.box} box break. I paid £{request.cost_gbp} for the box.
Here's what I pulled:
{pulls_list}

Give me a full ROI breakdown and recommendations.
"""
    result = run_agent(client, DEPLOYMENT, prompt)
    return {"result": result}