# Supplier Classifier - Project Blueprint

**Projekt:** Automatická klasifikácia dodávateľov z PDF faktúr pomocou Machine Learning  
**Časový horizont:** 2-4 týždne  
**Priorita:** VYSOKÁ (Quick Win projekt)  
**Status:** READY TO START  
**Vytvorené:** 2024-12-04

---

## 1. Project Overview

### 1.1 Účel projektu

Vytvoriť AI model, ktorý automaticky rozpozná dodávateľa z PDF faktúry bez manuálnej identifikácie. Model je prvým krokom v AI transformácii NEX Automat v2.0 a základ pre všetky ďalšie ML funkcie.

### 1.2 Problém, ktorý rieši

**SÚČASNÝ STAV:**
```
1. Email s faktúrou → PDF download
2. Človek otvorí PDF
3. Človek manuálne identifikuje: "Toto je od Magna Slovakia"
4. Človek vyberie správnu šablónu
5. Pokračuje spracovanie
```

**Problémy:**
- ⏱️ 30-60 sekúnd manuálnej práce per faktúra
- 👤 Závislé na ľudskom faktore
- ❌ Možnosť chyby (nesprávny dodávateľ = nesprávna šablóna)
- 📊 Nemožnosť automatického trackingu per dodávateľ

**NOVÝ STAV S AI:**
```
1. Email s faktúrou → PDF download
2. AI automaticky: "MAGNA_SLOVAKIA (97% confidence)"
3. Automaticky načíta správnu šablónu
4. Pokračuje spracovanie
```

**Benefity:**
- ⚡ 0 sekúnd manuálnej práce
- 🤖 Plná automatizácia
- ✅ 95%+ presnosť
- 📊 Automatický tracking

### 1.3 Business Value

**ROI pre pilotného zákazníka (Mágerstav s.r.o.):**
- **Objem:** 50 faktúr/deň (1000 faktúr/mesiac)
- **Úspora času:** 45 sekúnd per faktúra
- **Mesačná úspora:** 12.5 hodín = 1.5 pracovného dňa
- **Ročná úspora:** 150 hodín = takmer 1 FTE mesiac práce
- **Zvýšenie automatizácie:** 70% → 90%+

**Strategický benefit:**
- ✅ **Quick win** - funguje za 2-4 týždne
- ✅ **Foundation** - základ pre ďalšie AI modely (NER, anomaly detection)
- ✅ **Proof of concept** - dôkaz, že AI v NEX Automat funguje
- ✅ **Konkurenčná výhoda** - žiadny iný slovenský ERP nemá takúto automatizáciu

### 1.4 Cieľové metriky

**Technické metriky:**
- 🎯 **Accuracy:** 95%+ pre top 20 dodávateľov
- 🎯 **Confidence:** >0.85 pre 90%+ faktúr
- 🎯 **Processing time:** <200ms per faktúra
- 🎯 **False positive rate:** <2%

**Business metriky:**
- 🎯 **Automatizácia:** 90%+ faktúr bez manuálnej intervencie
- 🎯 **Time saving:** 30-60 sekúnd per faktúra
- 🎯 **Error reduction:** 80% zníženie chybovosti

---

## 2. Technical Architecture

### 2.1 Celková architektúra

```
┌─────────────────────────────────────────────────────────┐
│                    n8n Workflow                          │
│  Email → PDF Download → AI Classification → Processing   │
└────────────┬────────────────────────────────────────────┘
             │ HTTP POST Request
             ↓
┌─────────────────────────────────────────────────────────┐
│         FastAPI AI Service (Port 8001)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  POST /api/v1/classify-supplier                   │  │
│  │  Input: PDF file (multipart/form-data)            │  │
│  │  Output: {supplier_id, confidence, time_ms}       │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↓                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ PDF → Image  │→ │ Tesseract    │→ │ Feature      │  │
│  │ Conversion   │  │ OCR          │  │ Extraction   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                         ↓                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │    Scikit-learn Supplier Classifier Model          │ │
│  │    • RandomForest (100 trees)                      │ │
│  │    • TfidfVectorizer for features                  │ │
│  │    • 20 supplier classes                           │ │
│  │    Model files: supplier_classifier.pkl (~10 MB)   │ │
│  └────────────────────────────────────────────────────┘ │
└────────────┬────────────────────────────────────────────┘
             │ Stores predictions
             ↓
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
│  Schema: ml_training_data                               │
│  Tables:                                                 │
│    • supplier_predictions (log)                         │
│    • supplier_corrections (feedback loop)               │
│    • model_versions (versioning)                        │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Technologický stack

**Machine Learning:**
- **Framework:** Scikit-learn 1.3+
- **Model:** RandomForestClassifier
- **Feature extraction:** TfidfVectorizer
- **Serialization:** joblib

**Backend:**
- **API:** FastAPI 0.104+
- **Server:** Uvicorn
- **Async:** asyncio, aiofiles
- **OCR:** Tesseract 5.0+
- **PDF handling:** pdf2image, Pillow

**Database:**
- **PostgreSQL 14+** (existujúca inštancia)
- **Schema:** ml_training_data

**Deployment:**
- **OS:** Windows Server 2012 R2 (existujúci server)
- **Python:** 3.13
- **Process manager:** systemd service alebo Windows Service

**Development:**
- **Jupyter Notebook** - experimentovanie a trénovanie
- **Git** - version control
- **pytest** - testovanie

### 2.3 Server špecifikácie

**Existujúci NEX Genesis Server:**
- ✅ **CPU:** 12 jadier - PERFEKTNÉ
- ✅ **RAM:** 128 GB - VIAC NEŽ DOSŤ
- ✅ **GPU:** Nie je potrebné
- ✅ **Disk:** SSD - stačí 10 GB pre modely a dáta

**Očakávané využitie:**
- CPU: 20-30% priemer (2-4 jadrá)
- RAM: 5-10 GB (modely + inference)
- Processing: 10-20 faktúr paralelne bez problémov

### 2.4 Integračné body

**n8n workflow integration:**
```
[Existing Supplier Invoice Workflow]
    ↓
