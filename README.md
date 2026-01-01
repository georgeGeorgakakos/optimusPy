# Swarmchestrate OptimusDB Python Client - Complete Testing Guide

**A comprehensive Python client for testing and interacting with the Swarmchestrate OptimusDB decentralized Knowledge Base System.**

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
    - [Installation](#installation)
    - [Test Connection](#test-connection)
    - [Upload Your TOSCA Files](#upload-your-tosca-files)
    - [Query Your Data](#query-your-data)
- [Your Project Files](#your-project-files)
- [CLI Reference](#cli-reference)
    - [Global Options](#global-options)
    - [Available Commands](#available-commands)
- [Python API Reference](#python-api-reference)
    - [Initialize Client](#initialize-client)
    - [CRUD Operations](#crud-operations)
    - [TOSCA Operations](#tosca-operations)
    - [Utility Operations](#utility-operations)
- [20 Testing Scenarios](#20-testing-scenarios)
    - [Scenario 1: Get All Documents (Baseline)](#scenario-1-get-all-documents-baseline)
    - [Scenario 2: Upload Single TOSCA File](#scenario-2-upload-single-tosca-file)
    - [Scenario 3: Batch Upload All TOSCA Files](#scenario-3-batch-upload-all-tosca-files)
    - [Scenario 4: Query by Document Type](#scenario-4-query-by-document-type)
    - [Scenario 5: Query by Template Name (Regex)](#scenario-5-query-by-template-name-regex)
    - [Scenario 6: Query by Specific ID](#scenario-6-query-by-specific-id)
    - [Scenario 7: Query by Node Type (Nested Fields)](#scenario-7-query-by-node-type-nested-fields)
    - [Scenario 8: Query by Properties (CPU, Memory)](#scenario-8-query-by-properties-cpu-memory)
    - [Scenario 9: Query by Metadata](#scenario-9-query-by-metadata)
    - [Scenario 10: Complex AND Query](#scenario-10-complex-and-query)
    - [Scenario 11: Complex OR Query](#scenario-11-complex-or-query)
    - [Scenario 12: Update Single Document](#scenario-12-update-single-document)
    - [Scenario 13: Bulk Update](#scenario-13-bulk-update)
    - [Scenario 14: Delete Single Document](#scenario-14-delete-single-document)
    - [Scenario 15: Delete by Pattern](#scenario-15-delete-by-pattern)
    - [Scenario 16: Conditional Delete](#scenario-16-conditional-delete)
    - [Scenario 17: Query with Sorting and Limiting](#scenario-17-query-with-sorting-and-limiting)
    - [Scenario 18: Export Documents to JSON](#scenario-18-export-documents-to-json)
    - [Scenario 19: Advanced Analysis](#scenario-19-advanced-analysis)
    - [Scenario 20: Delete All Documents (Clean Slate)](#scenario-20-delete-all-documents-clean-slate)
- [Batch Operations](#batch-operations)
- [Query Operators Reference](#query-operators-reference)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [License](#license)

---

## Overview

The **Swarmchestrate OptimusDB Python Client** is a comprehensive testing and interaction tool for the OptimusDB distributed data catalog system. It enables full CRUD operations, TOSCA template management, and advanced querying capabilities for testing Swarmchestrate's knowledge base infrastructure.

**What This Guide Covers:**
- Complete CLI and Python API reference
- 20 practical testing scenarios with real commands
- Batch operations for bulk testing
- Your actual TOSCA files from `toscaSamples/`
- Query patterns for content-based search
- Update and delete operations
- Export and analysis capabilities

---

## Features

✅ **Full CRUD Operations** - Create, Read, Update, Delete documents  
✅ **TOSCA File Upload** - Upload and process TOSCA YAML templates with full structure mode  
✅ **Advanced Queries** - Regex, operators ($gt, $lt, $in, etc.), nested field queries  
✅ **Batch Operations** - Bulk upload, export, import, cleanup  
✅ **Content-Based Search** - Search inside TOSCA nodes, properties, metadata  
✅ **Logging & Debug** - Comprehensive logging with adjustable levels  
✅ **CLI Interface** - Easy command-line usage for quick testing  
✅ **Python API** - Use as a library in your automation scripts  
✅ **Full Structure Mode** - Creates queryable documents (not binary blobs)

---

## Quick Start

### Installation

**Prerequisites:**
- Python 3.8 or higher
- Access to Swarmchestrate OptimusDB server (default: http://193.225.250.240)

**Install Dependencies:**

```bash
pip3 install requests PyYAML colorlog
```

Or use the requirements file:

```bash
pip3 install -r requirements.txt
```

**Make Scripts Executable** (Linux/Mac):

```bash
chmod +x optimusdb_client.py
chmod +x batch_operations.py
```

---

### Test Connection

```bash
python3 optimusdb_client.py health
```

**Expected Output:**
```
Server: http://193.225.250.240
Context: swarmkb
Status: healthy ✓
```

---

### Upload Your TOSCA Files

Upload all 5 TOSCA files from your `toscaSamples/` directory:

```bash
python3 batch_operations.py bulk-upload toscaSamples/
```

**Expected Output:**
```
Starting bulk upload from: toscaSamples/

✓ webapp_adt.yaml → tosca_webapp_microservicesapplication_v1_0_0
✓ app_requirements.yaml → tosca_app_requirements_v1_0_0
✓ capacity_profile.yaml → tosca_capacity_profile_v1_0_0
✓ deployment_plan.yaml → tosca_deployment_plan_v1_0_0
✓ opentofu_hybrid.yaml → tosca_opentofu_hybrid_v1_0_0

================================================================================
UPLOAD SUMMARY
================================================================================
Total files: 5
Successful: 5
Failed: 0
Documents created: 15-25 (3-5 per file in full structure mode)
================================================================================
```

---

### Query Your Data

See what was uploaded:

```bash
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'
```

**Expected Output:**
```
Retrieved 5 document(s)

Document IDs:
  1. tosca_webapp_microservicesapplication_v1_0_0
  2. tosca_app_requirements_v1_0_0
  3. tosca_capacity_profile_v1_0_0
  4. tosca_deployment_plan_v1_0_0
  5. tosca_opentofu_hybrid_v1_0_0
```

**✅ You're now ready to test all scenarios!**

---

## Your Project Files

```
📂 Swarmchestrate Testing Project
├── optimusdb_client.py          ← Main Python client
├── batch_operations.py           ← Bulk operations tool
├── requirements.txt              ← Dependencies
└── toscaSamples/                 ← Your TOSCA templates
    ├── webapp_adt.yaml           (6.0 KB) - Web application with microservices
    ├── app_requirements.yaml     (11 KB)  - Application requirements
    ├── capacity_profile.yaml     (6.9 KB) - Capacity planning profile
    ├── deployment_plan.yaml      (14 KB)  - Deployment orchestration plan
    └── opentofu_hybrid.yaml      (11 KB)  - OpenTofu hybrid infrastructure
```

**What Each TOSCA File Contains:**
- **webapp_adt.yaml**: E-commerce web application with frontend, API gateway, PostgreSQL, and Redis
- **app_requirements.yaml**: Application requirements and constraints
- **capacity_profile.yaml**: Resource capacity profiles and scaling policies
- **deployment_plan.yaml**: Complete deployment orchestration plans
- **opentofu_hybrid.yaml**: Hybrid cloud infrastructure with OpenTofu

---

## CLI Reference

### Global Options

These options apply to all commands and must come **before** the command:

```bash
python3 optimusdb_client.py [OPTIONS] COMMAND [COMMAND_OPTIONS]
```

**Available Global Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--url URL` | OptimusDB base URL | `http://193.225.250.240` |
| `--context CONTEXT` | API context path | `swarmkb` |
| `--log-level LEVEL` | Logging level | `INFO` |

**Log Levels:** `DEBUG`, `INFO`, `WARNING`, `ERROR`

**Example:**
```bash
python3 optimusdb_client.py --log-level DEBUG get --criteria 'type:test'
```

---

### Available Commands

#### 1. `get` - Retrieve Documents

**Syntax:**
```bash
python3 optimusdb_client.py get [--dstype DATASTORE] [--criteria CRITERIA...]
```

**Examples:**

```bash
# Get all documents
python3 optimusdb_client.py get

# Get from specific datastore
python3 optimusdb_client.py get --dstype kbmetadata

# Simple exact match
python3 optimusdb_client.py get --criteria 'type:renewable_energy'

# Regex pattern
python3 optimusdb_client.py get --criteria '_id:tosca_.*:regex'

# Numeric comparison
python3 optimusdb_client.py get --criteria 'capacity:100:gt'

# Nested field
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'

# Multiple criteria (implicit AND)
python3 optimusdb_client.py get --criteria 'type:test' 'status:active'
```

**Criteria Format:**
```
field:value              → Exact match
field:value:operator     → With operator
```

**Supported Operators:**
- `regex` - Regular expression match
- `gt` / `gte` - Greater than / Greater than or equal
- `lt` / `lte` - Less than / Less than or equal
- `ne` - Not equal
- `in` - Value in list

---

#### 2. `create` - Insert Documents

**Syntax:**
```bash
python3 optimusdb_client.py create --json JSON_DATA [--dstype DATASTORE]
```

**Examples:**

```bash
# Create from JSON string
python3 optimusdb_client.py create --json '[{"name":"Test","capacity":100}]'

# Create from file
python3 optimusdb_client.py create --json documents.json
```

**Example JSON file:**
```json
[
  {
    "name": "Solar Panel Array",
    "type": "renewable_energy",
    "capacity": 150,
    "location": "Athens"
  },
  {
    "name": "Wind Turbine",
    "type": "renewable_energy",
    "capacity": 200,
    "location": "Thessaloniki"
  }
]
```

---

#### 3. `update` - Modify Documents

**Syntax:**
```bash
python3 optimusdb_client.py update --criteria CRITERIA --data UPDATE_DATA
```

**Examples:**

```bash
# Update single field
python3 optimusdb_client.py update \
  --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0' \
  --data '{"status":"active"}'

# Update multiple fields
python3 optimusdb_client.py update \
  --criteria 'type:test' \
  --data '{"status":"completed","verified":true,"date":"2026-01-01"}'
```

---

#### 4. `delete` - Remove Documents

**Syntax:**
```bash
python3 optimusdb_client.py delete --criteria CRITERIA
```

**Examples:**

```bash
# Delete by exact ID
python3 optimusdb_client.py delete --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0'

# Delete by type
python3 optimusdb_client.py delete --criteria 'type:test'

# Delete by regex pattern
python3 optimusdb_client.py delete --criteria '_id:temp_.*:regex'

# Delete by condition
python3 optimusdb_client.py delete --criteria 'status:inactive'
```

---

#### 5. `delete-all` - Clear All Documents

**⚠️ WARNING: This deletes ALL documents!**

```bash
# Interactive (asks for confirmation)
python3 optimusdb_client.py delete-all

# Skip confirmation (dangerous!)
python3 optimusdb_client.py delete-all --confirm
```

---

#### 6. `upload` - Upload TOSCA Files

**Syntax:**
```bash
python3 optimusdb_client.py upload FILE_PATH
```

**Examples:**

```bash
# Upload single file
python3 optimusdb_client.py upload toscaSamples/webapp_adt.yaml

# Upload with debug logging
python3 optimusdb_client.py --log-level DEBUG upload toscaSamples/webapp_adt.yaml
```

**What Happens:**
- File is uploaded in **full structure mode** (queryable)
- Creates 3-5 structured documents per file
- Returns template ID for queries
- All content becomes searchable

---

#### 7. `status` - Get Agent Status

```bash
python3 optimusdb_client.py status
```

**Shows:** Peer count, database info, cluster health

---

#### 8. `peers` - List Cluster Peers

```bash
python3 optimusdb_client.py peers
```

**Shows:** Connected peers in the OptimusDB cluster

---

#### 9. `health` - Health Check

```bash
python3 optimusdb_client.py health
```

**Returns:** Server health status (pass/fail)

---

## Python API Reference

### Initialize Client

```python
from optimusdb_client import OptimusDBClient

# Use defaults (production server)
client = OptimusDBClient()

# Custom configuration
client = OptimusDBClient(
    base_url="http://193.225.250.240",
    context="swarmkb",
    timeout=30,
    log_level="INFO"  # DEBUG, INFO, WARNING, ERROR
)
```

---

### CRUD Operations

#### Get Documents

```python
# Get all documents
result = client.get()
print(f"Total: {len(result['data'])} documents")

# Get with simple criteria
result = client.get(criteria=[{"type": "renewable_energy"}])

# Get with regex
result = client.get(criteria=[{"_id": {"$regex": "^tosca_"}}])

# Get with comparison
result = client.get(criteria=[{"capacity": {"$gt": 100}}])

# Get nested field
result = client.get(criteria=[{"metadata.kb_datastore": "ADT"}])

# Complex AND query
result = client.get(criteria=[{
    "$and": [
        {"type": "renewable_energy"},
        {"capacity": {"$gte": 100}},
        {"location": "Athens"}
    ]
}])

# Complex OR query
result = client.get(criteria=[{
    "$or": [
        {"type": "solar"},
        {"type": "wind"}
    ]
}])

# Specific datastore
result = client.get(dstype="kbmetadata")
```

#### Create Documents

```python
# Single document
client.create(documents=[{
    "name": "Solar Panel A",
    "capacity": 100,
    "type": "renewable_energy"
}])

# Multiple documents
client.create(documents=[
    {"name": "Panel 1", "capacity": 100},
    {"name": "Panel 2", "capacity": 150},
    {"name": "Panel 3", "capacity": 200}
])
```

#### Update Documents

```python
# Update by ID
client.update(
    criteria=[{"_id": "tosca_webapp_microservicesapplication_v1_0_0"}],
    update_data=[{"status": "active", "updated_at": "2026-01-01"}]
)

# Bulk update
client.update(
    criteria=[{"type": "test"}],
    update_data=[{"verified": True, "verification_date": "2026-01-01"}]
)
```

#### Delete Documents

```python
# Delete by ID
client.delete(criteria=[{"_id": "12345"}])

# Delete by pattern
client.delete(criteria=[{"_id": {"$regex": "^temp_"}}])

# Delete all (dangerous!)
client.delete_all()
```

---

### TOSCA Operations

```python
# Upload TOSCA file (full structure mode - queryable)
result = client.upload_tosca("toscaSamples/webapp_adt.yaml")
template_id = result.get('template_id')
print(f"Uploaded: {template_id}")

# Upload creates 3-5 queryable documents:
# 1. Main template (tosca_template)
# 2. Flattened template (flattened_template)
# 3. Application description (application_description)
# 4-5. Additional metadata/topology documents
```

---

### Utility Operations

```python
# Health check
is_healthy = client.health_check()
if not is_healthy:
    print("Server unavailable")

# Get agent status
status = client.get_agent_status()
print(f"Peers: {status.get('peer_count')}")

# Get peer list
peers = client.get_peers()
print(f"Connected peers: {len(peers)}")

# Pretty print results
result = client.get()
client.print_result(result, "Query Results")
```

---

## 20 Testing Scenarios

### Scenario 1: Get All Documents (Baseline)

**Purpose:** Establish baseline document count before testing

**Command:**
```bash
python3 optimusdb_client.py get
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()
result = client.get()
print(f"Total documents: {len(result['data'])}")
```

**Expected Output:**
```
Retrieved X document(s)
Total: X documents
```

**Use Case:** Check initial state before uploading test data

---

### Scenario 2: Upload Single TOSCA File

**Purpose:** Test single file upload with full structure mode

**Command:**
```bash
python3 optimusdb_client.py upload toscaSamples/webapp_adt.yaml
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()
result = client.upload_tosca("toscaSamples/webapp_adt.yaml")
template_id = result.get('template_id')
print(f"✓ Uploaded: {template_id}")
```

**Expected Output:**
```
Uploading TOSCA file: toscaSamples/webapp_adt.yaml
File size: 5849 bytes

Response: {
  "data": {
    "filename": "webapp_adt.yaml",
    "message": "TOSCA uploaded with full structure",
    "queryable": true,
    "storage_location": "dsswres",
    "template_id": "tosca_webapp_microservicesapplication_v1_0_0"
  },
  "status": 200
}

✓ Template ID: tosca_webapp_microservicesapplication_v1_0_0
✓ Queryable: true (full structure mode)
✓ Created 3-5 documents
```

**Verification:**
```bash
# Check document count increased by 3-5
python3 optimusdb_client.py get | grep -c '"_id"'
```

---

### Scenario 3: Batch Upload All TOSCA Files

**Purpose:** Test bulk upload of all 5 TOSCA files

**Command:**
```bash
python3 batch_operations.py bulk-upload toscaSamples/
```

**Python:**
```python
from optimusdb_client import OptimusDBClient
import os

client = OptimusDBClient()
tosca_dir = "toscaSamples/"

for filename in os.listdir(tosca_dir):
    if filename.endswith('.yaml'):
        filepath = os.path.join(tosca_dir, filename)
        result = client.upload_tosca(filepath)
        print(f"✓ {filename} → {result['template_id']}")
```

**Expected Output:**
```
✓ webapp_adt.yaml → tosca_webapp_microservicesapplication_v1_0_0
✓ app_requirements.yaml → tosca_app_requirements_v1_0_0
✓ capacity_profile.yaml → tosca_capacity_profile_v1_0_0
✓ deployment_plan.yaml → tosca_deployment_plan_v1_0_0
✓ opentofu_hybrid.yaml → tosca_opentofu_hybrid_v1_0_0

Total: 5 files
Documents created: 15-25
```

**Verification:**
```bash
# Verify all templates uploaded
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'
# Should show 5 templates
```

---

### Scenario 4: Query by Document Type

**Purpose:** Filter documents by type (templates, flattened, etc.)

**Command:**
```bash
# Get main TOSCA templates
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'

# Get flattened templates
python3 optimusdb_client.py get --criteria 'document_type:flattened_template'

# Get application descriptions
python3 optimusdb_client.py get --criteria 'document_type:application_description'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Count by document type
templates = client.get(criteria=[{"document_type": "tosca_template"}])
flattened = client.get(criteria=[{"document_type": "flattened_template"}])
apps = client.get(criteria=[{"document_type": "application_description"}])

print(f"TOSCA templates: {len(templates['data'])}")
print(f"Flattened templates: {len(flattened['data'])}")
print(f"Application descriptions: {len(apps['data'])}")
```

**Expected Output:**
```
Retrieved 5 document(s)

  1. tosca_webapp_microservicesapplication_v1_0_0
  2. tosca_app_requirements_v1_0_0
  3. tosca_capacity_profile_v1_0_0
  4. tosca_deployment_plan_v1_0_0
  5. tosca_opentofu_hybrid_v1_0_0
```

---

### Scenario 5: Query by Template Name (Regex)

**Purpose:** Search templates by name pattern

**Command:**
```bash
# Find templates with "WebApp" in name
python3 optimusdb_client.py get --criteria 'template_name:.*WebApp.*:regex'

# Find templates starting with "App"
python3 optimusdb_client.py get --criteria 'template_name:^App.*:regex'

# Case-insensitive search
python3 optimusdb_client.py get --criteria 'template_name:.*deployment.*:regex'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Find webapp templates
result = client.get(criteria=[{"template_name": {"$regex": ".*WebApp.*"}}])

print(f"Found {len(result['data'])} templates with 'WebApp'")
for doc in result['data']:
    print(f"  - {doc['template_name']}")
```

**Expected Output:**
```
Retrieved 1 document(s)

  1. tosca_webapp_microservicesapplication_v1_0_0
     template_name: "WebApp-MicroservicesApplication"
```

---

### Scenario 6: Query by Specific ID

**Purpose:** Retrieve a specific template by exact ID

**Command:**
```bash
python3 optimusdb_client.py get --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

doc_id = "tosca_webapp_microservicesapplication_v1_0_0"
result = client.get(criteria=[{"_id": doc_id}])

if result['data']:
    doc = result['data'][0]
    print(f"Template: {doc.get('template_name')}")
    print(f"Version: {doc.get('template_version')}")
    print(f"Nodes: {len(doc.get('node_templates', {}))}")
```

**Expected Output:**
```
Retrieved 1 document(s)

{
  "_id": "tosca_webapp_microservicesapplication_v1_0_0",
  "template_name": "WebApp-MicroservicesApplication",
  "template_version": "1.0.0",
  "node_templates": {...},
  ...
}
```

---

### Scenario 7: Query by Node Type (Nested Fields)

**Purpose:** Search for templates containing specific node types

**Command:**
```bash
# Find templates with Docker containers
python3 optimusdb_client.py get --criteria 'node_templates.*.type:.*Docker.*:regex'

# Find templates with PostgreSQL
python3 optimusdb_client.py get --criteria 'node_templates.*.type:.*PostgreSQL.*:regex'

# Find templates with Redis
python3 optimusdb_client.py get --criteria 'node_templates.*.type:.*Redis.*:regex'

# Find any database
python3 optimusdb_client.py get --criteria 'node_templates.*.type:.*Database.*:regex'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Find Docker containers
result = client.get(criteria=[{
    "node_templates.*.type": {"$regex": ".*Docker.*"}
}])

print(f"Templates with Docker: {len(result['data'])}")

for doc in result['data']:
    nodes = doc.get('node_templates', {})
    docker_nodes = [
        name for name, node in nodes.items()
        if 'Docker' in node.get('type', '')
    ]
    print(f"  {doc['template_name']}: {docker_nodes}")
```

**Expected Output:**
```
Templates with Docker: 1

  WebApp-MicroservicesApplication: ['web_frontend', 'api_gateway', 
    'frontend_container_runtime', 'backend_container_runtime', 
    'database_container_runtime', 'cache_container_runtime']
```

---

### Scenario 8: Query by Properties (CPU, Memory)

**Purpose:** Find nodes with specific resource requirements

**Command:**
```bash
# Find nodes with 4 CPUs
python3 optimusdb_client.py get --criteria 'node_templates.*.properties.num_cpus:4'

# Find nodes with >= 8 CPUs
python3 optimusdb_client.py get --criteria 'node_templates.*.properties.num_cpus:8:gte'

# Find nodes with >= 16GB memory
python3 optimusdb_client.py get --criteria 'node_templates.*.properties.mem_size:.*16.*GB.*:regex'

# Find nodes with disk >= 100GB
python3 optimusdb_client.py get --criteria 'node_templates.*.properties.disk_size:.*100.*GB.*:regex'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Find high-CPU nodes (>= 4)
result = client.get(criteria=[{
    "node_templates.*.properties.num_cpus": {"$gte": 4}
}])

print(f"Templates with high-CPU nodes: {len(result['data'])}")

for doc in result['data']:
    print(f"\n{doc['template_name']}:")
    nodes = doc.get('node_templates', {})
    for name, node in nodes.items():
        cpus = node.get('properties', {}).get('num_cpus')
        if cpus and cpus >= 4:
            print(f"  - {name}: {cpus} CPUs")
```

**Expected Output:**
```
Templates with high-CPU nodes: 1

WebApp-MicroservicesApplication:
  - backend_container_runtime: 4 CPUs
  - database_container_runtime: 4 CPUs
```

---

### Scenario 9: Query by Metadata

**Purpose:** Filter by template metadata (author, datastore, version)

**Command:**
```bash
# Find templates in ADT datastore
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'

# Find by author
python3 optimusdb_client.py get --criteria 'metadata.template_author:Swarmchestrate.*:regex'

# Find by version
python3 optimusdb_client.py get --criteria 'metadata.template_version:1.0.0'

# Find by TOSCA version
python3 optimusdb_client.py get --criteria 'tosca_version:tosca_simple_yaml_1_3'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Find by datastore
result = client.get(criteria=[{
    "metadata.kb_datastore": "ADT"
}])

print(f"Templates in ADT: {len(result['data'])}")
for doc in result['data']:
    print(f"  - {doc['template_name']}")
    print(f"    Author: {doc.get('metadata', {}).get('template_author')}")
    print(f"    Version: {doc.get('metadata', {}).get('template_version')}")
```

**Expected Output:**
```
Templates in ADT: 1

  - WebApp-MicroservicesApplication
    Author: Swarmchestrate Orchestrator
    Version: 1.0.0
```

---

### Scenario 10: Complex AND Query

**Purpose:** Combine multiple conditions with AND logic

**Command:**
```bash
# Find Docker containers in ADT with >= 4 CPUs
python3 optimusdb_client.py get --criteria '$and:[{"node_templates.*.type":".*Docker.*:regex"},{"metadata.kb_datastore":"ADT"},{"node_templates.*.properties.num_cpus":"4:gte"}]'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Complex AND query
result = client.get(criteria=[{
    "$and": [
        {"node_templates.*.type": {"$regex": ".*Docker.*"}},
        {"metadata.kb_datastore": "ADT"},
        {"node_templates.*.properties.num_cpus": {"$gte": 4}}
    ]
}])

print(f"Matching templates: {len(result['data'])}")
for doc in result['data']:
    print(f"  ✓ {doc['template_name']}")
    print(f"    - Has Docker containers")
    print(f"    - In ADT datastore")
    print(f"    - Has nodes with >= 4 CPUs")
```

**Expected Output:**
```
Matching templates: 1

  ✓ WebApp-MicroservicesApplication
    - Has Docker containers
    - In ADT datastore
    - Has nodes with >= 4 CPUs
```

---

### Scenario 11: Complex OR Query

**Purpose:** Find templates matching any of multiple conditions

**Command:**
```bash
# Find templates with PostgreSQL OR Redis
python3 optimusdb_client.py get --criteria '$or:[{"node_templates.*.type":".*PostgreSQL.*:regex"},{"node_templates.*.type":".*Redis.*:regex"}]'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# OR query
result = client.get(criteria=[{
    "$or": [
        {"node_templates.*.type": {"$regex": ".*PostgreSQL.*"}},
        {"node_templates.*.type": {"$regex": ".*Redis.*"}}
    ]
}])

print(f"Templates with PostgreSQL or Redis: {len(result['data'])}")
for doc in result['data']:
    nodes = doc.get('node_templates', {})
    db_nodes = [
        name for name, node in nodes.items()
        if 'PostgreSQL' in node.get('type', '') or 'Redis' in node.get('type', '')
    ]
    print(f"  {doc['template_name']}: {db_nodes}")
```

**Expected Output:**
```
Templates with PostgreSQL or Redis: 1

  WebApp-MicroservicesApplication: ['postgres_db', 'redis_cache']
```

---

### Scenario 12: Update Single Document

**Purpose:** Add or modify fields in a specific document

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Update deployment status
result = client.update(
    criteria=[{'_id': 'tosca_webapp_microservicesapplication_v1_0_0'}],
    update_data=[{
        'deployment_status': 'active',
        'deployed_at': '2026-01-01T16:00:00Z',
        'deployed_by': 'automation'
    }]
)

print(f"Modified: {result['data']['modified_count']} documents")
```

**Expected Output:**
```
Modified: 1 documents
```

**Verification:**
```bash
# Check the updated document
python3 optimusdb_client.py get --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0'

# Should now show:
# "deployment_status": "active"
# "deployed_at": "2026-01-01T16:00:00Z"
```

---

### Scenario 13: Bulk Update

**Purpose:** Update multiple documents matching criteria

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Update all templates in ADT datastore
result = client.update(
    criteria=[{"metadata.kb_datastore": "ADT"}],
    update_data=[{
        "validated": True,
        "validation_timestamp": "2026-01-01T16:00:00Z",
        "validator": "Swarmchestrate Test Suite"
    }]
)

print(f"Updated {result['data']['modified_count']} templates")
```

**Expected Output:**
```
Updated 1 templates
```

---

### Scenario 14: Delete Single Document

**Purpose:** Remove a specific document by ID

**Command:**
```bash
# Delete specific template
python3 optimusdb_client.py delete --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Delete specific document
result = client.delete(criteria=[{
    "_id": "tosca_webapp_microservicesapplication_v1_0_0"
}])

print(f"Deleted: {result['data']['deleted_count']} documents")
```

**Expected Output:**
```
Deleted: 1 documents
```

**Verification:**
```bash
# Try to get the deleted document
python3 optimusdb_client.py get --criteria '_id:tosca_webapp_microservicesapplication_v1_0_0'

# Expected: Retrieved 0 document(s)
```

---

### Scenario 15: Delete by Pattern

**Purpose:** Delete multiple documents matching a pattern

**Command:**
```bash
# Delete all flattened templates
python3 optimusdb_client.py delete --criteria 'document_type:flattened_template'

# Delete test templates
python3 optimusdb_client.py delete --criteria '_id:test_.*:regex'
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Delete by document type
result = client.delete(criteria=[{
    "document_type": "flattened_template"
}])

print(f"Deleted {result['data']['deleted_count']} flattened templates")
```

**Expected Output:**
```
Deleted 5 flattened templates
```

---

### Scenario 16: Conditional Delete

**Purpose:** Delete only if multiple conditions are met

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Delete old test templates
result = client.delete(criteria=[{
    "$and": [
        {"document_type": "tosca_template"},
        {"metadata.kb_datastore": "TEST"},
        {"metadata.template_version": {"$regex": "^0\\."}}
    ]
}])

print(f"Deleted {result['data']['deleted_count']} old test templates")
```

---

### Scenario 17: Query with Sorting and Limiting

**Purpose:** Get documents in specific order or limited count

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Get all templates, sort by name
result = client.get(criteria=[{"document_type": "tosca_template"}])

# Sort in Python (OptimusDB returns data unsorted)
templates = sorted(
    result['data'],
    key=lambda x: x.get('template_name', '')
)

print("Templates (sorted):")
for doc in templates[:5]:  # Limit to first 5
    print(f"  - {doc.get('template_name')}")

# Count documents
print(f"\nTotal templates: {len(result['data'])}")
```

**Expected Output:**
```
Templates (sorted):
  - App-Requirements
  - Capacity-Profile
  - Deployment-Plan
  - OpenTofu-Hybrid
  - WebApp-MicroservicesApplication

Total templates: 5
```

---

### Scenario 18: Export Documents to JSON

**Purpose:** Export all or filtered documents to a file

**Command:**
```bash
# Export all documents
python3 batch_operations.py export all_templates.json

# Export only TOSCA templates
python3 batch_operations.py export --criteria 'document_type:tosca_template' templates_only.json
```

**Python:**
```python
from optimusdb_client import OptimusDBClient
import json

client = OptimusDBClient()

# Get all TOSCA templates
result = client.get(criteria=[{"document_type": "tosca_template"}])

# Export to file
with open('templates_export.json', 'w') as f:
    json.dump(result['data'], f, indent=2)

print(f"Exported {len(result['data'])} templates to templates_export.json")
```

**Expected Output:**
```
Exporting documents to: templates_export.json
Retrieved 5 documents
✓ Exported 5 documents
File size: 125 KB
```

---

### Scenario 19: Advanced Analysis

**Purpose:** Analyze templates for statistics and insights

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Get all TOSCA templates
result = client.get(criteria=[{"document_type": "tosca_template"}])

print("="*80)
print("SWARMCHESTRATE TEMPLATE ANALYSIS")
print("="*80)

for doc in result['data']:
    template_name = doc.get('template_name', 'Unknown')
    nodes = doc.get('node_templates', {})
    
    print(f"\n{template_name}:")
    print(f"  Total nodes: {len(nodes)}")
    
    # Count by type
    docker_count = sum(
        1 for node in nodes.values()
        if 'Docker' in node.get('type', '')
    )
    db_count = sum(
        1 for node in nodes.values()
        if 'Database' in node.get('type', '')
    )
    
    print(f"  Docker containers: {docker_count}")
    print(f"  Databases: {db_count}")
    
    # Total CPU requirements
    total_cpus = 0
    for node in nodes.values():
        props = node.get('properties', {})
        cpus = props.get('num_cpus', 0)
        if isinstance(cpus, int):
            total_cpus += cpus
    
    print(f"  Total CPUs required: {total_cpus}")

print("\n" + "="*80)
```

**Expected Output:**
```
================================================================================
SWARMCHESTRATE TEMPLATE ANALYSIS
================================================================================

WebApp-MicroservicesApplication:
  Total nodes: 7
  Docker containers: 6
  Databases: 2
  Total CPUs required: 12

App-Requirements:
  Total nodes: 3
  Docker containers: 0
  Databases: 0
  Total CPUs required: 0

...
================================================================================
```

---

### Scenario 20: Delete All Documents (Clean Slate)

**Purpose:** Remove all documents to reset the database

**Command:**
```bash
python3 optimusdb_client.py delete-all
```

**Python:**
```python
from optimusdb_client import OptimusDBClient

client = OptimusDBClient()

# Get count before
before = client.get()
print(f"Documents before: {len(before['data'])}")

# Delete all
result = client.delete_all()
print(f"Deleted: {result['data']['deleted_count']} documents")

# Verify
after = client.get()
print(f"Documents after: {len(after['data'])}")
```

**Expected Output:**
```
⚠ WARNING: This will delete ALL documents!
Are you sure? (yes/no): yes

Documents before: 20
Deleted: 20 documents
Documents after: 0

✓ Database is now empty
```

**Verification:**
```bash
# Check document count
python3 optimusdb_client.py get | grep -c '"_id"'

# Expected: 0
```

---

## Batch Operations

Use `batch_operations.py` for bulk testing operations.

### Bulk Upload

```bash
# Upload all YAML files from directory
python3 batch_operations.py bulk-upload toscaSamples/

# Upload from custom directory
python3 batch_operations.py bulk-upload /path/to/tosca/files/
```

### Export to JSON

```bash
# Export all documents
python3 batch_operations.py export backup.json

# Export from specific datastore
python3 batch_operations.py export backup.json --dstype kbmetadata

# Export with date in filename
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
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

# Cleanup old versions
python3 batch_operations.py cleanup 'v0\\..*'
```

---

## Query Operators Reference

| Operator | CLI Syntax | Python Syntax | Description | Example |
|----------|-----------|---------------|-------------|---------|
| **Exact match** | `field:value` | `{"field": "value"}` | Exact equality | `type:test` |
| **Regex** | `field:pattern:regex` | `{"field": {"$regex": "pattern"}}` | Pattern match | `_id:tosca_.*:regex` |
| **Greater than** | `field:value:gt` | `{"field": {"$gt": value}}` | Numeric > | `capacity:100:gt` |
| **Greater or equal** | `field:value:gte` | `{"field": {"$gte": value}}` | Numeric >= | `capacity:100:gte` |
| **Less than** | `field:value:lt` | `{"field": {"$lt": value}}` | Numeric < | `capacity:200:lt` |
| **Less or equal** | `field:value:lte` | `{"field": {"$lte": value}}` | Numeric <= | `capacity:200:lte` |
| **Not equal** | `field:value:ne` | `{"field": {"$ne": "value"}}` | Not equal | `status:inactive:ne` |
| **In array** | N/A | `{"field": {"$in": [...]}}` | Value in list | `{"type": {"$in": ["solar", "wind"]}}` |
| **Exists** | N/A | `{"field": {"$exists": true}}` | Field exists | `{"metadata": {"$exists": true}}` |
| **AND** | Multiple --criteria | `{"$and": [{...}, {...}]}` | All conditions | See Scenario 10 |
| **OR** | N/A | `{"$or": [{...}, {...}]}` | Any condition | See Scenario 11 |

---

## Complete Workflow Examples

### Workflow 1: Complete Testing Cycle

```bash
# 1. Check initial state
python3 optimusdb_client.py get | grep -c '"_id"'
# Output: 0 (empty)

# 2. Upload all TOSCA files
python3 batch_operations.py bulk-upload toscaSamples/
# Output: 5 files uploaded, 15-25 documents created

# 3. Query what was uploaded
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'
# Output: 5 TOSCA templates

# 4. Find Docker containers
python3 optimusdb_client.py get --criteria 'node_templates.*.type:.*Docker.*:regex'
# Output: Templates with Docker

# 5. Update deployment status (Python)
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient()
client.update(
    criteria=[{'document_type': 'tosca_template'}],
    update_data=[{'test_status': 'validated', 'tested_at': '2026-01-01'}]
)
print('All templates updated')
"

# 6. Export for backup
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"

# 7. Cleanup (if needed)
python3 optimusdb_client.py delete --criteria 'document_type:flattened_template'

# 8. Final state
python3 optimusdb_client.py get | grep -c '"_id"'
```

### Workflow 2: Automated Testing Script

```python
#!/usr/bin/env python3
"""
Swarmchestrate OptimusDB Automated Test Suite
"""
from optimusdb_client import OptimusDBClient
import sys

def run_tests():
    client = OptimusDBClient(log_level="INFO")
    
    print("="*80)
    print("SWARMCHESTRATE OPTIMUSDB TEST SUITE")
    print("="*80)
    
    # Test 1: Health Check
    print("\n[Test 1] Health Check...")
    if not client.health_check():
        print("✗ FAIL: Server unavailable")
        sys.exit(1)
    print("✓ PASS: Server healthy")
    
    # Test 2: Upload TOSCA files
    print("\n[Test 2] Upload TOSCA files...")
    tosca_files = [
        "toscaSamples/webapp_adt.yaml",
        "toscaSamples/app_requirements.yaml",
        "toscaSamples/capacity_profile.yaml",
        "toscaSamples/deployment_plan.yaml",
        "toscaSamples/opentofu_hybrid.yaml"
    ]
    
    uploaded = 0
    for file_path in tosca_files:
        try:
            result = client.upload_tosca(file_path)
            print(f"  ✓ {file_path}")
            uploaded += 1
        except Exception as e:
            print(f"  ✗ {file_path}: {e}")
    
    print(f"✓ PASS: Uploaded {uploaded}/{len(tosca_files)} files")
    
    # Test 3: Verify uploads
    print("\n[Test 3] Verify uploads...")
    result = client.get(criteria=[{"document_type": "tosca_template"}])
    count = len(result['data'])
    
    if count == 5:
        print(f"✓ PASS: Found {count} templates")
    else:
        print(f"✗ FAIL: Expected 5 templates, found {count}")
    
    # Test 4: Content search
    print("\n[Test 4] Content-based search...")
    docker_result = client.get(criteria=[{
        "node_templates.*.type": {"$regex": ".*Docker.*"}
    }])
    
    if len(docker_result['data']) > 0:
        print(f"✓ PASS: Found {len(docker_result['data'])} templates with Docker")
    else:
        print("✗ FAIL: No Docker containers found")
    
    # Test 5: Update operation
    print("\n[Test 5] Update operation...")
    update_result = client.update(
        criteria=[{"document_type": "tosca_template"}],
        update_data=[{"test_run": "2026-01-01", "test_status": "passed"}]
    )
    
    if update_result['data']['modified_count'] > 0:
        print(f"✓ PASS: Updated {update_result['data']['modified_count']} documents")
    else:
        print("✗ FAIL: No documents updated")
    
    # Test 6: Cleanup
    print("\n[Test 6] Cleanup...")
    delete_result = client.delete_all()
    print(f"✓ PASS: Deleted {delete_result['data']['deleted_count']} documents")
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    run_tests()
```

---

## Troubleshooting

### Connection Refused

**Error:**
```
Error: Connection refused
```

**Solution:**
```bash
# Verify OptimusDB is running
python3 optimusdb_client.py health

# Check correct URL
python3 optimusdb_client.py --url http://193.225.250.240 health

# Test with curl
curl http://193.225.250.240/swarmkb/agent/status
```

### Invalid JSON Response

**Error:**
```
Error: Failed to parse response JSON
```

**Solution:**
```bash
# Enable debug logging
python3 optimusdb_client.py --log-level DEBUG get

# Check server logs
# Verify endpoint exists
```

### Timeout

**Error:**
```
Error: Request timeout after 30 seconds
```

**Solution:**
```python
# Increase timeout
client = OptimusDBClient(timeout=60)
```

### No Documents Found

**Error:**
```
Retrieved 0 document(s)
```

**Solution:**
```bash
# Check correct datastore
python3 optimusdb_client.py get --dstype dsswres

# Verify uploads succeeded
python3 optimusdb_client.py --log-level DEBUG upload toscaSamples/webapp_adt.yaml
```

### Upload Shows "Legacy Mode"

**Problem:**
```
"message": "TOSCA uploaded (legacy mode)",
"queryable": false
```

**Solution:** This shouldn't happen with the current client (full structure mode is default). If you see this:
1. Check you're using the latest `optimusdb_client.py`
2. Verify `store_full_structure=True` in upload_tosca()
3. Contact Swarmchestrate support

---

## Best Practices

### 1. Always Check Health First

```bash
python3 optimusdb_client.py health
```

### 2. Use Debug Logging for Troubleshooting

```bash
python3 optimusdb_client.py --log-level DEBUG upload toscaSamples/webapp_adt.yaml
```

### 3. Export Before Major Operations

```bash
# Before bulk delete or update
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
```

### 4. Verify After Upload

```bash
# Upload
python3 batch_operations.py bulk-upload toscaSamples/

# Verify
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'
```

### 5. Use Specific Queries

Instead of:
```bash
python3 optimusdb_client.py get  # Gets everything
```

Use:
```bash
python3 optimusdb_client.py get --criteria 'document_type:tosca_template'
```

### 6. Test Queries Before Deletes

```bash
# First, see what will be deleted
python3 optimusdb_client.py get --criteria 'type:test'

# Then delete
python3 optimusdb_client.py delete --criteria 'type:test'
```

### 7. Use Meaningful IDs

When creating test documents:
```python
client.create(documents=[{
    "_id": "test_webapp_001",  # Prefix with test_ for easy cleanup
    "name": "Test Document"
}])
```

### 8. Clean Up After Testing

```bash
# Delete test documents
python3 optimusdb_client.py delete --criteria '_id:test_.*:regex'

# Or delete all
python3 optimusdb_client.py delete-all
```

---

## License

MIT License - Free to use and modify for Swarmchestrate testing

---

## Support

**For Swarmchestrate OptimusDB Support:**

1. Check this guide first
2. Enable DEBUG logging: `--log-level DEBUG`
3. Review OptimusDB server logs
4. Check network connectivity to 193.225.250.240
5. Verify TOSCA files are valid YAML

**Contact:** Swarmchestrate ICCS Team

---

**Swarmchestrate OptimusDB - JAN 2026** 🚀
