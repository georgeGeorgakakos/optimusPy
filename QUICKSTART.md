# OptimusDB Python Client - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
pip install requests PyYAML colorlog
```

### Step 2: Test Connection

```bash
# Check if OptimusDB server is running
python optimusdb_client.py health

# If successful, you'll see:
# ✓ Server is healthy
```

### Step 3: Basic Operations

```bash
# Get all documents
python optimusdb_client.py get

# Upload a TOSCA file
python optimusdb_client.py upload app_requirements.yaml
  or
python optimusdb_client.py upload capacity_profile.yaml
  or
python optimusdb_client.py upload opentofu_hybrid.yaml
  or
python optimusdb_client.py upload webapp_adt.yaml
  or
python optimusdb_client.py upload deployment_plan.yaml


# Check status
python optimusdb_client.py status
```

## Common Tasks

### Upload TOSCA Files

```bash
# Single file
python optimusdb_client.py upload webapp_adt.yaml

# Multiple files from directory
python batch_operations.py bulk-upload /path/to/tosca/files/
```

### Query Documents

```bash
# All documents
python optimusdb_client.py get

# By ID pattern
python optimusdb_client.py get --criteria '_id:tosca_.*:regex'

# By type
python optimusdb_client.py get --criteria 'document_type:application_description'

# By nested field
python optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'
```

### Delete Documents

```bash
# Delete by ID
python optimusdb_client.py delete --criteria '_id:12345'

# Delete by pattern
python optimusdb_client.py delete --criteria '_id:test_.*:regex'

# Delete all (CAREFUL!)
python optimusdb_client.py delete-all
```

### Batch Operations

```bash
# Export all documents
python batch_operations.py export backup.json

# Import documents
python batch_operations.py import backup.json

# Cleanup test data
python batch_operations.py cleanup '^test_'
```

## Python Script Usage

### Basic Example

```python
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

```python
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
python optimusdb_client.py health

```

### Enable Debug Logging

```bash
python optimusdb_client.py get --log-level DEBUG
```

### Check Current Documents

```bash
# Quick count
python optimusdb_client.py get | grep -c "_id"

# Full list
python optimusdb_client.py get
```

## Next Steps

1. Read full documentation: [README.md](README.md)
2. Run examples: `python example_usage.py`
3. Try batch operations: `python batch_operations.py --help`
4. Explore the Python API in your own scripts

## Command Reference Card

| Task | Command |
|------|---------|
| Get all | `python optimusdb_client.py get` |
| Upload TOSCA | `python optimusdb_client.py upload file.yaml` |
| Delete by pattern | `python optimusdb_client.py delete --criteria '_id:pattern:regex'` |
| Export backup | `python batch_operations.py export backup.json` |
| Import backup | `python batch_operations.py import backup.json` |
| Health check | `python optimusdb_client.py health` |
| Agent status | `python optimusdb_client.py status` |
| Get peers | `python optimusdb_client.py peers` |

---

**Swarmchestrate Project** Part of `OptimusDB`