[Email Trigger] → Zostáva
[Download PDF] → Zostáva
    ↓
[NEW NODE: HTTP Request]
    • URL: http://localhost:8001/api/v1/classify-supplier
    • Method: POST
    • Body: PDF file (multipart)
    • Response: {supplier_id, confidence}
    ↓
[Switch Node]
    • IF confidence >= 0.85: Use AI prediction
    • ELSE: Fallback to manual/OCR logic
    ↓
[Continue existing workflow] → Zostáva
```

---

## 3. Data Requirements

### 3.1 Trénovacie dáta

**Minimálne požiadavky:**
- **Počet dodávateľov:** 20 (top dodávatelia podľa objemu)
- **Faktúry per dodávateľ:** 50-100 minimum
- **Celkový dataset:** 1000-2000 faktúr
- **Formát:** PDF + metadata

**Dataset štruktúra:**
```
training_data/
├── metadata.csv
│   Stĺpce: invoice_id, supplier_id, supplier_name, date, amount, pdf_path
│
└── pdfs/
    ├── invoice_001.pdf
    ├── invoice_002.pdf
    └── ...
```

**Zdroj dát:**
- Export z NEX Genesis (Btrieve)
- Faktúry za posledných 6-12 mesiacov
- Rôznorodosť: rôzne formáty PDF od rovnakého dodávateľa

### 3.2 Data split

```
Training set:   70% (700-1400 faktúr)
Validation set: 15% (150-300 faktúr)
Test set:       15% (150-300 faktúr)
```

**Stratified split** - rovnomerné zastúpenie všetkých dodávateľov v každom sete.

### 3.3 Features

**Text features z OCR:**
```python
# TF-IDF features z celého textu faktúry
vectorizer = TfidfVectorizer(
    max_features=1000,        # Top 1000 slov
    ngram_range=(1, 2),       # Unigrams + bigrams
    min_df=2,                 # Slovo musí byť v min 2 dokumentoch
    stop_words='english'      # Remove common words
)
```

**Dodatočné features (optional):**
- Dĺžka textu
- Počet číselných znakov
- Prítomnosť kľúčových slov (IČO, DIČ, IBAN)
- Layout features (počet riadkov, priemerná dĺžka riadku)

### 3.4 Labels

```python
# Supplier mapping
SUPPLIERS = {
    1: "MAGNA_SLOVAKIA",
    2: "ANDROS_SK",
    3: "STAVEBNINY_XYZ",
    4: "ELEKTRO_COMPANY",
    # ... top 20 dodávateľov
    0: "UNKNOWN"  # Pre neznámych dodávateľov
}
```

**Label encoding:**
- Kategorické labels → číselné ID
- Scikit-learn automaticky handles multi-class classification

---

## 4. Implementation Plan

### PHASE 1: Setup & Data Preparation (Week 1)

#### 1.1 Environment Setup (Day 1-2)

**Tasks:**
```bash
# 1. Vytvorenie Python virtual environment
cd /path/to/nex-automat
python -m venv venv_ml
source venv_ml/bin/activate  # Linux
# alebo
venv_ml\Scripts\activate  # Windows

# 2. Inštalácia dependencies
pip install --upgrade pip
pip install scikit-learn==1.3.2
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install matplotlib==3.8.2
pip install seaborn==0.13.0
pip install jupyter==1.0.0
pip install pytesseract==0.3.10
pip install pdf2image==1.16.3
pip install Pillow==10.1.0
pip install joblib==1.3.2
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install aiofiles==23.2.1

# 3. Save requirements
pip freeze > requirements_ml.txt
```

**Setup Tesseract:**
```bash
# Windows: Download installer
# https://github.com/UB-Mannheim/tesseract/wiki

# Linux:
sudo apt-get install tesseract-ocr
```

**Create project structure:**
```
nex-automat/
├── ml_service/
│   ├── __init__.py
│   ├── api.py                 # FastAPI app
│   ├── classifier.py          # Model loading & inference
│   ├── preprocessing.py       # PDF → features
│   └── config.py              # Configuration
│
├── ml_models/
│   ├── supplier_classifier.pkl
│   ├── vectorizer.pkl
│   └── model_metadata.json
│
├── training/
│   ├── notebooks/
│   │   └── supplier_classifier_training.ipynb
│   ├── data/
│   │   ├── raw/              # Original PDFs
│   │   └── processed/        # OCR text files
│   └── scripts/
│       ├── export_data.py
│       └── train_model.py
│
└── docs/
    └── projects/
        └── SUPPLIER_CLASSIFIER_BLUEPRINT.md
```

**Deliverables:**
- ✅ Python ML environment ready
- ✅ Project structure created
- ✅ Tesseract OCR working

---

#### 1.2 Data Export (Day 2-3)

**SQL query pre export faktúr z NEX Genesis:**
```sql
-- Top 20 dodávateľov podľa počtu faktúr
SELECT 
    supplier_id,
    supplier_name,
    COUNT(*) as invoice_count
FROM invoices
WHERE date >= '2023-01-01'
GROUP BY supplier_id, supplier_name
ORDER BY invoice_count DESC
LIMIT 20;

-- Export faktúr pre týchto dodávateľov
-- Minimum 50 faktúr per dodávateľ
```

**Python script pre export:**
```python
# training/scripts/export_data.py

import pandas as pd
import shutil
from pathlib import Path

