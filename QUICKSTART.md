# OptimusDB python3 Client - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
pip install requests PyYAML colorlog
```

### Step 2: Test Connection

```bash
# Check if OptimusDB server is running
python3 optimusdb_client.py health

# If successful, you'll see:
# ✓ Server is healthy
```

### Step 3: Basic Operations

```bash
# Get all documents
python3 optimusdb_client.py get

# Upload a TOSCA file
python3 optimusdb_client.py upload app_requirements.yaml
  or
python3 optimusdb_client.py upload capacity_profile.yaml
  or
python3 optimusdb_client.py upload opentofu_hybrid.yaml
  or
python3 optimusdb_client.py upload webapp_adt.yaml
  or
python3 optimusdb_client.py upload deployment_plan.yaml


# Check status
python3 optimusdb_client.py status
```

## Common Tasks

### Upload TOSCA Files

```bash
# Single file
python3 optimusdb_client.py upload webapp_adt.yaml

# Multiple files from directory
python3 batch_operations.py bulk-upload /path/to/tosca/files/
```

### Query Documents

```bash
# All documents
python3 optimusdb_client.py get

# By ID pattern
python3 optimusdb_client.py get --criteria '_id:tosca_.*:regex'

# By type
python3 optimusdb_client.py get --criteria 'document_type:application_description'

# By nested field
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'
```

### Delete Documents

```bash
# Delete by ID
python3 optimusdb_client.py delete --criteria '_id:12345'

# Delete by pattern
python3 optimusdb_client.py delete --criteria '_id:test_.*:regex'

# Delete all (CAREFUL!)
python3 optimusdb_client.py delete-all
```

### Batch Operations

```bash
# Export all documents
python3 batch_operations.py export backup.json

# Import documents
python3 batch_operations.py import backup.json

# Cleanup test data
python3 batch_operations.py cleanup '^test_'
```

## python3 Script Usage

### Basic Example

```python3
from optimusdb_client import OptimusDBClient

# Initialize
client = OptimusDBClient()

# Upload TOSCA
client.upload_tosca("webapp_adt.yaml")

# Query
result = client.get()
print(f"Total documents: {len(result['data'])}")
```

### Full Workflow Example

```python3
from optimusdb_client import OptimusDBClient

client = OptimusDBClient(log_level="INFO")

# 1. Check health
if not client.health_check():
    exit(1)

# 2. Upload TOSCA
client.upload_tosca("webapp_adt.yaml")

# 3. Verify
result = client.get(criteria=[{"_id": {"$regex": ".*webapp.*"}}])
client.print_documents(result['data'])

# 4. Query with filters
result = client.get(criteria=[{"tosca_version": "tosca_simple_yaml_1_3"}])
print(f"Found {len(result['data'])} TOSCA templates")
```

## Troubleshooting

### Connection Error

```bash
# Check server URL
python3 optimusdb_client.py health

```

### Enable Debug Logging

```bash
python3 optimusdb_client.py get --log-level DEBUG
```

### Check Current Documents

```bash
# Quick count
python3 optimusdb_client.py get | grep -c "_id"

# Full list
python3 optimusdb_client.py get
```

## Next Steps

1. Read full documentation: [README.md](README.md)
2. Run examples: `python3 example_usage.py`
3. Try batch operations: `python3 batch_operations.py --help`
4. Explore the python3 API in your own scripts

## Command Reference Card

| Task | Command |
|------|---------|
| Get all | `python3 optimusdb_client.py get` |
| Upload TOSCA | `python3 optimusdb_client.py upload file.yaml` |
| Delete by pattern | `python3 optimusdb_client.py delete --criteria '_id:pattern:regex'` |
| Export backup | `python3 batch_operations.py export backup.json` |
| Import backup | `python3 batch_operations.py import backup.json` |
| Health check | `python3 optimusdb_client.py health` |
| Agent status | `python3 optimusdb_client.py status` |
| Get peers | `python3 optimusdb_client.py peers` |

---

**Swarmchestrate Project** Part of `OptimusDB`