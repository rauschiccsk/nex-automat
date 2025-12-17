# artifact-server.py

**Path:** `tools\artifact-server.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Artifact Server - nex-automat projekt
Lokálny FastAPI server pre ukladanie artifacts z claude.ai

---

## Classes

### ArtifactSave(BaseModel)

Model pre ukladanie artifact

**Methods:**

#### `validate_filename(cls, v)`

Validácia názvu súboru

---

### ArtifactInfo(BaseModel)

Info o uloženom artifact

---

## Functions

### `async root()`

Health check

---

### `async save_artifact(data)`

Uloží artifact do projektu

Args:
    data: ArtifactSave s filename a content

Returns:
    ArtifactInfo s informáciami o uloženom súbore

---

### `async list_recent_artifacts(limit)`

Zoznam naposledy upravených súborov

Args:
    limit: Počet súborov (default 10)

Returns:
    Zoznam súborov s informáciami

---

### `async ping()`

Jednoduchý ping pre test dostupnosti

---

### `main()`

Spusti server

---