def export_supplier_invoices(supplier_ids, min_count=50):
    """
    Export faktúr z NEX Genesis pre training.
    
    Args:
        supplier_ids: List top 20 supplier IDs
        min_count: Minimum faktúr per dodávateľ
    """
    
    # 1. Connect to database (Btrieve/PostgreSQL)
    # 2. Query invoices for each supplier
    # 3. Copy PDF files to training_data/raw/
    # 4. Create metadata.csv
    
    metadata = []
    
    for supplier_id in supplier_ids:
        invoices = query_invoices(supplier_id, limit=min_count)
        
        for invoice in invoices:
            # Copy PDF
            src = invoice['pdf_path']
            dst = f"training/data/raw/{invoice['invoice_id']}.pdf"
            shutil.copy(src, dst)
            
            # Add to metadata
            metadata.append({
                'invoice_id': invoice['invoice_id'],
                'supplier_id': supplier_id,
                'supplier_name': invoice['supplier_name'],
                'date': invoice['date'],
                'amount': invoice['amount'],
                'pdf_path': dst
            })
    
    # Save metadata
    df = pd.DataFrame(metadata)
    df.to_csv('training/data/metadata.csv', index=False)
    
    print(f"Exported {len(metadata)} invoices from {len(supplier_ids)} suppliers")
    return df

# Usage:
top_suppliers = [1, 2, 3, ...]  # From SQL query
df = export_supplier_invoices(top_suppliers)
```

**Data validation:**
```python
# Check data quality
df = pd.read_csv('training/data/metadata.csv')

# Distribution per supplier
print(df['supplier_name'].value_counts())

# Minimum check
assert df['supplier_name'].value_counts().min() >= 50, "Some suppliers have <50 invoices!"
```

**Deliverables:**
- ✅ 1000+ faktúr exportovaných
- ✅ metadata.csv created
- ✅ Data quality validated

---

#### 1.3 OCR Processing (Day 3-4)

**Batch OCR script:**
```python
# training/scripts/ocr_batch.py

import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def ocr_invoice(pdf_path):
    """
    Extract text from PDF using Tesseract OCR.
    
    Returns:
        str: Extracted text
    """
    try:
        # Convert PDF to images (první strana stačí pro většinu faktur)
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        
        # OCR first page
        text = pytesseract.image_to_string(images[0], lang='eng+slk')
        
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""

def batch_ocr_processing():
    """Process all invoices and save OCR text."""
    
    df = pd.read_csv('training/data/metadata.csv')
    
    ocr_texts = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        pdf_path = row['pdf_path']
        invoice_id = row['invoice_id']
        
        # OCR
        text = ocr_invoice(pdf_path)
        
        # Save text file
        text_path = f"training/data/processed/{invoice_id}.txt"
        Path(text_path).write_text(text, encoding='utf-8')
        
        ocr_texts.append({
            'invoice_id': invoice_id,
            'text': text,
            'text_length': len(text)
        })
    
    # Save OCR results
    ocr_df = pd.DataFrame(ocr_texts)
    ocr_df.to_csv('training/data/ocr_results.csv', index=False)
    
    print(f"OCR completed for {len(ocr_df)} invoices")
    print(f"Average text length: {ocr_df['text_length'].mean():.0f} chars")
    
    return ocr_df

# Usage:
ocr_df = batch_ocr_processing()
```

**Deliverables:**
- ✅ OCR text pre všetky faktúry
- ✅ ocr_results.csv created
- ✅ Text quality validated

---

### PHASE 2: Model Development (Week 2)

#### 2.1 Jupyter Notebook Exploration (Day 5-6)

**Create training notebook:**
```python
# training/notebooks/supplier_classifier_training.ipynb

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ========================================
# 1. LOAD DATA
# ========================================

metadata = pd.read_csv('../data/metadata.csv')
ocr_results = pd.read_csv('../data/ocr_results.csv')

# Merge
df = metadata.merge(ocr_results, on='invoice_id')

print(f"Total invoices: {len(df)}")
print(f"Suppliers: {df['supplier_name'].nunique()}")
print("\nDistribution:")
print(df['supplier_name'].value_counts())

# ========================================
# 2. PREPARE DATA
# ========================================

# Features (X) and labels (y)
X = df['text'].values
y = df['supplier_id'].values

# Train/validation/test split
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

print(f"\nTrain: {len(X_train)}")
print(f"Validation: {len(X_val)}")
print(f"Test: {len(X_test)}")

# ========================================
# 3. FEATURE EXTRACTION
# ========================================

vectorizer = TfidfVectorizer(
    max_features=1000,
    ngram_range=(1, 2),
    min_df=2,
    stop_words='english'
)

# Fit on training data only
X_train_features = vectorizer.fit_transform(X_train)
X_val_features = vectorizer.transform(X_val)
X_test_features = vectorizer.transform(X_test)

print(f"\nFeature matrix shape: {X_train_features.shape}")

# ========================================
# 4. BASELINE MODEL
# ========================================

print("\n" + "="*50)
print("TRAINING BASELINE MODEL")
print("="*50)

baseline_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

baseline_model.fit(X_train_features, y_train)

# Evaluate on validation set
val_accuracy = baseline_model.score(X_val_features, y_val)
print(f"\nValidation Accuracy: {val_accuracy:.4f}")

# Detailed metrics
y_val_pred = baseline_model.predict(X_val_features)
print("\nClassification Report:")
print(classification_report(y_val, y_val_pred, target_names=df['supplier_name'].unique()))

# ========================================
# 5. HYPERPARAMETER TUNING
# ========================================

from sklearn.model_selection import GridSearchCV

print("\n" + "="*50)
print("HYPERPARAMETER TUNING")
print("="*50)

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid,
    cv=5,
    scoring='accuracy',
    verbose=1
)

grid_search.fit(X_train_features, y_train)

print(f"\nBest parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")

best_model = grid_search.best_estimator_

# ========================================
# 6. FINAL EVALUATION ON TEST SET
# ========================================

print("\n" + "="*50)
print("FINAL EVALUATION ON TEST SET")
print("="*50)

test_accuracy = best_model.score(X_test_features, y_test)
print(f"\nTest Accuracy: {test_accuracy:.4f}")

y_test_pred = best_model.predict(X_test_features)
y_test_proba = best_model.predict_proba(X_test_features)

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig('../outputs/confusion_matrix.png')
plt.show()

