import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pipeline import run_research_pipeline

app = FastAPI(title="Mistral Research AI", docs_url="/docs")

app.mount("/static", StaticFiles(directory="frontend"), name="static")


class ResearchRequest(BaseModel):
    topic: str


@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse("frontend/index.html")


@app.post("/api/research")
def research(request: ResearchRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic must not be empty")

    try:
        state = run_research_pipeline(topic)
        return {
            "status": "ok",
            "topic": topic,
            "search_result": state.get("search_result", ""),
            "scraped_content": state.get("scraped_content", ""),
            "final_report": state.get("final_report", ""),
            "feedback": state.get("feedback", ""),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
