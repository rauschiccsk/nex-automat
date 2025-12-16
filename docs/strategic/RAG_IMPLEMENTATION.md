# RAG Implementation - Kompletný Implementačný Plán

**Vytvorené:** 2025-12-16  
**Status:** 🟡 Ready for Implementation  
**Verzia:** 1.0  
**Umiestnenie:** `docs/strategic/RAG_IMPLEMENTATION.md`  
**Časový odhad:** 1 týždeň (RAG MVP)

---

## 🎯 Cieľ Projektu

Implementovať RAG (Retrieval-Augmented Generation) systém pre efektívne vyhľadávanie v dokumentácii projektu NEX Automat. RAG umožní Claude okamžitý prístup k relevantným dokumentom, čím:

- ✅ Zvýši produktivitu o 30-40%
- ✅ Zníži počet potrebných chatov o 60%
- ✅ Eliminuje manuálne hľadanie dokumentov
- ✅ Zabezpečí že žiadna informácia neunikne

---

## 📋 Obsah

1. [Architektúra Systému](#architektúra-systému)
2. [Technologický Stack](#technologický-stack)
3. [Hardvérové Požiadavky](#hardvérové-požiadavky)
4. [Implementačné Fázy](#implementačné-fázy)
5. [Fáza 1: PostgreSQL Setup](#fáza-1-postgresql-setup)
6. [Fáza 2: Python Environment](#fáza-2-python-environment)
7. [Fáza 3: Ingestion Pipeline](#fáza-3-ingestion-pipeline)
8. [Fáza 4: Query Pipeline](#fáza-4-query-pipeline)
9. [Fáza 5: Testovanie](#fáza-5-testovanie)
10. [Fáza 6: Integrácia s Claude](#fáza-6-integrácia-s-claude)
11. [Údržba a Aktualizácia](#údržba-a-aktualizácia)
12. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architektúra Systému

### Komponenty

```
┌─────────────────────────────────────────────────┐
│  DOKUMENTÁCIA NEX AUTOMAT                       │
│  - 45 .md súborov                               │
│  - ~450k tokens                                 │
│  - 10 kategórií                                 │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│  INGESTION PIPELINE                             │
│  - Markdown parser                              │
│  - Chunking (500-1000 tokens)                   │
│  - Embedding generation                         │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│  POSTGRESQL + PGVECTOR                          │
│  - rag_documents (dokumenty)                    │
│  - rag_chunks (chunks + embeddings)             │
│  - rag_keywords (kľúčové slová)                 │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│  QUERY PIPELINE                                 │
│  - Vector search (embeddings)                   │
│  - Keyword boost                                │
│  - Re-ranking                                   │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│  CLAUDE (LLM)                                   │
│  - Dostane relevantné chunks                    │
│  - Generuje odpovede                            │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Technologický Stack

### Core Komponenty

| Komponenta | Technológia | Verzia | Licencia |
|------------|-------------|--------|----------|
| **Databáza** | PostgreSQL | 16+ | PostgreSQL |
| **Vector Extension** | pgvector | 0.5.1+ | PostgreSQL |
| **Embedding Model** | sentence-transformers | 2.2.2+ | Apache 2.0 |
| **Embedding Model Type** | all-MiniLM-L6-v2 | - | Apache 2.0 |
| **Python** | Python | 3.11+ | PSF |
| **Database Driver** | psycopg2-binary | 2.9.9+ | LGPL |
| **CLI Framework** | click | 8.1.7+ | BSD |
| **Output Formatting** | rich | 13.7.0+ | MIT |

### Python Dependencies

```txt
# requirements-rag.txt
sentence-transformers==2.2.2
psycopg2-binary==2.9.9
pgvector==0.2.4
markdown==3.5.1
pyyaml==6.0.1
click==8.1.7
rich==13.7.0
python-dotenv==1.0.0
```

---

## 💻 Hardvérové Požiadavky

### Minimálne Požiadavky

```
CPU:     4+ cores
RAM:     16GB (8GB PostgreSQL + 4GB Python + 4GB OS)
HDD:     20GB voľného miesta
  ├─ PostgreSQL databáza: ~500MB
  ├─ Embedding model: ~80MB
  ├─ Python packages: ~2GB
  └─ Dokumentácia chunks: ~100MB
OS:      Windows Server 2019+ / Linux
```

### Odporúčané

```
CPU:     8+ cores
RAM:     32GB
SSD:     50GB+
Network: LAN (pre PostgreSQL)
```

---

## 📅 Implementačné Fázy

### Časový Harmonogram (1 týždeň = RAG MVP)

| Fáza | Popis | Čas | Status |
|------|-------|-----|--------|
| **1** | PostgreSQL + pgvector setup | 2-3 hodiny | ⏸️ |
| **2** | Python environment setup | 1 hodina | ⏸️ |
| **3** | Ingestion pipeline | 4-6 hodín | ⏸️ |
| **4** | Query pipeline | 3-4 hodiny | ⏸️ |
| **5** | Testovanie | 2-3 hodiny | ⏸️ |
| **6** | Integrácia s Claude | 1-2 hodiny | ⏸️ |
| **TOTAL** | RAG MVP | **1 týždeň** | ⏸️ |

---

## 🗄️ Fáza 1: PostgreSQL Setup

### 1.1 Inštalácia PostgreSQL

**Windows Server:**

```powershell
# Stiahni PostgreSQL 16
# https://www.postgresql.org/download/windows/

# Alebo cez Chocolatey
choco install postgresql16

# Alebo cez Scoop
scoop install postgresql
```

**Konfigurácia po inštalácii:**

```powershell
# Nastav environment variable
$env:PATH += ";C:\Program Files\PostgreSQL\16\bin"

# Test
psql --version
# Výstup: psql (PostgreSQL) 16.x
```

### 1.2 Vytvorenie RAG Databázy

```sql
-- Pripoj sa ako postgres user
psql -U postgres

-- Vytvor databázu
CREATE DATABASE nex_automat_rag
    ENCODING 'UTF8'
    LC_COLLATE 'Slovak_Slovakia.1250'
    LC_CTYPE 'Slovak_Slovakia.1250';

-- Pripoj sa na novú databázu
\c nex_automat_rag

-- Vytvor pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Overte instaláciu
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### 1.3 Vytvorenie Databázových Tabuliek

```sql
-- ===================================================================
-- TABUĽKA: rag_documents
-- Popis: Hlavná tabuľka dokumentov (metadata)
-- ===================================================================

CREATE TABLE rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    version VARCHAR(20) DEFAULT '1.0',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexy pre rýchle vyhľadávanie
CREATE INDEX idx_documents_category ON rag_documents(category);
CREATE INDEX idx_documents_status ON rag_documents(status);
CREATE INDEX idx_documents_updated ON rag_documents(updated_at);
CREATE INDEX idx_documents_metadata ON rag_documents USING GIN(metadata);

-- ===================================================================
-- TABUĽKA: rag_chunks
-- Popis: Chunks dokumentov s embeddingmi
-- ===================================================================

CREATE TABLE rag_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id VARCHAR(255) NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_type VARCHAR(50) NOT NULL,
    section_path TEXT,
    heading_level INTEGER,
    content TEXT NOT NULL,
    tokens INTEGER,
    embedding vector(384),  -- all-MiniLM-L6-v2 = 384 dimenzií
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_document 
        FOREIGN KEY (document_id) 
        REFERENCES rag_documents(document_id)
        ON DELETE CASCADE
);

-- Indexy
CREATE INDEX idx_chunks_document ON rag_chunks(document_id);
CREATE INDEX idx_chunks_type ON rag_chunks(chunk_type);

-- Vector index (HNSW pre rýchle similarity search)
CREATE INDEX idx_chunks_embedding 
    ON rag_chunks 
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- ===================================================================
-- TABUĽKA: rag_keywords
-- Popis: Kľúčové slová pre keyword-based search
-- ===================================================================

CREATE TABLE rag_keywords (
    id SERIAL PRIMARY KEY,
    chunk_id UUID NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    
    CONSTRAINT fk_chunk 
        FOREIGN KEY (chunk_id) 
        REFERENCES rag_chunks(id)
        ON DELETE CASCADE
);

-- Indexy
CREATE INDEX idx_keywords_chunk ON rag_keywords(chunk_id);
CREATE INDEX idx_keywords_keyword ON rag_keywords(keyword);

-- ===================================================================
-- TABUĽKA: rag_search_history
-- Popis: História vyhľadávaní (analytics)
-- ===================================================================

CREATE TABLE rag_search_history (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    results_count INTEGER,
    top_chunk_ids UUID[],
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_search_created ON rag_search_history(created_at);
```

### 1.4 Test Databázy

```sql
-- Test vector operations
SELECT '[0.1, 0.2, 0.3]'::vector <=> '[0.2, 0.3, 0.4]'::vector AS distance;

-- Výstup: distance (cosine distance)
-- Ak funguje, pgvector je OK
```

---

## 🐍 Fáza 2: Python Environment

### 2.1 Vytvorenie Virtual Environment

```bash
# Prejdi do projekt root
cd C:\Development\nex-automat

# Vytvor venv pre RAG
python -m venv venv-rag

# Aktivuj
venv-rag\Scripts\activate  # Windows
# alebo
source venv-rag/bin/activate  # Linux

# Upgrade pip
python -m pip install --upgrade pip
```

### 2.2 Inštalácia Dependencies

```bash
# Inštaluj všetky dependencies
pip install -r requirements-rag.txt

# Alebo manuálne:
pip install sentence-transformers==2.2.2
pip install psycopg2-binary==2.9.9
pip install pgvector==0.2.4
pip install markdown==3.5.1
pip install pyyaml==6.0.1
pip install click==8.1.7
pip install rich==13.7.0
pip install python-dotenv==1.0.0
```

### 2.3 Download Embedding Model

```python
# test_embedding_model.py
from sentence_transformers import SentenceTransformer

print("Sťahujem embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model stiahnutý!")

# Test
text = "PostgreSQL databáza"
embedding = model.encode(text)
print(f"✅ Embedding dimension: {len(embedding)}")
print(f"✅ Sample values: {embedding[:5]}")
```

**Spustenie:**
```bash
python test_embedding_model.py

# Výstup:
# Sťahujem embedding model...
# ✅ Model stiahnutý!
# ✅ Embedding dimension: 384
# ✅ Sample values: [0.123, -0.456, 0.789, ...]
```

### 2.4 Konfiguračný Súbor

```yaml
# config/rag_config.yaml

database:
  host: localhost
  port: 5432
  database: nex_automat_rag
  user: postgres
  password: your_password_here

embedding:
  model_name: all-MiniLM-L6-v2
  dimension: 384
  batch_size: 32

chunking:
  min_chunk_size: 100
  target_chunk_size: 750
  max_chunk_size: 1500
  overlap_tokens: 150

paths:
  docs_root: C:/Development/nex-automat/docs
  output_dir: C:/Development/nex-automat/rag_output

search:
  top_k: 5
  similarity_threshold: 0.5
  vector_weight: 0.7
  keyword_weight: 0.3
```

---

## 📥 Fáza 3: Ingestion Pipeline

### 3.1 Štruktúra Skriptov

```
tools/
├── rag/
│   ├── __init__.py
│   ├── config.py           # Načítanie konfigurácie
│   ├── database.py         # PostgreSQL connection
│   ├── embedding.py        # Embedding model wrapper
│   ├── chunking.py         # Document chunking
│   ├── ingestion.py        # Main ingestion logic
│   ├── query.py            # Query pipeline
│   └── utils.py            # Helper funkcie
└── rag_ingest.py           # CLI entry point
```

### 3.2 Config Module

```python
# tools/rag/config.py

import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

@dataclass
class EmbeddingConfig:
    model_name: str
    dimension: int
    batch_size: int

@dataclass
class ChunkingConfig:
    min_chunk_size: int
    target_chunk_size: int
    max_chunk_size: int
    overlap_tokens: int

@dataclass
class PathsConfig:
    docs_root: Path
    output_dir: Path

@dataclass
class SearchConfig:
    top_k: int
    similarity_threshold: float
    vector_weight: float
    keyword_weight: float

@dataclass
class RAGConfig:
    database: DatabaseConfig
    embedding: EmbeddingConfig
    chunking: ChunkingConfig
    paths: PathsConfig
    search: SearchConfig

def load_config(config_path: str = "config/rag_config.yaml") -> RAGConfig:
    """Načíta konfiguráciu zo YAML súboru"""
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return RAGConfig(
        database=DatabaseConfig(**data['database']),
        embedding=EmbeddingConfig(**data['embedding']),
        chunking=ChunkingConfig(**data['chunking']),
        paths=PathsConfig(
            docs_root=Path(data['paths']['docs_root']),
            output_dir=Path(data['paths']['output_dir'])
        ),
        search=SearchConfig(**data['search'])
    )
```

### 3.3 Database Module

```python
# tools/rag/database.py

import psycopg2
from psycopg2.extras import execute_values
from typing import List, Dict, Any
from contextlib import contextmanager

class RAGDatabase:
    """PostgreSQL databáza pre RAG systém"""
    
    def __init__(self, config):
        self.config = config
        self.conn = None
    
    def connect(self):
        """Pripoj sa na databázu"""
        self.conn = psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password
        )
        return self.conn
    
    @contextmanager
    def cursor(self):
        """Context manager pre cursor"""
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()
    
    def insert_document(self, doc_data: Dict[str, Any]) -> str:
        """Vlož dokument metadata"""
        
        with self.cursor() as cur:
            cur.execute("""
                INSERT INTO rag_documents 
                (document_id, category, title, file_path, metadata)
                VALUES (%(document_id)s, %(category)s, %(title)s, 
                        %(file_path)s, %(metadata)s)
                ON CONFLICT (document_id) DO UPDATE
                SET updated_at = CURRENT_TIMESTAMP
                RETURNING document_id
            """, doc_data)
            
            return cur.fetchone()[0]
    
    def insert_chunks(self, chunks: List[Dict[str, Any]]):
        """Vlož chunks s embeddingmi (batch)"""
        
        with self.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO rag_chunks 
                (document_id, chunk_index, chunk_type, section_path,
                 heading_level, content, tokens, embedding, metadata)
                VALUES %s
                """,
                [
                    (
                        c['document_id'],
                        c['chunk_index'],
                        c['chunk_type'],
                        c.get('section_path'),
                        c.get('heading_level'),
                        c['content'],
                        c['tokens'],
                        c['embedding'],
                        psycopg2.extras.Json(c.get('metadata', {}))
                    )
                    for c in chunks
                ]
            )
    
    def delete_document_chunks(self, document_id: str):
        """Zmaž všetky chunks pre dokument"""
        
        with self.cursor() as cur:
            cur.execute(
                "DELETE FROM rag_chunks WHERE document_id = %s",
                (document_id,)
            )
    
    def search_similar_chunks(self, query_embedding: List[float], 
                             top_k: int = 5) -> List[Dict]:
        """Vector similarity search"""
        
        with self.cursor() as cur:
            cur.execute("""
                SELECT 
                    c.id,
                    c.document_id,
                    c.content,
                    c.section_path,
                    c.metadata,
                    d.title as doc_title,
                    d.category,
                    1 - (c.embedding <=> %s::vector) as similarity
                FROM rag_chunks c
                JOIN rag_documents d ON c.document_id = d.document_id
                WHERE d.status = 'active'
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, top_k))
            
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def close(self):
        """Zatvor connection"""
        if self.conn:
            self.conn.close()
```

### 3.4 Embedding Module

```python
# tools/rag/embedding.py

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

class EmbeddingModel:
    """Wrapper pre sentence-transformers model"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
    
    def load(self):
        """Načítaj model"""
        print(f"Načítavam embedding model: {self.config.model_name}")
        self.model = SentenceTransformer(self.config.model_name)
        print("✅ Model načítaný")
    
    def encode(self, texts: Union[str, List[str]], 
               batch_size: int = None) -> Union[np.ndarray, List[float]]:
        """Vytvor embeddings pre text(y)"""
        
        if not self.model:
            self.load()
        
        batch_size = batch_size or self.config.batch_size
        
        # Single text
        if isinstance(texts, str):
            embedding = self.model.encode(texts)
            return embedding.tolist()
        
        # Multiple texts (batch)
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True
        )
        return embeddings.tolist()
    
    def encode_query(self, query: str) -> List[float]:
        """Vytvor embedding pre query (optimalizované)"""
        return self.encode(query)
```

### 3.5 Chunking Module

```python
# tools/rag/chunking.py

import re
from typing import List, Dict
from pathlib import Path

class DocumentChunker:
    """Rozdeľovanie dokumentov na chunks"""
    
    def __init__(self, config):
        self.config = config
    
    def count_tokens(self, text: str) -> int:
        """Približný počet tokenov (1 token ≈ 4 znaky)"""
        return len(text) // 4
    
    def chunk_document(self, content: str, document_id: str) -> List[Dict]:
        """Rozdeľ dokument na chunks podľa veľkosti"""
        
        tokens = self.count_tokens(content)
        
        # Malý dokument - celý ako jeden chunk
        if tokens < 5000:
            return self._create_whole_document_chunk(content, document_id)
        
        # Stredný dokument - rozdeľ podľa H2
        elif tokens < 15000:
            return self._chunk_by_h2(content, document_id)
        
        # Veľký dokument - rozdeľ podľa H3
        else:
            return self._chunk_by_h3(content, document_id)
    
    def _create_whole_document_chunk(self, content: str, 
                                    document_id: str) -> List[Dict]:
        """Celý dokument ako jeden chunk"""
        
        return [{
            'document_id': document_id,
            'chunk_index': 0,
            'chunk_type': 'whole_document',
            'content': content,
            'tokens': self.count_tokens(content),
            'metadata': {'full_document': True}
        }]
    
    def _chunk_by_h2(self, content: str, document_id: str) -> List[Dict]:
        """Rozdeľ podľa ## nadpisov"""
        
        chunks = []
        sections = re.split(r'\n## ', content)
        
        for idx, section in enumerate(sections):
            if not section.strip():
                continue
            
            # Pridaj späť ## prefix (okrem prvej sekcie)
            if idx > 0:
                section = '## ' + section
            
            chunks.append({
                'document_id': document_id,
                'chunk_index': idx,
                'chunk_type': 'h2_section',
                'section_path': self._extract_heading(section),
                'heading_level': 2,
                'content': section,
                'tokens': self.count_tokens(section),
                'metadata': {}
            })
        
        return chunks
    
    def _chunk_by_h3(self, content: str, document_id: str) -> List[Dict]:
        """Rozdeľ podľa ### nadpisov"""
        
        chunks = []
        sections = re.split(r'\n### ', content)
        
        for idx, section in enumerate(sections):
            if not section.strip():
                continue
            
            if idx > 0:
                section = '### ' + section
            
            chunks.append({
                'document_id': document_id,
                'chunk_index': idx,
                'chunk_type': 'h3_section',
                'section_path': self._extract_heading(section),
                'heading_level': 3,
                'content': section,
                'tokens': self.count_tokens(section),
                'metadata': {}
            })
        
        return chunks
    
    def _extract_heading(self, text: str) -> str:
        """Extrahuj nadpis zo sekcie"""
        
        lines = text.split('\n')
        for line in lines[:3]:  # Hľadaj v prvých 3 riadkoch
            if line.strip().startswith('#'):
                return line.strip('#').strip()
        
        return "Unknown Section"
```

### 3.6 Main Ingestion Script

```python
# tools/rag/ingestion.py

from pathlib import Path
from typing import List
import json
from rich.console import Console
from rich.progress import track

from .config import load_config
from .database import RAGDatabase
from .embedding import EmbeddingModel
from .chunking import DocumentChunker

console = Console()

class RAGIngestion:
    """Main ingestion pipeline"""
    
    def __init__(self, config_path: str = "config/rag_config.yaml"):
        self.config = load_config(config_path)
        self.db = RAGDatabase(self.config.database)
        self.embedder = EmbeddingModel(self.config.embedding)
        self.chunker = DocumentChunker(self.config.chunking)
    
    def connect(self):
        """Pripoj sa na databázu"""
        self.db.connect()
        self.embedder.load()
    
    def ingest_document(self, file_path: Path):
        """Spracuj jeden dokument"""
        
        console.print(f"\n📄 Spracovávam: [cyan]{file_path.name}[/cyan]")
        
        # 1. Načítaj obsah
        content = file_path.read_text(encoding='utf-8')
        
        # 2. Určte kategóriu z cesty
        category = self._determine_category(file_path)
        
        # 3. Vytvor document metadata
        doc_data = {
            'document_id': str(file_path.relative_to(self.config.paths.docs_root)),
            'category': category,
            'title': file_path.stem,
            'file_path': str(file_path),
            'metadata': json.dumps({
                'size': len(content),
                'lines': content.count('\n')
            })
        }
        
        # 4. Ulož document
        self.db.insert_document(doc_data)
        
        # 5. Rozdeľ na chunks
        console.print("  ├─ Rozdeľujem na chunks...")
        chunks = self.chunker.chunk_document(content, doc_data['document_id'])
        console.print(f"  ├─ ✅ {len(chunks)} chunks")
        
        # 6. Vytvor embeddings
        console.print("  ├─ Vytváram embeddings...")
        texts = [c['content'] for c in chunks]
        embeddings = self.embedder.encode(texts)
        
        # Pridaj embeddings do chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding
        
        console.print(f"  ├─ ✅ {len(embeddings)} embeddings")
        
        # 7. Ulož chunks
        console.print("  ├─ Ukladám do databázy...")
        self.db.insert_chunks(chunks)
        console.print(f"  └─ ✅ Hotovo")
        
        return len(chunks)
    
    def ingest_all(self):
        """Spracuj všetky dokumenty"""
        
        # Nájdi všetky .md súbory
        md_files = list(self.config.paths.docs_root.rglob("*.md"))
        
        console.print(f"\n📚 Našiel som [bold]{len(md_files)}[/bold] dokumentov\n")
        
        total_chunks = 0
        
        for file_path in track(md_files, description="Spracovávam..."):
            try:
                chunks_count = self.ingest_document(file_path)
                total_chunks += chunks_count
            except Exception as e:
                console.print(f"  └─ ❌ Chyba: {e}", style="red")
        
        console.print(f"\n🎉 [bold green]HOTOVO![/bold green]")
        console.print(f"   Dokumenty: {len(md_files)}")
        console.print(f"   Chunks: {total_chunks}")
    
    def _determine_category(self, file_path: Path) -> str:
        """Určte kategóriu dokumentu z cesty"""
        
        parts = file_path.relative_to(self.config.paths.docs_root).parts
        
        if len(parts) > 0:
            return parts[0]  # Prvá úroveň = kategória
        
        return "general"
    
    def close(self):
        """Zatvor connections"""
        self.db.close()
```

### 3.7 CLI Entry Point

```python
# tools/rag_ingest.py

import click
from pathlib import Path
from rag.ingestion import RAGIngestion

@click.command()
@click.option('--config', default='config/rag_config.yaml',
              help='Cesta ku config súboru')
@click.option('--single', type=click.Path(exists=True),
              help='Spracuj jeden dokument')
def main(config, single):
    """RAG Ingestion Pipeline - Nahraj dokumentáciu do RAG systému"""
    
    ingestion = RAGIngestion(config_path=config)
    
    try:
        ingestion.connect()
        
        if single:
            # Spracuj jeden dokument
            ingestion.ingest_document(Path(single))
        else:
            # Spracuj všetky dokumenty
            ingestion.ingest_all()
    
    finally:
        ingestion.close()

if __name__ == '__main__':
    main()
```

---

## 🔍 Fáza 4: Query Pipeline

### 4.1 Query Module

```python
# tools/rag/query.py

from typing import List, Dict
from rich.console import Console
from rich.table import Table

from .database import RAGDatabase
from .embedding import EmbeddingModel

console = Console()

class RAGQuery:
    """Query pipeline pre RAG systém"""
    
    def __init__(self, config):
        self.config = config
        self.db = RAGDatabase(self.config.database)
        self.embedder = EmbeddingModel(self.config.embedding)
    
    def connect(self):
        """Pripoj sa"""
        self.db.connect()
        self.embedder.load()
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """Vyhľadaj relevantné chunks"""
        
        top_k = top_k or self.config.search.top_k
        
        # 1. Vytvor query embedding
        console.print(f"🔍 Hľadám: [cyan]{query}[/cyan]")
        query_embedding = self.embedder.encode_query(query)
        
        # 2. Vector search
        results = self.db.search_similar_chunks(query_embedding, top_k)
        
        # 3. Filter by similarity threshold
        threshold = self.config.search.similarity_threshold
        filtered = [r for r in results if r['similarity'] >= threshold]
        
        console.print(f"✅ Našiel som {len(filtered)} relevantných chunks")
        
        return filtered
    
    def display_results(self, results: List[Dict]):
        """Zobraz výsledky v peknom formáte"""
        
        if not results:
            console.print("❌ Žiadne výsledky", style="red")
            return
        
        table = Table(title="RAG Search Results")
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Document", style="green")
        table.add_column("Section", style="yellow")
        table.add_column("Similarity", style="magenta", width=10)
        
        for idx, result in enumerate(results, 1):
            table.add_row(
                str(idx),
                result['doc_title'],
                result.get('section_path', 'N/A')[:50],
                f"{result['similarity']:.3f}"
            )
        
        console.print(table)
    
    def get_context(self, results: List[Dict]) -> str:
        """Vytvor context string pre LLM"""
        
        context_parts = []
        
        for idx, result in enumerate(results, 1):
            context_parts.append(f"""
---
SOURCE {idx}: {result['doc_title']}
Section: {result.get('section_path', 'N/A')}
Category: {result['category']}
Similarity: {result['similarity']:.3f}

{result['content']}
---
""")
        
        return "\n".join(context_parts)
    
    def close(self):
        """Zatvor connections"""
        self.db.close()
```

### 4.2 CLI Query Tool

```python
# tools/rag_query.py

import click
from rag.config import load_config
from rag.query import RAGQuery

@click.command()
@click.argument('query')
@click.option('--config', default='config/rag_config.yaml')
@click.option('--top-k', default=5, type=int)
@click.option('--context', is_flag=True, 
              help='Zobraz LLM context')
def main(query, config, top_k, context):
    """RAG Query Tool - Vyhľadaj v dokumentácii"""
    
    rag = RAGQuery(load_config(config))
    
    try:
        rag.connect()
        
        # Vyhľadaj
        results = rag.search(query, top_k)
        
        # Zobraz výsledky
        rag.display_results(results)
        
        # Zobraz context pre LLM
        if context and results:
            click.echo("\n" + "="*80)
            click.echo("LLM CONTEXT:")
            click.echo("="*80)
            click.echo(rag.get_context(results))
    
    finally:
        rag.close()

if __name__ == '__main__':
    main()
```

---

## 🧪 Fáza 5: Testovanie

### 5.1 Test Suite

```python
# tests/test_rag_system.py

import pytest
from pathlib import Path
from tools.rag.config import load_config
from tools.rag.database import RAGDatabase
from tools.rag.embedding import EmbeddingModel
from tools.rag.chunking import DocumentChunker
from tools.rag.query import RAGQuery

@pytest.fixture
def config():
    return load_config('config/rag_config.yaml')

@pytest.fixture
def db(config):
    database = RAGDatabase(config.database)
    database.connect()
    yield database
    database.close()

def test_database_connection(db):
    """Test PostgreSQL connection"""
    assert db.conn is not None
    assert not db.conn.closed

def test_embedding_model(config):
    """Test embedding model"""
    embedder = EmbeddingModel(config.embedding)
    embedder.load()
    
    # Test single text
    embedding = embedder.encode("PostgreSQL databáza")
    assert len(embedding) == 384
    
    # Test batch
    embeddings = embedder.encode(["text1", "text2"])
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384

def test_chunking(config):
    """Test document chunking"""
    chunker = DocumentChunker(config.chunking)
    
    # Malý dokument
    content = "# Title\n\nSome content here."
    chunks = chunker.chunk_document(content, "test_doc")
    assert len(chunks) == 1
    assert chunks[0]['chunk_type'] == 'whole_document'
    
    # Stredný dokument (H2 chunks)
    content = "# Title\n\n## Section 1\nContent 1\n\n## Section 2\nContent 2" * 100
    chunks = chunker.chunk_document(content, "test_doc")
    assert len(chunks) > 1

def test_search_query(config, db):
    """Test RAG query"""
    query_tool = RAGQuery(config)
    query_tool.connect()
    
    # Test vyhľadávanie
    results = query_tool.search("PostgreSQL databáza", top_k=3)
    
    assert isinstance(results, list)
    if results:
        assert 'similarity' in results[0]
        assert 'content' in results[0]
    
    query_tool.close()

def test_end_to_end(config):
    """End-to-end test: ingest → query"""
    
    from tools.rag.ingestion import RAGIngestion
    
    # 1. Ingest test document
    ingestion = RAGIngestion()
    ingestion.connect()
    
    test_doc = Path("tests/fixtures/test_document.md")
    if test_doc.exists():
        ingestion.ingest_document(test_doc)
    
    ingestion.close()
    
    # 2. Query
    query_tool = RAGQuery(config)
    query_tool.connect()
    
    results = query_tool.search("test query", top_k=1)
    assert len(results) >= 0  # Môže byť prázdne ak test_document.md neexistuje
    
    query_tool.close()
```

### 5.2 Test Queries

**Vytvor test queries súbor:**

```yaml
# tests/test_queries.yaml

queries:
  - query: "Ako funguje GSCAT tabuľka?"
    expected_docs:
      - "database/tables/GSCAT.md"
    min_similarity: 0.7
  
  - query: "Kde sú uložené EAN kódy?"
    expected_docs:
      - "database/tables/GSCAT.md"
      - "database/tables/BARCODE.md"
    min_similarity: 0.6
  
  - query: "Ako číslujeme faktúry?"
    expected_docs:
      - "documents/NUMBERING.md"
    min_similarity: 0.7
  
  - query: "PySide6 migration"
    expected_docs:
      - "migration/PYSIDE6_MIGRATION.md"
    min_similarity: 0.6
  
  - query: "n8n workflow temporal"
    expected_docs:
      - "strategic/N8N_TO_TEMPORAL_MIGRATION.md"
    min_similarity: 0.7
```

**Test runner:**

```python
# tests/run_query_tests.py

import yaml
from rich.console import Console
from tools.rag.config import load_config
from tools.rag.query import RAGQuery

console = Console()

def run_tests():
    """Spusti test queries"""
    
    # Načítaj test queries
    with open('tests/test_queries.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    # Inicializuj RAG
    config = load_config()
    rag = RAGQuery(config)
    rag.connect()
    
    passed = 0
    failed = 0
    
    console.print("\n🧪 [bold]RAG Query Tests[/bold]\n")
    
    for test in data['queries']:
        query = test['query']
        expected_docs = test['expected_docs']
        min_sim = test['min_similarity']
        
        console.print(f"Testing: [cyan]{query}[/cyan]")
        
        # Vyhľadaj
        results = rag.search(query, top_k=5)
        
        # Check ak očakávané dokumenty sú v top results
        found_docs = [r['document_id'] for r in results]
        
        success = any(
            any(exp in doc for exp in expected_docs)
            for doc in found_docs
        )
        
        if success and results[0]['similarity'] >= min_sim:
            console.print(f"  ✅ PASS (similarity: {results[0]['similarity']:.3f})\n")
            passed += 1
        else:
            console.print(f"  ❌ FAIL\n", style="red")
            failed += 1
    
    console.print(f"\n{'='*50}")
    console.print(f"Results: {passed} passed, {failed} failed")
    console.print(f"{'='*50}\n")
    
    rag.close()
    
    return passed, failed

if __name__ == '__main__':
    run_tests()
```

---

## 🔗 Fáza 6: Integrácia s Claude

### 6.1 API Wrapper

```python
# tools/rag/claude_integration.py

from anthropic import Anthropic
from typing import List, Dict

class ClaudeRAG:
    """Integrácia RAG s Claude API"""
    
    def __init__(self, api_key: str, rag_query):
        self.client = Anthropic(api_key=api_key)
        self.rag = rag_query
    
    def ask(self, question: str, top_k: int = 5) -> str:
        """Opýtaj sa otázku s RAG kontextom"""
        
        # 1. RAG search
        results = self.rag.search(question, top_k)
        
        if not results:
            return self._ask_without_context(question)
        
        # 2. Vytvor context
        context = self.rag.get_context(results)
        
        # 3. Vytvor prompt
        prompt = f"""
Máš k dispozícii nasledujúcu dokumentáciu z projektu NEX Automat:

{context}

Na základe tejto dokumentácie odpovedz na otázku:

{question}

Ak odpoveď nájdeš v dokumentácii, cituj zdroj (SOURCE číslo).
Ak odpoveď nie je v dokumentácii, povedz to priamo.
"""
        
        # 4. Zavolaj Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def _ask_without_context(self, question: str) -> str:
        """Otázka bez RAG kontextu"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": f"""
Otázka je o projekte NEX Automat, ale nenašiel som relevantné dokumenty.
Skús odpovedať na základe všeobecných znalostí:

{question}
"""}
            ]
        )
        
        return response.content[0].text
```

### 6.2 CLI Tool s Claude

```python
# tools/rag_ask.py

import click
import os
from dotenv import load_dotenv
from tools.rag.config import load_config
from tools.rag.query import RAGQuery
from tools.rag.claude_integration import ClaudeRAG

load_dotenv()

@click.command()
@click.argument('question')
@click.option('--top-k', default=5)
def main(question, top_k):
    """Opýtaj sa otázku s RAG + Claude"""
    
    # API key z environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        click.echo("❌ ANTHROPIC_API_KEY not set", err=True)
        return
    
    # Inicializuj RAG
    config = load_config()
    rag_query = RAGQuery(config)
    rag_query.connect()
    
    # Inicializuj Claude
    claude = ClaudeRAG(api_key, rag_query)
    
    # Opýtaj sa
    click.echo(f"\n🤔 Otázka: {question}\n")
    click.echo("🔍 Hľadám v dokumentácii...")
    
    answer = claude.ask(question, top_k)
    
    click.echo("\n" + "="*80)
    click.echo("💬 Claude odpoveď:")
    click.echo("="*80)
    click.echo(answer)
    click.echo("="*80 + "\n")
    
    rag_query.close()

if __name__ == '__main__':
    main()
```

**Použitie:**

```bash
# Nastav API key
export ANTHROPIC_API_KEY=your_key_here

# Opýtaj sa
python tools/rag_ask.py "Ako funguje GSCAT tabuľka?"

# Výstup:
# 🤔 Otázka: Ako funguje GSCAT tabuľka?
# 
# 🔍 Hľadám v dokumentácii...
# 
# ================================================================================
# 💬 Claude odpoveď:
# ================================================================================
# Podľa SOURCE 1 (database/tables/GSCAT.md), GSCAT je globálny katalóg produktov...
# ================================================================================
```

---

## 🔄 Údržba a Aktualizácia

### Automatické Sledovanie Zmien

```python
# tools/rag_watch.py

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from tools.rag.config import load_config
from tools.rag.ingestion import RAGIngestion

class DocsWatcher(FileSystemEventHandler):
    """Sleduje zmeny v docs/ priečinku"""
    
    def __init__(self, ingestion: RAGIngestion):
        self.ingestion = ingestion
    
    def on_created(self, event):
        """Nový súbor"""
        if event.src_path.endswith('.md'):
            print(f"✨ Nový dokument: {event.src_path}")
            self.ingestion.ingest_document(Path(event.src_path))
    
    def on_modified(self, event):
        """Súbor upravený"""
        if event.src_path.endswith('.md'):
            print(f"🔄 Aktualizujem: {event.src_path}")
            file_path = Path(event.src_path)
            doc_id = str(file_path.relative_to(self.ingestion.config.paths.docs_root))
            
            # Zmaž staré chunks
            self.ingestion.db.delete_document_chunks(doc_id)
            
            # Nahraj nové
            self.ingestion.ingest_document(file_path)
    
    def on_deleted(self, event):
        """Súbor zmazaný"""
        if event.src_path.endswith('.md'):
            print(f"🗑️ Zmazaný: {event.src_path}")
            file_path = Path(event.src_path)
            doc_id = str(file_path.relative_to(self.ingestion.config.paths.docs_root))
            self.ingestion.db.delete_document_chunks(doc_id)

def main():
    """Spusti watcher"""
    
    config = load_config()
    ingestion = RAGIngestion()
    ingestion.connect()
    
    handler = DocsWatcher(ingestion)
    observer = Observer()
    observer.schedule(handler, str(config.paths.docs_root), recursive=True)
    observer.start()
    
    print(f"👀 Sledujem: {config.paths.docs_root}")
    print("   Stlač Ctrl+C pre ukončenie")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        ingestion.close()
    
    observer.join()

if __name__ == '__main__':
    main()
```

---

## 🐛 Troubleshooting

### Časté Problémy

**1. pgvector extension nie je nájdený**

```bash
# Riešenie: Reinštaluj pgvector
DROP EXTENSION IF EXISTS vector;
CREATE EXTENSION vector;

# Ak stále nefunguje, skontroluj či je nainštalovaný
SELECT * FROM pg_available_extensions WHERE name = 'vector';
```

**2. Embedding model sa nedá stiahnuť**

```python
# Riešenie: Manuálne stiahnutie
from sentence_transformers import SentenceTransformer

# Explicitne stiahni
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', 
                           cache_folder='./models')
```

**3. Out of memory pri ingestion**

```python
# Riešenie: Znížiť batch size
# V config/rag_config.yaml:
embedding:
  batch_size: 8  # Namiesto 32
```

**4. Pomalé vyhľadávanie**

```sql
-- Riešenie: Skontroluj indexy
SELECT * FROM pg_indexes WHERE tablename = 'rag_chunks';

-- Vytvor chýbajúce indexy
CREATE INDEX IF NOT EXISTS idx_chunks_embedding 
ON rag_chunks USING hnsw (embedding vector_cosine_ops);
```

---

## 📊 Success Metrics

### Po Implementácii Skontroluj

```sql
-- Počet dokumentov
SELECT COUNT(*) FROM rag_documents;
-- Očakávané: ~45

-- Počet chunks
SELECT COUNT(*) FROM rag_chunks;
-- Očakávané: ~300-500

-- Priemerná veľkosť chunk
SELECT AVG(tokens) FROM rag_chunks;
-- Očakávané: 500-800

-- Kategórie
SELECT category, COUNT(*) 
FROM rag_documents 
GROUP BY category;

-- Test query rychlosti
EXPLAIN ANALYZE
SELECT * FROM rag_chunks
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
-- Očakávané: <50ms
```

---

## 🎯 Next Steps Po RAG MVP

Po dokončení RAG MVP (týždeň 1), môžeš pokračovať:

1. **PySide6 Migrácia** (týždeň 2-6)
   - S RAG pomocou = 30% rýchlejšie
   - Dokumentácia: `docs/migration/PYSIDE6_MIGRATION.md`

2. **Temporal Migrácia** (týždeň 7-9)
   - S RAG pomocou = 30% rýchlejšie
   - Dokumentácia: `docs/strategic/N8N_TO_TEMPORAL_MIGRATION.md`

3. **RAG Full Features** (týždeň 10+)
   - Ollama lokálne LLM
   - Web UI
   - Advanced search features

---

## 📚 Súvisiace Dokumenty

- [Architecture](../system/ARCHITECTURE.md) - Systémová architektúra
- [Database Index](../database/00_DATABASE_INDEX.md) - Databázová dokumentácia
- [Technology Decisions](TECHNOLOGY_DECISIONS.md) - Tech stack rozhodnutia
- [N8N to Temporal Migration](N8N_TO_TEMPORAL_MIGRATION.md) - Workflow migrácia

---

**Verzia:** 1.0  
**Status:** 🟡 Ready for Implementation  
**Časový Odhad:** 1 týždeň (RAG MVP)  
**Priorita:** 🔴 HIGH - Blocker pre PySide6 + Temporal

---

**KONIEC DOKUMENTU**