# ========================================
# 7. CONFIDENCE ANALYSIS
# ========================================

# Analyze prediction confidence
max_proba = y_test_proba.max(axis=1)

plt.figure(figsize=(10, 6))
plt.hist(max_proba, bins=50, edgecolor='black')
plt.xlabel('Confidence Score')
plt.ylabel('Number of Predictions')
plt.title('Distribution of Prediction Confidence')
plt.axvline(x=0.85, color='red', linestyle='--', label='Threshold (0.85)')
plt.legend()
plt.savefig('../outputs/confidence_distribution.png')
plt.show()

high_confidence = (max_proba >= 0.85).sum()
print(f"\nPredictions with confidence >= 0.85: {high_confidence}/{len(y_test)} ({high_confidence/len(y_test)*100:.1f}%)")

# ========================================
# 8. SAVE MODEL
# ========================================

print("\n" + "="*50)
print("SAVING MODEL")
print("="*50)

# Save model
joblib.dump(best_model, '../../ml_models/supplier_classifier.pkl')
joblib.dump(vectorizer, '../../ml_models/vectorizer.pkl')

# Save metadata
model_metadata = {
    'model_type': 'RandomForestClassifier',
    'parameters': best_model.get_params(),
    'test_accuracy': float(test_accuracy),
    'n_suppliers': int(df['supplier_id'].nunique()),
    'n_features': int(X_train_features.shape[1]),
    'training_samples': int(len(X_train)),
    'trained_date': pd.Timestamp.now().isoformat(),
    'supplier_mapping': df[['supplier_id', 'supplier_name']].drop_duplicates().to_dict('records')
}

import json
with open('../../ml_models/model_metadata.json', 'w') as f:
    json.dump(model_metadata, f, indent=2)

print("\nModel saved successfully!")
print(f"Model size: {Path('../../ml_models/supplier_classifier.pkl').stat().st_size / 1024 / 1024:.2f} MB")
```

**Deliverables:**
- ✅ Trained model (95%+ accuracy)
- ✅ Model files saved (supplier_classifier.pkl, vectorizer.pkl)
- ✅ Evaluation report
- ✅ Confidence analysis

---

#### 2.2 Model Optimization (Day 7)

**Focus areas:**
1. Feature engineering improvements
2. Handling class imbalance (if any)
3. Model ensemble (if needed)
4. Confidence threshold tuning

**Target metrics:**
- Accuracy: 95%+
- High confidence predictions: 90%+
- False positive rate: <2%

---

### PHASE 3: API Development (Week 3)

#### 3.1 FastAPI Service (Day 8-9)

**Create ml_service/api.py:**
```python
# ml_service/api.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import time
from .classifier import SupplierClassifier
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title="NEX Automat AI Service",
    description="Machine Learning API for NEX Automat v2.0",
    version="1.0.0"
)

# Global classifier instance
classifier = None

@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    global classifier
    print("Loading ML models...")
    classifier = SupplierClassifier(
        model_path=settings.MODEL_PATH,
        vectorizer_path=settings.VECTORIZER_PATH
    )
    print("Models loaded successfully!")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "nex-automat-ai-service",
        "models_loaded": classifier is not None
    }

@app.post("/api/v1/classify-supplier")
async def classify_supplier(file: UploadFile = File(...)):
    """
    Classify supplier from invoice PDF.
    
    Args:
        file: PDF file (multipart/form-data)
    
    Returns:
        {
            "supplier_id": str,
            "supplier_name": str,
            "confidence": float,
            "processing_time_ms": int,
            "needs_review": bool
        }
    """
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    start_time = time.time()
    
    try:
        # Read PDF file
        pdf_content = await file.read()
        
        # Classify
        result = classifier.predict(pdf_content)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "supplier_id": result['supplier_id'],
            "supplier_name": result['supplier_name'],
            "confidence": round(result['confidence'], 4),
            "processing_time_ms": processing_time,
            "needs_review": result['confidence'] < settings.CONFIDENCE_THRESHOLD
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")

