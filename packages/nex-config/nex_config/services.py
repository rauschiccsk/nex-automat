"""URL adresy externých služieb a API portov."""
import os

# API URLs
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
INVOICE_PIPELINE_URL = os.getenv("INVOICE_PIPELINE_URL", f"{FASTAPI_URL}/api/v1/invoice")
NEX_MANAGER_API_PORT = int(os.getenv("NEX_MANAGER_PORT", "9110"))
NEX_BRAIN_API_URL = os.getenv("NEX_BRAIN_API_URL", "http://localhost:8001")
NEX_BRAIN_API_PORT = int(os.getenv("NEX_BRAIN_API_PORT", "8000"))

# Qdrant + Ollama
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Temporal
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost")
TEMPORAL_PORT = int(os.getenv("TEMPORAL_PORT", "7233"))

# MARSO SOAP API
MARSO_WSDL_URL_PROD = os.getenv(
    "MARSO_WSDL_PROD",
    "http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl",
)
MARSO_WSDL_URL_TEST = os.getenv(
    "MARSO_WSDL_TEST",
    "http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl",
)
