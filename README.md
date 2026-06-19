# REsearch AI

A polished AI research dashboard built with FastAPI, LangChain, and Mistral AI. The app performs web search, page scraping, report generation, and critic evaluation to produce professional research summaries.

## Features

- Responsive static frontend UI for user input and results
- FastAPI backend serving the app and `/api/research` endpoint
- LangChain-powered agent pipeline using Mistral AI (`mistral-small`)
- Web search integration with Tavily
- URL scraping with BeautifulSoup
- Structured research report generation and critic feedback
- Docker support and GitHub Actions automation for deployment

## Repository structure

- `app.py` — FastAPI application and API route
- `agents.py` — model + prompt setup for search, reader, writer, and critic
- `pipeline.py` — orchestration of the research workflow
- `tools.py` — external tool definitions for web search and scraping
- `frontend/` — static web UI assets (`index.html`, `styles.css`, `app.js`)
- `Dockerfile` — container image definition
- `.github/workflows/deploy.yml` — GitHub Actions automation
- `requirements.txt` — Python dependencies

## Local setup

1. Create the virtual environment:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```bash
   MISTRAL_API_KEY=your_mistral_key
   TAVILY_API_KEY=your_tavily_key
   ```
4. Start the app:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Open the browser:
   ```bash
   http://127.0.0.1:8000
   ```

## Docker

Build the container:
```bash
docker build -t research-ai:latest .
```

Run the container:
```bash
docker run --env MISTRAL_API_KEY=$MISTRAL_API_KEY --env TAVILY_API_KEY=$TAVILY_API_KEY -p 8000:8000 research-ai:latest
```

## GitHub Actions deploy

This repository includes a workflow at `.github/workflows/deploy.yml` that triggers on `push` to `master`.
It will:

- checkout the repository
- install Python 3.13
- install dependencies
- run a basic Python syntax check
- build a Docker image

> Note: To complete automatic deployment, connect this repo to a cloud host or container registry such as Render, Railway, Fly.io, or any Docker-ready platform.

## Environment variables

- `MISTRAL_API_KEY` — required for Mistral AI calls
- `TAVILY_API_KEY` — required for Tavily web search

## Notes

- Keep `.env` out of version control (already listed in `.gitignore`).
- If you want to use a different model later, update `agents.py` and ensure the model provider matches the available integration.

## Optional upgrade paths

- Add a production-grade process manager like `gunicorn`
- Add unit tests for API and pipeline behavior
- Add frontend state loading indicators and history
- Connect to a hosted registry to auto-deploy Docker images