@app.post("/api/v1/supplier-feedback")
async def supplier_feedback(
    invoice_id: str,
    predicted_supplier: str,
    actual_supplier: str,
    confidence: float
):
    """
    Log user corrections for model retraining.
    
    This creates a feedback loop for continuous improvement.
    """
    
    # TODO: Save to PostgreSQL ml_training_data.supplier_corrections
    
    return {
        "status": "feedback_recorded",
        "invoice_id": invoice_id,
        "will_be_used_for": "model_retraining"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Create ml_service/classifier.py:**
```python
# ml_service/classifier.py

import joblib
import pytesseract
from pdf2image import convert_from_bytes
from pathlib import Path
import numpy as np

class SupplierClassifier:
    """Supplier classification from invoice PDF."""
    
    def __init__(self, model_path: str, vectorizer_path: str):
        """
        Initialize classifier with trained models.
        
        Args:
            model_path: Path to supplier_classifier.pkl
            vectorizer_path: Path to vectorizer.pkl
        """
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
        # Load supplier mapping
        import json
        metadata_path = Path(model_path).parent / 'model_metadata.json'
        with open(metadata_path) as f:
            metadata = json.load(f)
            self.supplier_mapping = {
                s['supplier_id']: s['supplier_name'] 
                for s in metadata['supplier_mapping']
            }
    
    def predict(self, pdf_content: bytes) -> dict:
        """
        Predict supplier from PDF content.
        
        Args:
            pdf_content: PDF file as bytes
            
        Returns:
            {
                'supplier_id': str,
                'supplier_name': str,
                'confidence': float
            }
        """
        # 1. Convert PDF to image
        images = convert_from_bytes(pdf_content, first_page=1, last_page=1)
        
        # 2. OCR
        text = pytesseract.image_to_string(images[0], lang='eng+slk')
        
        # 3. Extract features
        features = self.vectorizer.transform([text])
        
        # 4. Predict
        supplier_id = self.model.predict(features)[0]
        confidence = self.model.predict_proba(features).max()
        
        # 5. Map to supplier name
        supplier_name = self.supplier_mapping.get(supplier_id, "UNKNOWN")
        
        return {
            'supplier_id': str(supplier_id),
            'supplier_name': supplier_name,
            'confidence': float(confidence)
        }
```

**Create ml_service/config.py:**
```python
# ml_service/config.py

from pathlib import Path

class Settings:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_PATH = BASE_DIR / "ml_models" / "supplier_classifier.pkl"
    VECTORIZER_PATH = BASE_DIR / "ml_models" / "vectorizer.pkl"
    
    # Thresholds
    CONFIDENCE_THRESHOLD = 0.85  # Predictions below this need manual review
    
    # API
    API_HOST = "0.0.0.0"
    API_PORT = 8001

settings = Settings()
```

**Deliverables:**
- ✅ FastAPI service implemented
- ✅ /classify-supplier endpoint working
- ✅ /health endpoint
- ✅ Error handling

---

#### 3.2 Testing (Day 10)

**Unit tests:**
```python
# tests/test_classifier.py

import pytest
from ml_service.classifier import SupplierClassifier

def test_classifier_initialization():
    """Test model loading."""
    classifier = SupplierClassifier(
        model_path="ml_models/supplier_classifier.pkl",
        vectorizer_path="ml_models/vectorizer.pkl"
    )
    assert classifier.model is not None
    assert classifier.vectorizer is not None

def test_prediction():
    """Test prediction on sample invoice."""
    classifier = SupplierClassifier(...)
    
    with open("tests/sample_invoice_magna.pdf", "rb") as f:
        result = classifier.predict(f.read())
    
    assert result['supplier_name'] == "MAGNA_SLOVAKIA"
    assert result['confidence'] > 0.85

# Run: pytest tests/
```

**Integration tests:**
```python
# tests/test_api.py

from fastapi.testclient import TestClient
from ml_service.api import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_classify_endpoint():
    """Test classification endpoint."""
    with open("tests/sample_invoice.pdf", "rb") as f:
        response = client.post(
            "/api/v1/classify-supplier",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "supplier_id" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1
```

**Deliverables:**
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ Test coverage >80%

---

### PHASE 4: Integration & Deployment (Week 4)

#### 4.1 n8n Workflow Integration (Day 11-12)

**Modified Supplier Invoice workflow:**

```json
{
  "name": "Supplier Invoice Processing with AI",
  "nodes": [
    {
      "name": "Email Trigger",
      "type": "n8n-nodes-base.emailReadImap",
      "position": [250, 300],
      "parameters": { ... }
    },
    {
      "name": "Download PDF",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": { ... }
    },
    {
      "name": "AI Supplier Classifier",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300],
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8001/api/v1/classify-supplier",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "file",
              "value": "={{ $binary.data }}"
            }
          ]
        },
        "options": {
          "timeout": 10000
        }
      }
    },
    {
      "name": "Confidence Check",
      "type": "n8n-nodes-base.switch",
      "position": [850, 300],
      "parameters": {
        "rules": {
          "rules": [
            {
              "operation": "largerEqual",
              "value1": "={{ $json.confidence }}",
              "value2": 0.85
            }
          ]
        }
      }
    },
    {
      "name": "Use AI Prediction",
      "type": "n8n-nodes-base.set",
      "position": [1050, 250],
      "parameters": {
        "values": {
          "string": [
            {
              "name": "supplier_id",
              "value": "={{ $json.supplier_id }}"
            }
          ]
        }
      }
    },
    {
      "name": "Manual Review Needed",
      "type": "n8n-nodes-base.sendEmail",
      "position": [1050, 400],
      "parameters": {
        "subject": "Invoice needs manual review",
        "text": "Confidence: {{ $json.confidence }}"
      }
    }
  ]
}
```

**Fallback logic:**
```javascript
// IF confidence < 0.85
// THEN trigger manual review or use old OCR logic
// ELSE use AI prediction and continue
```

**Deliverables:**
- ✅ n8n workflow updated
- ✅ AI integration working
- ✅ Fallback logic implemented

---

#### 4.2 Database Setup (Day 12)

**PostgreSQL schema:**
```sql
-- Create schema for ML data
CREATE SCHEMA IF NOT EXISTS ml_training_data;

-- Table for prediction logs
CREATE TABLE ml_training_data.supplier_predictions (
    id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(100),
    predicted_supplier_id VARCHAR(50),
    predicted_supplier_name VARCHAR(200),
    confidence DECIMAL(5, 4),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_invoice ON ml_training_data.supplier_predictions(invoice_id);
CREATE INDEX idx_predictions_created ON ml_training_data.supplier_predictions(created_at);

-- Table for user corrections (feedback loop)
CREATE TABLE ml_training_data.supplier_corrections (
    id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(100),
    predicted_supplier VARCHAR(50),
    actual_supplier VARCHAR(50),
    confidence DECIMAL(5, 4),
    corrected_by VARCHAR(100),
    corrected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for model versions
CREATE TABLE ml_training_data.model_versions (
    id SERIAL PRIMARY KEY,
    version VARCHAR(20),
    model_type VARCHAR(50),
    accuracy DECIMAL(5, 4),
    parameters JSONB,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE
);

-- Insert initial model version
INSERT INTO ml_training_data.model_versions (version, model_type, accuracy, is_active)
VALUES ('v1.0', 'RandomForest', 0.95, TRUE);
```

**Deliverables:**
- ✅ Database schema created
- ✅ Logging enabled

---

#### 4.3 Deployment (Day 13-14)

**Windows Service setup:**
```python
# ml_service/run_service.py

import uvicorn
from api import app
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level="info",
        access_log=True
    )
```

**Create Windows Service (using NSSM):**
```powershell
# Download NSSM (Non-Sucking Service Manager)
# https://nssm.cc/download

# Install service
nssm install NEXAutomatAI "C:\path\to\python.exe" "C:\path\to\ml_service\run_service.py"

# Configure
nssm set NEXAutomatAI AppDirectory "C:\path\to\nex-automat"
nssm set NEXAutomatAI DisplayName "NEX Automat AI Service"
nssm set NEXAutomatAI Description "Machine Learning API for supplier classification"
nssm set NEXAutomatAI Start SERVICE_AUTO_START

# Start service
nssm start NEXAutomatAI

# Check status
nssm status NEXAutomatAI
```

**Health monitoring:**
```python
# Simple health check script
import requests
import time

while True:
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print(f"✅ Service healthy at {time.ctime()}")
        else:
            print(f"⚠️ Service returned {response.status_code}")
    except Exception as e:
        print(f"❌ Service unreachable: {e}")
    
    time.sleep(60)  # Check every minute
```

**Deliverables:**
- ✅ Service deployed
- ✅ Auto-start configured
- ✅ Monitoring active
- ✅ Production ready

---

## 5. Code Templates & Examples

### 5.1 Quick Start - Minimal Example

**Simplest possible implementation:**
```python
# minimal_classifier.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pytesseract
from pdf2image import convert_from_path

# 1. TRAINING (once)
def train_model(invoice_texts, supplier_labels):
    # Extract features
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(invoice_texts)
    
    # Train
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, supplier_labels)
    
    # Save
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

# 2. INFERENCE (in production)
def classify_invoice(pdf_path):
    # Load models
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    
    # OCR
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    text = pytesseract.image_to_string(images[0])
    
    # Predict
    features = vectorizer.transform([text])
    supplier = model.predict(features)[0]
    confidence = model.predict_proba(features).max()
    
    return supplier, confidence

# Usage:
supplier, conf = classify_invoice('invoice.pdf')
print(f"Supplier: {supplier}, Confidence: {conf:.2%}")
```

**This is it!** 50 lines of code = working supplier classifier.

---

### 5.2 Production-Ready Template

**See ml_service/api.py above** for full production implementation with:
- FastAPI endpoints
- Error handling
- Logging
- Model versioning
- Feedback loop

---

## 6. Testing Strategy

### 6.1 Unit Tests

```python
# tests/test_classifier.py

def test_ocr_extraction():
    """Test OCR text extraction."""
    text = ocr_invoice("tests/sample.pdf")
    assert len(text) > 100
    assert "IČO" in text or "ICO" in text

def test_feature_extraction():
    """Test TF-IDF vectorization."""
    vectorizer = load_vectorizer()
    text = "Sample invoice text"
    features = vectorizer.transform([text])
    assert features.shape[1] == 1000  # max_features

def test_model_prediction():
    """Test model prediction."""
    model = load_model()
    features = get_sample_features()
    prediction = model.predict(features)
    assert prediction[0] in range(1, 21)  # Valid supplier ID
```

### 6.2 Integration Tests

```python
def test_end_to_end():
    """Test complete pipeline."""
    # 1. Load PDF
    pdf_path = "tests/magna_invoice.pdf"
    
    # 2. Classify
    result = classify_supplier(pdf_path)
    
    # 3. Validate
    assert result['supplier_name'] == "MAGNA_SLOVAKIA"
    assert result['confidence'] >= 0.85
```

### 6.3 Acceptance Criteria

**Before Go-Live, verify:**
- ✅ Accuracy >= 95% on test set
- ✅ Processing time < 200ms per invoice
- ✅ API response time < 500ms
- ✅ 90%+ predictions have confidence >= 0.85
- ✅ False positive rate < 2%
- ✅ Service uptime > 99%
- ✅ n8n integration working smoothly

---

## 7. Deployment Plan

### 7.1 Pre-Deployment Checklist

```
Infrastructure:
□ Server resources checked (CPU, RAM, disk)
□ Python 3.13 installed
□ Tesseract OCR installed
□ PostgreSQL schema created
□ Network ports configured (8001)

Code:
□ All tests passing
□ Code reviewed
□ Documentation complete
□ Config files prepared

Data:
□ Models trained and validated
□ Model files < 50 MB
□ Metadata JSON created
□ Supplier mapping complete
```

### 7.2 Deployment Steps

**Day 1: Staging Deployment**
```bash
# 1. Deploy to staging environment
git clone <repo>
cd nex-automat
python -m venv venv_ml
source venv_ml/bin/activate
pip install -r requirements_ml.txt

# 2. Copy model files
cp trained_models/* ml_models/

# 3. Configure
nano ml_service/config.py  # Update paths

# 4. Start service
python ml_service/run_service.py

# 5. Test
curl http://localhost:8001/health
# Test with sample invoice
```

**Day 2: Production Deployment**
```bash
# 1. Backup current system
pg_dump nex_automat > backup.sql

# 2. Deploy to production
# Same steps as staging

# 3. Configure as service
nssm install NEXAutomatAI ...

# 4. Update n8n workflow
# Import new workflow JSON

# 5. Smoke test
# Process 5 test invoices manually
```

**Day 3: Monitoring**
```
# Monitor for 24 hours:
- Check API logs
- Monitor prediction accuracy
- Watch confidence scores
- Track processing times
- Check error rates
```

### 7.3 Rollback Plan

**If issues detected:**
```bash
# 1. Stop AI service
nssm stop NEXAutomatAI

# 2. Revert n8n workflow
# Re-import old workflow (without AI node)

# 3. Check issues
tail -f logs/ai_service.log

# 4. Fix and redeploy
```

**Rollback triggers:**
- Accuracy drops below 90%
- Processing time > 2 seconds
- Service crashes repeatedly
- False positive rate > 5%

---

## 8. Success Metrics & KPIs

### 8.1 Technical Metrics

**Model Performance:**
```
Target metrics (measured weekly):

Accuracy:
- Overall: >= 95%
- Per supplier: >= 90%

Confidence:
- High confidence (>=0.85): >= 90% of predictions
- Average confidence: >= 0.92

Speed:
- OCR time: < 1000ms
- Classification time: < 200ms
- Total API response: < 1500ms

Reliability:
- Service uptime: > 99%
- Error rate: < 1%
```

**Dashboard KPIs:**
```sql
-- Daily metrics query
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_predictions,
    AVG(confidence) as avg_confidence,
    AVG(processing_time_ms) as avg_time_ms,
    SUM(CASE WHEN confidence >= 0.85 THEN 1 ELSE 0 END) as high_confidence_count,
    SUM(CASE WHEN confidence < 0.85 THEN 1 ELSE 0 END) as needs_review_count
FROM ml_training_data.supplier_predictions
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### 8.2 Business Metrics

**Time Savings:**
```
Baseline: 45 seconds per invoice (manual identification)

With AI:
- High confidence (90%): 0 seconds
- Manual review (10%): 15 seconds

Average savings:
0.9 * 45 + 0.1 * (-15) = 39 seconds per invoice

For Mágerstav (50 invoices/day):
Daily: 50 * 39s = 32.5 minutes
Monthly: ~16 hours
Yearly: ~195 hours
```

**Automation Rate:**
```
Before: 70% automation
After: 90%+ automation

Improvement: +20 percentage points
```

**Error Reduction:**
```
Manual errors: ~3-5% (wrong template selection)
AI errors: <1% (false positives)

Improvement: 80% error reduction
```

### 8.3 User Satisfaction

**Measure via:**
- Feedback from operators
- Number of manual corrections
- Time to process batch of invoices
- Overall satisfaction score (1-5)

**Target:** 4.5+ satisfaction score

---

## 9. Troubleshooting Guide

### 9.1 Common Issues

**Issue 1: Low Accuracy (<90%)**
```
Symptoms:
- Model frequently misclassifies invoices
- Confidence scores consistently low

Diagnosis:
- Check data quality: Are training PDFs good quality?
- Check feature extraction: Is OCR working properly?
- Check class balance: Are all suppliers well represented?

Solutions:
1. Collect more training data (aim for 100+ per supplier)
2. Improve OCR quality (better PDFs, adjust Tesseract settings)
3. Try different features (add layout features, bigrams)
4. Retrain with balanced dataset
```

**Issue 2: Slow Processing (>2s per invoice)**
```
Symptoms:
- API timeout errors
- n8n workflow delays
- High CPU usage

Diagnosis:
- Check OCR time (should be <1s)
- Check model size (should be <50 MB)
- Monitor CPU/RAM usage

Solutions:
1. Optimize OCR: Use first page only
2. Reduce max_features in TfidfVectorizer (1000 → 500)
3. Use smaller model: Reduce n_estimators (200 → 100)
4. Enable parallel processing (n_jobs=-1)
```

**Issue 3: Service Crashes**
```
Symptoms:
- API unreachable
- 500 errors
- Service stops randomly

Diagnosis:
- Check logs: tail -f logs/ai_service.log
- Check memory: Is RAM exhausted?
- Check disk: Is disk full?

Solutions:
1. Restart service: nssm restart NEXAutomatAI
2. Check model loading: Ensure files exist and are valid
3. Add error handling: Catch all exceptions
4. Increase timeout: In n8n HTTP Request node
```

**Issue 4: Poor Confidence Scores**
```
Symptoms:
- Many predictions with confidence <0.85
- Requires frequent manual review

Diagnosis:
- Check if new supplier types appearing
- Check PDF quality variance
- Check if suppliers changed invoice formats

Solutions:
1. Retrain with recent data
2. Add new suppliers to training set
3. Adjust confidence threshold (0.85 → 0.80)
4. Implement ensemble model (multiple classifiers)
```

### 9.2 Debug Commands

```bash
# Check service status
nssm status NEXAutomatAI

# View logs
tail -f logs/ai_service.log

# Test API manually
curl -X POST http://localhost:8001/api/v1/classify-supplier \
  -F "file=@test_invoice.pdf"

# Check model files
ls -lh ml_models/
# Should see: supplier_classifier.pkl, vectorizer.pkl, model_metadata.json

# Python debug session
python
>>> from ml_service.classifier import SupplierClassifier
>>> clf = SupplierClassifier(...)
>>> result = clf.predict(open('test.pdf', 'rb').read())
>>> print(result)

# Database queries
psql -d nex_automat
SELECT * FROM ml_training_data.supplier_predictions ORDER BY created_at DESC LIMIT 10;
```

### 9.3 Performance Optimization

**If processing is slow:**
```python
# 1. Cache models in memory (done in FastAPI @startup)

# 2. Batch processing for multiple invoices
async def classify_batch(files: List[UploadFile]):
    results = []
    for file in files:
        result = await classify_supplier(file)
        results.append(result)
    return results

# 3. Reduce OCR quality for speed (if acceptable)
images = convert_from_bytes(pdf_content, dpi=150)  # Instead of 300

# 4. Use lightweight model
model = RandomForestClassifier(n_estimators=50)  # Instead of 200
```

---

## 10. Next Steps & Future Enhancements

### 10.1 Immediate Next Steps (After Go-Live)

**Week 1-2: Monitoring & Stabilization**
1. Monitor prediction accuracy daily
2. Collect user feedback
3. Fix any critical bugs
4. Tune confidence threshold if needed

**Week 3-4: Feedback Loop Implementation**
1. Enable correction logging in n8n
2. Collect corrections from users
3. Analyze common errors
4. Plan first model retraining

**Month 2: First Model Update**
1. Retrain with new data (including corrections)
2. Evaluate improvement
3. Deploy model v1.1
4. Compare metrics

### 10.2 Short-Term Enhancements (1-3 months)

**Enhancement 1: Multi-Language Support**
- Add Slovak-specific OCR models
- Improve handling of Czech/Hungarian invoices

**Enhancement 2: Confidence Explanation**
- Show why model classified as X
- Display top features contributing to decision
- Help users trust predictions

**Enhancement 3: Template Auto-Selection**
- Automatically load supplier-specific template
- Reduce manual template selection

**Enhancement 4: Batch Processing**
- Process 10-20 invoices at once
- Bulk classification endpoint

### 10.3 Medium-Term Enhancements (3-6 months)

**Enhancement 5: NER Integration**
- Add Named Entity Recognition
- Extract IČO, DIČ, sumy, dátumy automatically
- Eliminate template dependency

**Enhancement 6: Anomaly Detection**
- Detect suspicious invoices
- Alert on unusual amounts
- Fraud detection

**Enhancement 7: Auto-Approval Predictor**
- ML model to decide: auto-approve vs manual review
- Based on supplier, amount, history

**Enhancement 8: Dashboard & Analytics**
- Real-time prediction monitoring
- Per-supplier accuracy tracking
- Processing time analytics
- ROI calculation

### 10.4 Long-Term Vision (6-12 months)

**Vision: Fully Autonomous Invoice Processing**

```
Email → AI Classification → AI Extraction → AI Validation → 
AI Approval → Automatic Posting to NEX Genesis

Human intervention only for exceptions (5-10% of invoices)
```

**Components:**
1. ✅ Supplier Classifier (Phase 1 - DONE)
2. NER Extraction Model (Phase 2)
3. Anomaly Detection (Phase 3)
4. Auto-Approval Model (Phase 4)
5. Complete Integration (Phase 5)

**Expected Outcome:**
- 95%+ full automation
- <1% error rate
- 1-2 FTE savings per customer
- Unique competitive advantage

---

## 11. Resources & References

### 11.1 Documentation

**Scikit-learn:**
- Official docs: https://scikit-learn.org/stable/
- RandomForest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- TF-IDF: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

**FastAPI:**
- Official docs: https://fastapi.tiangolo.com/
- File uploads: https://fastapi.tiangolo.com/tutorial/request-files/

**Tesseract OCR:**
- GitHub: https://github.com/tesseract-ocr/tesseract
- pytesseract: https://pypi.org/project/pytesseract/

### 11.2 Training Materials

**Scikit-learn Tutorials:**
- Text Classification: https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
- Model Selection: https://scikit-learn.org/stable/model_selection.html

**Books:**
- "Hands-On Machine Learning" by Aurélien Géron
- "Python Machine Learning" by Sebastian Raschka

### 11.3 Tools

**Development:**
- Jupyter Notebook
- VS Code with Python extension
- Git for version control

**Testing:**
- pytest: https://pytest.org/
- Postman: For API testing

**Monitoring:**
- PostgreSQL for logs
- Custom dashboard (optional)

---

## 12. Project Contacts & Roles

**Project Owner:** Zoltán (Senior Developer, ICC Komárno)  
**Customer:** Mágerstav s.r.o. (Pilot customer)  
**Timeline:** 2-4 weeks  
**Budget:** Internal development (no external costs)

**Key Stakeholders:**
- NEX Genesis users (invoice operators)
- IT team (deployment, maintenance)
- Management (ROI tracking)

---

## Appendix A: Configuration Files

**requirements_ml.txt:**
```
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
matplotlib==3.8.2
seaborn==0.13.0
jupyter==1.0.0
pytesseract==0.3.10
pdf2image==1.16.3
Pillow==10.1.0
joblib==1.3.2
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
aiofiles==23.2.1
pytest==7.4.3
requests==2.31.0
```

**Directory structure:**
```
nex-automat/
├── ml_service/
│   ├── __init__.py
│   ├── api.py
│   ├── classifier.py
│   ├── preprocessing.py
│   ├── config.py
│   └── run_service.py
├── ml_models/
│   ├── supplier_classifier.pkl
│   ├── vectorizer.pkl
│   └── model_metadata.json
├── training/
│   ├── notebooks/
│   │   └── supplier_classifier_training.ipynb
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   ├── metadata.csv
│   │   └── ocr_results.csv
│   └── scripts/
│       ├── export_data.py
│       ├── ocr_batch.py
│       └── train_model.py
├── tests/
│   ├── test_classifier.py
│   ├── test_api.py
│   └── sample_invoices/
├── logs/
│   └── ai_service.log
├── docs/
│   └── projects/
│       └── SUPPLIER_CLASSIFIER_BLUEPRINT.md
├── requirements_ml.txt
└── README.md
```

---

## Appendix B: SQL Queries

**Export suppliers:**
```sql
-- Get top 20 suppliers by invoice count
SELECT 
    supplier_id,
    supplier_name,
    COUNT(*) as invoice_count,
    MIN(date) as first_invoice,
    MAX(date) as last_invoice
FROM invoices
WHERE date >= '2023-01-01'
GROUP BY supplier_id, supplier_name
HAVING COUNT(*) >= 50
ORDER BY invoice_count DESC
LIMIT 20;
```

**Daily metrics:**
```sql
-- Track daily performance
SELECT 
    DATE(created_at) as date,
    COUNT(*) as predictions,
    ROUND(AVG(confidence), 3) as avg_confidence,
    ROUND(AVG(processing_time_ms), 0) as avg_time_ms,
    COUNT(*) FILTER (WHERE confidence >= 0.85) as high_confidence,
    COUNT(*) FILTER (WHERE confidence < 0.85) as needs_review
FROM ml_training_data.supplier_predictions
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 30;
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-04 | Zoltán | Initial blueprint created |

---

**END OF DOCUMENT**

---

## QUICK START SUMMARY

**To začať implementáciu:**

1. **Load this document** in new chat
2. **Week 1:** Setup environment + export data
3. **Week 2:** Train model in Jupyter notebook
4. **Week 3:** Create FastAPI service
5. **Week 4:** Integrate with n8n + deploy

**Expected results:**
- 95%+ accuracy
- 90%+ automation
- 2-4 weeks timeline
- Immediate ROI visible

**First command to run:**
```bash
python -m venv venv_ml
source venv_ml/bin/activate
pip install scikit-learn pandas jupyter pytesseract
```

**Ready to start!** 🚀