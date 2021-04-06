# -*- coding: utf-8 -*-
from loguru import logger as log
import uvicorn
from fastapi import FastAPI
import iscc_index
from iscc_index.config import ISCC_INDEX_ALLOWED_ORIGINS
from starlette.middleware.cors import CORSMiddleware
import iscc

app = FastAPI(
    title="ISCC Index API",
    version=iscc_index.__version__,
    description="Microservice for indexing and searching ISCC Codes.",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ISCC_INDEX_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add", tags=["add"])
def add(iscc_obj: iscc.ISCC):
    """Add an ISCC to the index."""
    key = app.state.index.add(iscc_obj)
    return {"added": key}


@app.post("/query", response_model=iscc.QueryResult, tags=["query"])
def add(iscc_obj: iscc.ISCC, k: int = 10, ct: int = 10, ft: int = 10):
    """Query ISCC for nearest neighbors."""
    qr = app.state.index.query(iscc_obj, k, ct, ft)
    return qr


@app.get("/stats", tags=["stats"])
def stats():
    """Return index statistics."""
    return app.state.index.stats


@app.on_event("startup")
async def on_startup():
    app.state.options = iscc.Options()
    log.info(app.state.options)
    app.state.index = iscc.Index()


def run_server():
    uvicorn.run("iscc_index.main:app", host="127.0.0.1", port=8090, reload=False)


if __name__ == "__main__":
    uvicorn.run("iscc_index.main:app", host="127.0.0.1", port=8090, reload=True)
