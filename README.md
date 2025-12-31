
# 
# OptimusDB (optimusPy) python Client
#
A comprehensive python3 client for interacting with OptimusDB distributed data catalog system.

## Features

✅ **Full CRUD Operations** - Create, Read, Update, Delete documents  
✅ **TOSCA File Upload** - Upload and process TOSCA YAML templates  
✅ **Advanced Queries** - Regex, operators ($gt, $lt, $in, etc.), nested fields  
✅ **Batch Operations** - Bulk upload, export, import, cleanup  
✅ **Logging & Debug** - Comprehensive logging with adjustable levels  
✅ **CLI Interface** - Easy command-line usage  
✅ **python3 API** - Use as a library in your code

## Installation

### Prerequisites

- python 3.8 or higher
- Access to OptimusDB server

### Setup

1. **Clone or download the client files**

```bash
# Make sure you have these files:
# - optimusdb_client.py
# - requirements.txt
# - example_usage.py
# - batch_operations.py
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests PyYAML colorlog
```

3. **Make scripts executable** (Linux/Mac)

```bash
chmod +x optimusdb_client.py
chmod +x example_usage.py
chmod +x batch_operations.py
```

4. **Verify installation**

```bash
python3 optimusdb_client.py health
```

Expected output:
```
✓ Server is healthy
```

## Quick Start

### CLI Usage

```bash
# Get all documents
python3 optimusdb_client.py get

# Get documents with criteria
python3 optimusdb_client.py get --criteria '_id:tosca_.*:regex'

# Upload TOSCA file
python3 optimusdb_client.py upload webapp_adt.yaml

# Delete documents
python3 optimusdb_client.py delete --criteria 'type:test'

# Check server health
python3 optimusdb_client.py health
```

### python3 API Usage

```python3
from optimusdb_client import OptimusDBClient

# Initialize client
client = OptimusDBClient(
    base_url="http://193.225.250.240",
    context="optimusdb",
    log_level="INFO"
)

# Get all documents
result = client.get()
print(result)

# Upload TOSCA file
result = client.upload_tosca("webapp_adt.yaml")

# Query with regex
result = client.get(criteria=[{"_id": {"$regex": "^tosca_"}}])
```

## CLI Commands

### General Options

```bash
--url URL              OptimusDB base URL (default: http://193.225.250.240)
--context CONTEXT      API context (default: optimusdb)
--log-level LEVEL      Logging level: DEBUG, INFO, WARNING, ERROR
```

### Available Commands

#### 1. GET - Retrieve Documents

```bash
# Get all documents
python3 optimusdb_client.py get

# Get from specific datastore
python3 optimusdb_client.py get --dstype kbmetadata

# Get with simple criteria
python3 optimusdb_client.py get --criteria 'type:renewable_energy'

# Get with regex pattern
python3 optimusdb_client.py get --criteria '_id:tosca_.*:regex'

# Get with numeric filter
python3 optimusdb_client.py get --criteria 'capacity:100:gt'

# Multiple criteria
python3 optimusdb_client.py get --criteria 'type:renewable_energy' 'capacity:100:gt'

# Get nested field
python3 optimusdb_client.py get --criteria 'metadata.status:active'
```

**Criteria Format:**
- `field:value` - Exact match
- `field:value:operator` - With operator (regex, gt, lt, gte, lte, ne, in)

**Supported Operators:**
- `regex` - Regular expression
- `gt` - Greater than
- `gte` - Greater than or equal
- `lt` - Less than
- `lte` - Less than or equal
- `ne` - Not equal
- `in` - Value in list

#### 2. CREATE - Insert Documents

```bash
# Create from JSON string
python3 optimusdb_client.py create --json '[{"name": "Solar Panel", "capacity": 100}]'

# Create from file
python3 optimusdb_client.py create --json documents.json
```

**Example documents.json:**
```json
[
  {
    "name": "Solar Panel Array 1",
    "type": "renewable_energy",
    "capacity": 150,
    "location": "Athens"
  },
  {
    "name": "Wind Turbine 1",
    "type": "renewable_energy",
    "capacity": 200,
    "location": "Thessaloniki"
  }
]
```

#### 3. UPDATE - Modify Documents

```bash
# Update by criteria
python3 optimusdb_client.py update \
  --criteria '_id:12345' \
  --data '{"status": "active", "updated_at": "2025-12-31"}'

# Update from file
python3 optimusdb_client.py update \
  --criteria 'type:test' \
  --data update_data.json
```

#### 4. DELETE - Remove Documents

```bash
# Delete by ID
python3 optimusdb_client.py delete --criteria '_id:12345'

# Delete by type
python3 optimusdb_client.py delete --criteria 'type:test'

# Delete with regex
python3 optimusdb_client.py delete --criteria '_id:temp_.*:regex'

# Delete all matching pattern
python3 optimusdb_client.py delete --criteria 'status:inactive'
```

#### 5. DELETE-ALL - Clear Datastore (⚠️ DANGEROUS)

