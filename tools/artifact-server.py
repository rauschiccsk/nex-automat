"""
Artifact Server - nex-automat projekt
Lokálny FastAPI server pre ukladanie artifacts z claude.ai
"""

import logging
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator

# Konfigurácia
try:
    from config import ARTIFACT_SERVER_HOST, ARTIFACT_SERVER_PORT, PROJECT_ROOT
except ImportError:
    PROJECT_ROOT = Path("C:/Development/nex-automat")
    ARTIFACT_SERVER_PORT = 8765
    ARTIFACT_SERVER_HOST = "localhost"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Claude Artifact Server - nex-automat", version="1.0")

# CORS - povoľ požiadavky z claude.ai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://claude.ai", "https://*.claude.ai", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class ArtifactSave(BaseModel):
    """Model pre ukladanie artifact"""

    filename: str
    content: str

    @validator("filename")
    def validate_filename(cls, v):
        """Validácia názvu súboru"""
        # Bezpečnostná kontrola - žiadne '..' v ceste
        if ".." in v:
            raise ValueError("Filename obsahuje nepovolené znaky '..'")

        # Musí byť relatívna cesta
        if Path(v).is_absolute():
            raise ValueError("Filename musí byť relatívna cesta")

        return v


class ArtifactInfo(BaseModel):
    """Info o uloženom artifact"""

    filename: str
    path: str
    size: int
    timestamp: str


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "service": "Claude Artifact Server",
        "project": "nex-automat",
        "version": "1.0",
        "project_root": str(PROJECT_ROOT),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/save-artifact", response_model=ArtifactInfo)
async def save_artifact(data: ArtifactSave):
    """
    Uloží artifact do projektu

    Args:
        data: ArtifactSave s filename a content

    Returns:
        ArtifactInfo s informáciami o uloženom súbore
    """
    try:
        # Zostavy plnú cestu
        project_root = Path(PROJECT_ROOT)
        file_path = project_root / data.filename

        # Vytvor adresár ak neexistuje
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Ulož súbor
        file_path.write_text(data.content, encoding="utf-8")

        # Info o súbore
        file_size = file_path.stat().st_size

        logger.info(f"✅ Uložené: {data.filename} ({file_size:,} B)")

        return ArtifactInfo(
            filename=data.filename, path=str(file_path), size=file_size, timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"❌ Chyba pri ukladaní {data.filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list-recent")
async def list_recent_artifacts(limit: int = 10):
    """
    Zoznam naposledy upravených súborov

    Args:
        limit: Počet súborov (default 10)

    Returns:
        Zoznam súborov s informáciami
    """
    try:
        project_root = Path(PROJECT_ROOT)

        # Nájdi všetky .py súbory
        py_files = list(project_root.rglob("*.py"))

        # Zoraď podľa času úpravy
        py_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        # Vráť top N
        recent = []
        for f in py_files[:limit]:
            rel_path = f.relative_to(project_root)
            stat = f.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)

            recent.append({"filename": str(rel_path), "size": stat.st_size, "modified": modified.isoformat()})

        return {"count": len(recent), "files": recent}

    except Exception as e:
        logger.error(f"❌ Chyba pri listovaní: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ping")
async def ping():
    """Jednoduchý ping pre test dostupnosti"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


def main():
    """Spusti server"""
    import uvicorn

    print("\n" + "=" * 60)
    print("🚀 ARTIFACT SERVER - nex-automat")
    print("=" * 60)
    print(f"\n📂 Project root: {PROJECT_ROOT}")
    print(f"🌐 URL: http://{ARTIFACT_SERVER_HOST}:{ARTIFACT_SERVER_PORT}")
    print("📡 CORS: https://claude.ai")
    print("\nEndpoints:")
    print("  GET  / - Health check")
    print("  POST /save-artifact - Uložiť artifact")
    print("  GET  /list-recent - Posledné súbory")
    print("  GET  /ping - Ping test")
    print("\nStlač Ctrl+C pre ukončenie")
    print("=" * 60 + "\n")

    uvicorn.run(app, host=ARTIFACT_SERVER_HOST, port=ARTIFACT_SERVER_PORT, log_level="info")


if __name__ == "__main__":
    main()
