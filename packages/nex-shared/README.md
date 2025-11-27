# NEX Shared Package

Shared Btrieve models, client and repositories for NEX Genesis ERP integration.

## Contents

- **models/** - Btrieve table models (TSH, TSI, etc.)
- **btrieve/** - Btrieve client wrapper for 32-bit API
- **repositories/** - Repository pattern for data access
- **utils/** - Utility functions

## Installation

```bash
# From nex-automat root
cd packages/nex-shared
pip install -e .
```

## Usage

```python
from nex_shared import BtrieveClient, TSHRecord, TSIRecord

# Open Btrieve file
client = BtrieveClient()
status, pos_block = client.open_file("C:/NEX/YEARACT/STORES/TSHA-001.BTR")

# Read records
status, data = client.get_first(pos_block)
tsh = TSHRecord.from_bytes(data)
print(tsh)

client.close_file(pos_block)
```

## Models

- **TSHRecord** - Dodacie listy Header (hlavičky dokladov)
- **TSIRecord** - Dodacie listy Items (položky dokladov)

## Requirements

- Python 3.9+ (32-bit for Btrieve)
- PyYAML>=6.0.0
- Pervasive PSQL 11.30 (w3btrv7.dll)