```bash
# Delete ALL documents (with confirmation)
python3 optimusdb_client.py delete-all

# Delete without confirmation (USE WITH CAUTION!)
python3 optimusdb_client.py delete-all --confirm
```

#### 6. UPLOAD - Upload TOSCA Files

```bash
# Upload single file
python3 optimusdb_client.py upload webapp_adt.yaml

# Upload with different server
python3 optimusdb_client.py upload webapp_adt.yaml --url http://192.168.1.100
```

#### 7. STATUS - Get Agent Status

```bash
python3 optimusdb_client.py status
```

#### 8. PEERS - Get Peer List

```bash
python3 optimusdb_client.py peers
```

#### 9. HEALTH - Health Check

```bash
python3 optimusdb_client.py health
```

## python3 API Reference

### Initialize Client

```python3
from optimusdb_client import OptimusDBClient

client = OptimusDBClient(
    base_url="http://193.225.250.240",  # OptimusDB server URL
    context="swarmkb",                # API context path
    timeout=30,                         # Request timeout in seconds
    log_level="INFO"                    # DEBUG, INFO, WARNING, ERROR
)
```

### CRUD Operations

#### Get Documents

```python3
# Get all documents
result = client.get()

# Get from specific datastore
result = client.get(dstype="kbmetadata")

# Get with criteria
result = client.get(criteria=[{"_id": "12345"}])

# Get with regex
result = client.get(criteria=[{"_id": {"$regex": "^tosca_"}}])

# Get with numeric filter
result = client.get(criteria=[{"capacity": {"$gt": 100}}])

# Get with nested field
result = client.get(criteria=[{"metadata.status": "active"}])

# Get with multiple conditions (AND)
result = client.get(criteria=[{
    "$and": [
        {"type": "renewable_energy"},
        {"capacity": {"$gt": 100}}
    ]
}])

# Get with OR conditions
result = client.get(criteria=[{
    "$or": [
        {"type": "solar"},
        {"type": "wind"}
    ]
}])
```

#### Create Documents

```python3
# Create single document
client.create(documents=[{
    "name": "Solar Panel A",
    "capacity": 100,
    "type": "renewable_energy"
}])

# Create multiple documents
client.create(documents=[
    {"name": "Panel 1", "capacity": 100},
    {"name": "Panel 2", "capacity": 150},
    {"name": "Panel 3", "capacity": 200}
])
```

#### Update Documents

```python3
# Update by criteria
client.update(
    criteria=[{"_id": "12345"}],
    update_data=[{"status": "active", "updated_at": "2025-12-31"}]
)

# Update multiple fields
client.update(
    criteria=[{"type": "test"}],
    update_data=[{
        "status": "completed",
        "test_date": "2025-12-31",
        "verified": True
    }]
)
```

#### Delete Documents

```python3
# Delete by ID
client.delete(criteria=[{"_id": "12345"}])

# Delete by field
client.delete(criteria=[{"type": "test"}])

# Delete with regex
client.delete(criteria=[{"_id": {"$regex": "^temp_"}}])

# Delete all documents (convenience method)
client.delete_all()  # ⚠️ Deletes everything!
```

### TOSCA Operations

```python3
# Upload TOSCA file
result = client.upload_tosca("webapp_adt.yaml")
client.print_result(result)
```

### Advanced Queries

```python3
# Query with strategy options
result = client.query(
    criteria=[{"type": "renewable_energy"}],
    options={
        "strategy": "PARALLEL_MERGE",
        "consistency": "QUORUM",
        "time_budget_ms": 2000,
        "quorum_n": 3,
        "include_local": True
    }
)
```

**Query Strategies:**
- `LOCAL_ONLY` - Query only local node
- `REMOTE_ONLY` - Query only remote peers
- `LOCAL_THEN_REMOTE_MERGE` - Query local first, then merge with remote (default)
- `PARALLEL_MERGE` - Query all peers in parallel
- `QUORUM` - Wait for quorum of responses

### Utility Operations

```python3
# Health check
is_healthy = client.health_check()

# Get agent status
status = client.get_agent_status()

# Get peer list
peers = client.get_peers()
```

### Pretty Printing

```python3
# Print result with formatting
result = client.get()
client.print_result(result, "My Query Results")

# Print documents list
documents = result.get('data', [])
client.print_documents(documents, max_display=10)
```

## Batch Operations

Use the `batch_operations.py` script for bulk tasks.

### Bulk Upload TOSCA Files

```bash
# Upload all YAML files from a directory
python3 batch_operations.py bulk-upload /path/to/tosca/files/
```

### Export to JSON

```bash
# Export all documents
python3 batch_operations.py export backup.json

# Export from specific datastore
python3 batch_operations.py export backup.json --dstype kbmetadata
```

### Import from JSON

```bash
# Import documents
python3 batch_operations.py import backup.json

# Import to specific datastore
python3 batch_operations.py import backup.json --dstype kbmetadata
```

### Cleanup by Pattern

