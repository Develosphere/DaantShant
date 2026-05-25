# DantShaant

Autonomous AI dental assistant — conversational agent with vision-based teeth analysis, Hybrid RAG recommendations, and MCP-driven follow-ups (Urdu/English).

**Foundation status:** FastAPI orchestrator + separate **Teeth Analyzer** and **Diagnosis** services, connected via OpenAPI specs.

## Architecture (foundation)

```
specs/                    # OpenAPI contracts (source of truth)
packages/dantshaant_common/   # Shared Pydantic types + HTTP clients
services/teeth_analyzer/      # Vision inference :8001
services/diagnosis/           # Clinical classification :8002
orchestrator/                 # API gateway :8000
docs/planning/MODELS.md       # Model roadmap (LoRA/QLoRA, datasets)
```

Aligns with technical doc **5-layer design**: this repo covers **L3 (inference)** split and the **FastAPI backend** slice of Phase 1 MVP.

## Quick start

```powershell
cd "e:\Nathan\SSUET University\Semester 4\DB\Lab\Project\DantShaant"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# If OpenCV download is slow/fails, retry: .\scripts\install-deps.ps1
copy .env.example .env
# Optional: TEETH_ANALYZER_BACKEND=gemini and TEETH_ANALYZER_GEMINI_API_KEY=your_key
.\scripts\start-services.ps1
```

**Web app (camera + live video):**

```powershell
cd apps\web
npm install
npm run dev
```

Open http://localhost:3000 — **Take picture** (HTTP) or **Live video** (WebSocket).

- Orchestrator docs: http://127.0.0.1:8000/docs  
- Teeth Analyzer: http://127.0.0.1:8001/docs  
- Diagnosis: http://127.0.0.1:8002/docs  
- Session logs: `orchestrator/data/sessions/sessions.jsonl` (when run from orchestrator cwd)  

### Pipeline endpoint (MCP `analyze_teeth_image` precursor)

`POST /v1/teeth/analyze` on the orchestrator runs:

1. Teeth Analyzer → visual findings  
2. Diagnosis → condition, severity, `action_trigger`, disclaimer  

## Environment

See `.env.example` for service URLs and ports.

## Spec-driven development

1. Change `specs/*.openapi.yaml`  
2. Mirror types in `packages/dantshaant_common/src/dantshaant_common/schemas.py`  
3. Update service implementations  

Do not couple vision weights into the diagnosis service — only HTTP + shared schemas.

## Roadmap pointer

| MVP phase (doc) | This repo |
|-----------------|-----------|
| Phase 1 — FastAPI + stub vision | ✅ foundation |
| Phase 2 — LoRA/QLoRA on LLaVA | `teeth_analyzer/inference.py` + `docs/planning/MODELS.md` |
| Phase 3 — Hybrid RAG | future `services/rag/` + orchestrator routes |
| Phase 4 — MCP tools | FastMCP server calling orchestrator |

## License

Confidential — DantShaant 2026 (per technical documentation).
