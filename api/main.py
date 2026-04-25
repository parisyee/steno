"""Steno API — entry point."""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

from api.routers import transcriptions, search

load_dotenv()

app = FastAPI(title="Steno", docs_url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(transcriptions.router)
app.include_router(search.router)