```bash
# Delete documents matching pattern (interactive)
python3 batch_operations.py cleanup '^temp_'

# Cleanup test documents
python3 batch_operations.py cleanup '^test_'
```

## Complete Examples

### Example 1: Complete Workflow

```python3
from optimusdb_client import OptimusDBClient

# Initialize
client = OptimusDBClient(log_level="INFO")

# 1. Health check
if not client.health_check():
    print("Server unavailable")
    exit(1)

# 2. Upload TOSCA file
client.upload_tosca("webapp_adt.yaml")

# 3. Verify upload
result = client.get(criteria=[{"_id": {"$regex": ".*webapp.*"}}])
client.print_documents(result['data'])

# 4. Create some test data
client.create([
    {"name": "Test 1", "type": "test", "value": 100},
    {"name": "Test 2", "type": "test", "value": 200}
])

# 5. Query test data
tests = client.get(criteria=[{"type": "test"}])
print(f"Found {len(tests['data'])} test documents")

# 6. Update test data
client.update(
    criteria=[{"type": "test"}],
    update_data=[{"verified": True}]
)

# 7. Delete test data
client.delete(criteria=[{"type": "test"}])

# 8. Final count
final = client.get()
print(f"Total documents: {len(final['data'])}")
```

### Example 2: Data Migration

```python3
# Export from one server
client_old = OptimusDBClient(base_url="http://old-server:18001")
result = client_old.get()
documents = result['data']

# Import to new server
client_new = OptimusDBClient(base_url="http://new-server:18001")
client_new.create(documents)

print(f"Migrated {len(documents)} documents")
```

### Example 3: Monitoring & Cleanup

```python3
import time

client = OptimusDBClient()

while True:
    # Get document count
    result = client.get()
    count = len(result['data'])
    print(f"Current documents: {count}")
    
    # Clean up old test documents
    client.delete(criteria=[{
        "$and": [
            {"type": "test"},
            {"created_at": {"$lt": "2025-01-01"}}
        ]
    }])
    
    time.sleep(60)  # Check every minute
```

## Troubleshooting

### Connection Refused

```
Error: Connection refused
```

**Solution:** Verify OptimusDB is running and URL is correct:
```bash
python3 optimusdb_client.py health --url http://193.225.250.240
```

### Invalid JSON

```
Error: Failed to parse response JSON
```

**Solution:** Check server logs and verify endpoint exists:
```bash
curl http://193.225.250.240/swarmkb/agent/status
```

### Timeout

```
Error: Request timeout after 30 seconds
```

**Solution:** Increase timeout or check server performance:
```python3
client = OptimusDBClient(timeout=60)
```

### No Documents Found

```
Retrieved 0 document(s)
```

**Solution:** Verify datastore name:
```bash
python3 optimusdb_client.py get --dstype dsswres
```

## Advanced Configuration

### Environment Variables

Create a `.env` file:

```bash
OPTIMUSDB_URL=http://193.225.250.240
OPTIMUSDB_CONTEXT=swarmkb
OPTIMUSDB_TIMEOUT=30
OPTIMUSDB_LOG_LEVEL=INFO
```

### Custom Configuration

```python3
import os
from optimusdb_client import OptimusDBClient

client = OptimusDBClient(
    base_url=os.getenv('OPTIMUSDB_URL', 'http://193.225.250.240'),
    context=os.getenv('OPTIMUSDB_CONTEXT', 'swarmkb'),
    timeout=int(os.getenv('OPTIMUSDB_TIMEOUT', '30')),
    log_level=os.getenv('OPTIMUSDB_LOG_LEVEL', 'INFO')
)
```

## Testing

Run the example script to test all functionality:

```bash
python3 example_usage.py
```

This will:
1. Check server health
2. Get agent status
3. Create sample documents
4. Query with various filters
5. Update documents
6. Delete test documents
7. Upload TOSCA file (if available)

## Query Operator Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `$regex` | Regular expression | `{"_id": {"$regex": "^tosca_"}}` |
| `$gt` | Greater than | `{"capacity": {"$gt": 100}}` |
| `$gte` | Greater than or equal | `{"capacity": {"$gte": 100}}` |
| `$lt` | Less than | `{"capacity": {"$lt": 200}}` |
| `$lte` | Less than or equal | `{"capacity": {"$lte": 200}}` |
| `$ne` | Not equal | `{"status": {"$ne": "inactive"}}` |
| `$in` | Value in array | `{"type": {"$in": ["solar", "wind"]}}` |
| `$exists` | Field exists | `{"metadata": {"$exists": true}}` |
| `$contains` | Array contains value | `{"tags": {"$contains": "renewable"}}` |
| `$all` | Array contains all | `{"tags": {"$all": ["solar", "active"]}}` |
| `$and` | Logical AND | `{"$and": [{...}, {...}]}` |
| `$or` | Logical OR | `{"$or": [{...}, {...}]}` |

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section
2. Enable DEBUG logging: `--log-level DEBUG`
3. Review OptimusDB server logs
4. Check network connectivity

---

**Happy querying with OptimusDB!** 🚀