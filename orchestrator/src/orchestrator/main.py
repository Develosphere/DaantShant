from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from orchestrator.config import settings
from orchestrator.live_session import handle_live_websocket
from orchestrator.pipeline import (
    TeethAnalyzePipelineRequest,
    TeethAnalyzePipelineResponse,
    check_dependencies,
    run_teeth_analysis_pipeline,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    yield


app = FastAPI(
    title="DantShaant Orchestrator",
    version="0.2.0",
    description="Gateway — HTTP snapshot + WebSocket live video",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    deps = await check_dependencies()
    status = "ok" if all(v == "ok" for v in deps.values()) else "degraded"
    return {
        "status": status,
        "service": "orchestrator",
        "version": "0.2.0",
        "dependencies": deps,
    }


@app.post("/v1/teeth/analyze", response_model=TeethAnalyzePipelineResponse)
async def analyze_teeth(
    request: TeethAnalyzePipelineRequest,
) -> TeethAnalyzePipelineResponse:
    try:
        return await run_teeth_analysis_pipeline(request)
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text
        try:
            detail = exc.response.json()
        except Exception:
            pass
        raise HTTPException(
            status_code=502,
            detail={"code": "downstream_error", "detail": detail},
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail={"code": "downstream_unavailable", "detail": str(exc)},
        ) from exc


@app.websocket("/v1/live/session")
async def live_session_ws(websocket: WebSocket) -> None:
    await handle_live_websocket(websocket)


def run() -> None:
    import uvicorn

    uvicorn.run(
        "orchestrator.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


if __name__ == "__main__":
    run()
