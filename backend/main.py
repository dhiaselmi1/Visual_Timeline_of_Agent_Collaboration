from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents import devil_agent, insight_agent, research_agent, summarizer_agent
from agents.base import get_topic_log

app = FastAPI(title="Agent Collaboration API")

# ---------- Request Models ----------
class RunAgentRequest(BaseModel):
    topic: str
    query: Optional[str] = None   # for research agent


# ---------- Routes ----------
@app.get("/")
def root():
    return {"message": "Agent Collaboration API is running 🚀"}


@app.post("/run/{agent_name}")
def run_agent(agent_name: str, request: RunAgentRequest):
    """
    Run a specific agent on a topic.
    """
    topic = request.topic

    if agent_name == "Devil":
        output = devil_agent.run(topic)
    elif agent_name == "Insight":
        output = insight_agent.run(topic)
    elif agent_name == "Research":
        if not request.query:
            raise HTTPException(status_code=400, detail="Research agent requires a query")
        output = research_agent.run(topic, request.query)
    elif agent_name == "Summarizer":
        output = summarizer_agent.run(topic)
    else:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_name}")

    return {"agent": agent_name, "topic": topic, "output": output}


@app.get("/logs/{topic}")
def get_logs(topic: str):
    """
    Retrieve all logs for a given topic.
    """
    logs = get_topic_log(topic)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this topic")
    return {"topic": topic, "logs": logs}
