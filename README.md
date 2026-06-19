# REsearch AI

A FastAPI + LangChain research dashboard using Mistral AI.

## Local setup

1. Create and activate virtual environment:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` with:
   ```bash
   MISTRAL_API_KEY=your_mistral_key
   TAVILY_API_KEY=your_tavily_key
   ```
4. Run app:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## GitHub auto-deploy

On push to `master`, GitHub Actions will:
- install Python dependencies
- run a basic Python syntax check
- build Docker image

To deploy automatically from GitHub, connect the repository to a container host or cloud provider and use the generated Docker image.

## Docker

Build locally:
```bash
docker build -t research-ai:latest .
```
Run locally:
```bash
docker run --env MISTRAL_API_KEY=$MISTRAL_API_KEY --env TAVILY_API_KEY=$TAVILY_API_KEY -p 8000:8000 research-ai:latest
```
