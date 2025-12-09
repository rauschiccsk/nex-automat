# Simple GSCAT record size check

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from packages.nexdata.nexdata.btrieve.btrieve_client import BtrieveClient

print("=" * 70)
print("SIMPLE GSCAT RECORD CHECK")
print("=" * 70)

client = BtrieveClient()
print("Client initialized")

result = client.open_file('gscat')
print(f"open_file result type: {type(result)}")

if isinstance(result, tuple):
    status, position_block = result
    print(f"Open status: {status}")
    print(f"Position block length: {len(position_block)}")
else:
    position_block = result
    print(f"Position block length: {len(position_block)}")

print("GSCAT opened")

result = client.get_first(position_block)
print(f"get_first result type: {type(result)}")
print(f"get_first result: {result}")

if isinstance(result, tuple):
    status, record_bytes = result
    print(f"Status: {status}")
    print(f"Record bytes length: {len(record_bytes)}")
    print(f"First 100 bytes: {record_bytes[:100]}")
else:
    print(f"Result is not tuple, it's: {type(result)}")

client.close_file(position_block)
print("Done")