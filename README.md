# Swarmchestrate OptimusDB Python Client - Complete Testing Guide

**A comprehensive Python client for testing and interacting with the Swarmchestrate OptimusDB decentralized Knowledge Base System.**

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Your Project Files](#your-project-files)
- [CLI Reference](#cli-reference)
- [20 Testing Scenarios - Quick Overview](#20-testing-scenarios---quick-overview)
- [20 Testing Scenarios - Detailed Guide](#20-testing-scenarios---detailed-guide)
- [Batch Operations](#batch-operations)
- [Query Operators Reference](#query-operators-reference)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

The **Swarmchestrate OptimusDB Python Client** is a comprehensive testing and interaction tool for the OptimusDB distributed data catalog system. It enables full CRUD operations, TOSCA template management, and advanced querying capabilities for testing Swarmchestrate's knowledge base infrastructure.

---

## Features

✅ **Full CRUD Operations** - Create, Read, Update, Delete documents  
✅ **TOSCA File Upload** - Upload and process TOSCA YAML templates  
✅ **Advanced Queries** - Regex, operators ($gt, $lt, $in, etc.), nested field queries  
✅ **Batch Operations** - Bulk upload, export, import, cleanup  
✅ **Content-Based Search** - Search inside TOSCA metadata, properties  
✅ **CLI Interface** - Easy command-line usage for quick testing  
✅ **Logging & Debug** - Comprehensive logging with adjustable levels

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

```bash
python3 batch_operations.py bulk-upload toscaSamples/
```

**Expected Output:**
```
Starting bulk upload from: toscaSamples/

✓ webapp_adt.yaml
✓ app_requirements.yaml
✓ capacity_profile.yaml
✓ deployment_plan.yaml
✓ opentofu_hybrid.yaml

Total files: 5
Successful: 5
```

---

### Query Your Data

```bash
python3 optimusdb_client.py get
```

**Expected Output:**
```
Retrieved 5 document(s)

Document IDs:
  1. 35e18fc5e1d8bdf4 (N/A)
  2. 1d68ededb3208434 (N/A)
  3. 8461a5719430370e (N/A)
  4. 1f019c344258970c (N/A)
  5. 69c1fe30be6a2340 (N/A)
```

---

## Your Project Files

```
📂 Swarmchestrate Testing Project
├── optimusdb_client.py          ← Main Python client
├── batch_operations.py           ← Bulk operations tool
├── requirements.txt              ← Dependencies
└── toscaSamples/                 ← Your TOSCA templates
    ├── webapp_adt.yaml           (6.0 KB) - Web application
    ├── app_requirements.yaml     (11 KB)  - Requirements
    ├── capacity_profile.yaml     (6.9 KB) - Capacity profile
    ├── deployment_plan.yaml      (14 KB)  - Deployment plan
    └── opentofu_hybrid.yaml      (11 KB)  - Hybrid infrastructure
```

---

## CLI Reference

### Global Options

```bash
python3 optimusdb_client.py [OPTIONS] COMMAND [COMMAND_OPTIONS]
```

**Available Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--url URL` | OptimusDB base URL | `http://193.225.250.240` |
| `--context CONTEXT` | API context path | `swarmkb` |
| `--log-level LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

---

### Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `get` | Retrieve documents | `python3 optimusdb_client.py get` |
| `create` | Insert documents | `python3 optimusdb_client.py create --json file.json` |
| `update` | Modify documents | `python3 optimusdb_client.py update --criteria '_id:123' --data '{}'` |
| `delete` | Remove documents | `python3 optimusdb_client.py delete --criteria 'type:test'` |
| `delete-all` | Clear all documents | `python3 optimusdb_client.py delete-all` |
| `upload` | Upload TOSCA file | `python3 optimusdb_client.py upload file.yaml` |
| `health` | Health check | `python3 optimusdb_client.py health` |
| `status` | Agent status | `python3 optimusdb_client.py status` |
| `peers` | List cluster peers | `python3 optimusdb_client.py peers` |

---

## 20 Testing Scenarios - Quick Overview

**Use this table to understand what each scenario tests and expected outcomes.**

| # | Scenario Goal | Command | Expected Outcome |
|---|---------------|---------|------------------|
| **1** | **Establish baseline** - Check current document count | `python3 optimusdb_client.py get` | Shows: `Retrieved X document(s)` |
| **2** | **Upload single file** - Test individual TOSCA upload | `python3 optimusdb_client.py upload toscaSamples/webapp_adt.yaml` | Upload successful, shows hash ID |
| **3** | **Batch upload** - Upload all 5 TOSCA files at once | `python3 batch_operations.py bulk-upload toscaSamples/` | All 5 files uploaded successfully |
| **4** | **List filenames** - See what files were uploaded | `python3 optimusdb_client.py get \| grep '_filename'` | Lists 5 YAML filenames |
| **5** | **Query by filename** - Find specific file | `python3 optimusdb_client.py get --criteria '_filename:webapp_adt.yaml'` | Retrieved 1 document (webapp file) |
| **6** | **Query by template name** - Search by TOSCA template name | `python3 optimusdb_client.py get --criteria 'metadata.template_name:.*WebApp.*:regex'` | Retrieved 1 document with WebApp in name |
| **7** | **Query by datastore** - Find templates in specific datastore | `python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'` | Retrieved documents from ADT datastore |
| **8** | **Query by author** - Find templates by author | `python3 optimusdb_client.py get --criteria 'metadata.template_author:Swarmchestrate.*:regex'` | Retrieved all Swarmchestrate templates |
| **9** | **Query by version** - Find specific version | `python3 optimusdb_client.py get --criteria 'metadata.template_version:1.0.0'` | Retrieved version 1.0.0 templates |
| **10** | **Query by TOSCA version** - Find by TOSCA spec version | `python3 optimusdb_client.py get --criteria 'tosca_definitions_version:tosca_simple_yaml_1_3'` | Retrieved TOSCA 1.3 templates |
| **11** | **Query by hash ID** - Get specific document by ID | `python3 optimusdb_client.py get --criteria '_id:35e18fc5e1d8bdf4'` | Retrieved 1 specific document |
| **12** | **Query by upload time** - Find recently uploaded files | `python3 optimusdb_client.py get --criteria '_imported_at:2026-01-01.*:regex'` | Retrieved today's uploads |
| **13** | **Complex AND query** - Multiple conditions (WebApp + ADT) | `python3 optimusdb_client.py get --criteria '$and:[{"metadata.template_name":".*WebApp.*:regex"},{"metadata.kb_datastore":"ADT"}]'` | Retrieved documents matching both conditions |
| **14** | **Complex OR query** - Alternative conditions | `python3 optimusdb_client.py get --criteria '$or:[{"_filename":".*opentofu.*:regex"},{"_filename":".*capacity.*:regex"}]'` | Retrieved documents matching either condition |
| **15** | **Count documents** - Get document statistics | `python3 optimusdb_client.py get \| grep -c '_filename'` | Shows number: 5 |
| **16** | **Export all** - Backup all documents to JSON | `python3 batch_operations.py export backup.json` | JSON file created with all documents |
| **17** | **Delete by filename** - Remove specific file | `python3 optimusdb_client.py delete --criteria '_filename:test.yaml'` | Deleted 1 document |
| **18** | **Delete by ID** - Remove by hash ID | `python3 optimusdb_client.py delete --criteria '_id:35e18fc5e1d8bdf4'` | Deleted 1 document |
| **19** | **Delete pattern** - Remove multiple matching files | `python3 optimusdb_client.py delete --criteria '_filename:.*test.*:regex'` | Deleted X matching documents |
| **20** | **Delete all & reset** - Clean slate for fresh start | `python3 optimusdb_client.py delete-all` | All documents deleted, count: 0 |

---

## 20 Testing Scenarios - Detailed Guide

### Scenario 1: Get All Documents (Baseline)

**Goal:** Establish baseline - see current state of database

**Command:**
```bash
python3 optimusdb_client.py get
```

**What it does:** Retrieves all documents from the default datastore (dsswres)

**Expected Output:**
```
Retrieved 5 document(s)

Document IDs:
  1. 35e18fc5e1d8bdf4 (N/A)
  2. 1d68ededb3208434 (N/A)
  3. 8461a5719430370e (N/A)
  4. 1f019c344258970c (N/A)
  5. 69c1fe30be6a2340 (N/A)
```

**Use case:** Run this first to understand the current database state before testing

**Verification:**
```bash
# Count documents
python3 optimusdb_client.py get | grep -c '"_id"'
# Output: 5
```

---

### Scenario 2: Upload Single TOSCA File

**Goal:** Test uploading a single TOSCA YAML file

**Command:**
```bash
python3 optimusdb_client.py upload toscaSamples/webapp_adt.yaml
```

**What it does:** Uploads one TOSCA file, creates a document with hash ID

**Expected Output:**
```
Uploading TOSCA file: toscaSamples/webapp_adt.yaml
File size: 5849 bytes
Upload successful
```

**Use case:** Test individual file upload capability

**Verification:**
```bash
# Check the file appears in listing
python3 optimusdb_client.py get | grep 'webapp_adt.yaml'
```

---

### Scenario 3: Batch Upload All TOSCA Files

**Goal:** Upload all 5 TOSCA files in bulk operation

**Command:**
```bash
python3 batch_operations.py bulk-upload toscaSamples/
```

**What it does:** Scans directory and uploads all .yaml files

**Expected Output:**
```
Starting bulk upload from: toscaSamples/

✓ webapp_adt.yaml
✓ app_requirements.yaml
✓ capacity_profile.yaml
✓ deployment_plan.yaml
✓ opentofu_hybrid.yaml

================================================================================
UPLOAD SUMMARY
================================================================================
Total files: 5
Successful: 5
Failed: 0
```

**Use case:** Quickly populate database with multiple templates

**Verification:**
```bash
# Count files uploaded
python3 optimusdb_client.py get | grep -c '_filename'
# Output: 5
```

---

### Scenario 4: List All Filenames

**Goal:** See what YAML files were uploaded

**Command:**
```bash
python3 optimusdb_client.py get | grep '_filename'
```

**What it does:** Filters output to show only filename fields

**Expected Output:**
```
"_filename": "opentofu_hybrid.yaml",
"_filename": "webapp_adt.yaml",
"_filename": "capacity_profile.yaml",
"_filename": "deployment_plan.yaml",
"_filename": "app_requirements.yaml",
```

**Use case:** Quick inventory of uploaded files

**Alternative:**
```bash
# More readable format
python3 optimusdb_client.py get | grep '"_filename"' | sort
```

---

### Scenario 5: Query by Filename

**Goal:** Retrieve a specific file by its filename

**Command:**
```bash
python3 optimusdb_client.py get --criteria '_filename:webapp_adt.yaml'
```

**What it does:** Exact match search on _filename field

**Expected Output:**
```
Retrieved 1 document(s)

Document IDs:
  1. 1d68ededb3208434 (N/A)

"_filename": "webapp_adt.yaml",
"metadata": {
  "template_name": "WebApp-MicroservicesApplication",
  ...
}
```

**Use case:** Locate specific file for inspection or modification

**Alternative queries:**
```bash
# Get deployment plan
python3 optimusdb_client.py get --criteria '_filename:deployment_plan.yaml'

# Get opentofu file
python3 optimusdb_client.py get --criteria '_filename:opentofu_hybrid.yaml'
```

---

### Scenario 6: Query by Template Name (Regex)

**Goal:** Search templates by name pattern using regex

**Command:**
```bash
python3 optimusdb_client.py get --criteria 'metadata.template_name:.*WebApp.*:regex'
```

**What it does:** Searches metadata.template_name field for "WebApp" anywhere in the name

**Expected Output:**
```
Retrieved 1 document(s)

"metadata": {
  "template_name": "WebApp-MicroservicesApplication",
  "template_author": "Swarmchestrate Orchestrator",
  "template_version": "1.0.0"
}
```

**Use case:** Find templates by descriptive name when filename is unknown

**More regex examples:**
```bash
# Find "Hybrid" templates
python3 optimusdb_client.py get --criteria 'metadata.template_name:.*Hybrid.*:regex'

# Find templates starting with "App"
python3 optimusdb_client.py get --criteria 'metadata.template_name:^App.*:regex'

# Case-insensitive: deployment
python3 optimusdb_client.py get --criteria 'metadata.template_name:.*deployment.*:regex'
```

---

### Scenario 7: Query by Datastore

**Goal:** Find all templates stored in a specific datastore

**Command:**
```bash
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'
```

**What it does:** Filters by kb_datastore metadata field

**Expected Output:**
```
Retrieved 1 document(s)

"metadata": {
  "kb_datastore": "ADT",
  "template_name": "WebApp-MicroservicesApplication"
}
```

**Use case:** Organize templates by logical datastore categories

**Other datastores to query:**
```bash
# OpenTofu templates
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:OpenTofu_TOSCA_Templates'

# Any datastore with "Templates" in name
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:.*Templates:regex'
```

---

### Scenario 8: Query by Author

**Goal:** Find templates created by specific author

**Command:**
```bash
python3 optimusdb_client.py get --criteria 'metadata.template_author:Swarmchestrate.*:regex'
```

**What it does:** Searches template_author field with regex

**Expected Output:**
```
Retrieved 5 document(s)

All documents by Swarmchestrate Orchestrator
```

**Use case:** Filter templates by creation source or team

**Variations:**
```bash
# Exact author match
python3 optimusdb_client.py get --criteria 'metadata.template_author:Swarmchestrate Orchestrator'
```

---

### Scenario 9: Query by Version

**Goal:** Find templates with specific version number

**Command:**
```bash
python3 optimusdb_client.py get --criteria 'metadata.template_version:1.0.0'
```

**What it does:** Exact match on template_version field

**Expected Output:**
```
Retrieved 5 document(s)

All version 1.0.0 templates
```

**Use case:** Version management and compatibility checking

**Version patterns:**
```bash
# All 1.x versions
python3 optimusdb_client.py get --criteria 'metadata.template_version:1\\..*:regex'

# Specific version
python3 optimusdb_client.py get --criteria 'metadata.template_version:2.0.0'
```

---

### Scenario 10: Query by TOSCA Version

**Goal:** Find templates using specific TOSCA specification

**Command:**
```bash
python3 optimusdb_client.py get --criteria 'tosca_definitions_version:tosca_simple_yaml_1_3'
```

**What it does:** Filters by TOSCA spec version

**Expected Output:**
```
Retrieved 5 document(s)

All TOSCA 1.3 compliant templates
```

**Use case:** Ensure TOSCA specification compliance

---

### Scenario 11: Query by Hash ID

**Goal:** Retrieve specific document using its hash ID

**Command:**
```bash
python3 optimusdb_client.py get --criteria '_id:35e18fc5e1d8bdf4'
```

**What it does:** Direct lookup by unique document ID

**Expected Output:**
```
Retrieved 1 document(s)

Document IDs:
  1. 35e18fc5e1d8bdf4 (N/A)

Complete document with all fields
```

**Use case:** Direct access to specific document when ID is known

**Note:** Hash IDs are generated during upload - use actual IDs from your system

**Get all IDs:**
```bash
# List all document IDs
python3 optimusdb_client.py get | grep '"_id"'
```

---

### Scenario 12: Query by Upload Time

**Goal:** Find documents uploaded at specific time

**Command:**
```bash
python3 optimusdb_client.py get --criteria '_imported_at:2026-01-01.*:regex'
```

**What it does:** Searches _imported_at timestamp field

**Expected Output:**
```
Retrieved 5 document(s)

All documents imported on 2026-01-01
```

**Use case:** Track uploads by date, audit recent changes

**Time-based queries:**
```bash
# Specific hour
python3 optimusdb_client.py get --criteria '_imported_at:2026-01-01T16:.*:regex'

# Specific date range
python3 optimusdb_client.py get --criteria '_imported_at:2026-01.*:regex'
```

---

### Scenario 13: Complex AND Query

**Goal:** Find documents matching multiple conditions simultaneously

**Command:**
```bash
python3 optimusdb_client.py get --criteria '$and:[{"metadata.template_name":".*WebApp.*:regex"},{"metadata.kb_datastore":"ADT"}]'
```

**What it does:** Combines two conditions - template name contains "WebApp" AND datastore is "ADT"

**Expected Output:**
```
Retrieved 1 document(s)

Document matching BOTH conditions:
- Template name contains "WebApp"
- Stored in ADT datastore
```

**Use case:** Precise filtering with multiple requirements

**More AND examples:**
```bash
# Version 1.0.0 in OpenTofu datastore
python3 optimusdb_client.py get --criteria '$and:[{"metadata.template_version":"1.0.0"},{"metadata.kb_datastore":"OpenTofu_TOSCA_Templates"}]'

# Swarmchestrate author AND version 1.0.0
python3 optimusdb_client.py get --criteria '$and:[{"metadata.template_author":"Swarmchestrate.*:regex"},{"metadata.template_version":"1.0.0"}]'
```

---

### Scenario 14: Complex OR Query

**Goal:** Find documents matching any of multiple conditions

**Command:**
```bash
python3 optimusdb_client.py get --criteria '$or:[{"_filename":".*opentofu.*:regex"},{"_filename":".*capacity.*:regex"}]'
```

**What it does:** Retrieves documents where filename contains "opentofu" OR "capacity"

**Expected Output:**
```
Retrieved 2 document(s)

Documents matching EITHER condition:
- opentofu_hybrid.yaml
- capacity_profile.yaml
```

**Use case:** Broad search across multiple criteria

**More OR examples:**
```bash
# Deployment OR webapp files
python3 optimusdb_client.py get --criteria '$or:[{"_filename":".*deployment.*:regex"},{"_filename":".*webapp.*:regex"}]'

# ADT OR OpenTofu datastores
python3 optimusdb_client.py get --criteria '$or:[{"metadata.kb_datastore":"ADT"},{"metadata.kb_datastore":"OpenTofu_TOSCA_Templates"}]'
```

---

### Scenario 15: Count Documents

**Goal:** Get quick count of documents without full output

**Command:**
```bash
python3 optimusdb_client.py get | grep -c '_filename'
```

**What it does:** Counts lines containing "_filename" field

**Expected Output:**
```
5
```

**Use case:** Quick inventory check, monitoring document count

**Alternative counting:**
```bash
# Count all documents by ID
python3 optimusdb_client.py get | grep -c '"_id"'

# Count documents in specific datastore
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT' | grep -c '"_id"'
```

---

### Scenario 16: Export All Documents

**Goal:** Backup all documents to JSON file

**Command:**
```bash
python3 batch_operations.py export backup.json
```

**What it does:** Retrieves all documents and saves to JSON file

**Expected Output:**
```
Exporting documents to: backup.json

Fetching all documents...
Retrieved 5 documents

Exporting to JSON...
✓ Exported 5 documents to backup.json

File size: 125 KB
```

**Use case:** Backup before major operations, data migration, archival

**Export with timestamp:**
```bash
# Create dated backup
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
```

---

### Scenario 17: Delete by Filename

**Goal:** Remove specific file from database

**Command:**
```bash
python3 optimusdb_client.py delete --criteria '_filename:test.yaml'
```

**What it does:** Deletes document matching exact filename

**Expected Output:**
```
Deleting documents...
Criteria: [{"_filename": "test.yaml"}]

Delete result: {
  'status': 200,
  'data': {
    'deleted_count': 1
  }
}

✓ Deleted 1 document(s)
```

**Use case:** Remove individual files, cleanup test data

**Verification:**
```bash
# Verify deletion
python3 optimusdb_client.py get --criteria '_filename:test.yaml'
# Output: Retrieved 0 document(s)
```

---

### Scenario 18: Delete by Hash ID

**Goal:** Remove document using its unique hash ID

**Command:**
```bash
python3 optimusdb_client.py delete --criteria '_id:35e18fc5e1d8bdf4'
```

**What it does:** Direct deletion by document ID

**Expected Output:**
```
✓ Deleted 1 document(s)
```

**Use case:** Precise deletion when ID is known

**Get ID first:**
```bash
# Find ID of file to delete
python3 optimusdb_client.py get | grep -A 1 'webapp_adt.yaml' | grep '_id'

# Then delete using that ID
python3 optimusdb_client.py delete --criteria '_id:HASH_ID_HERE'
```

---

### Scenario 19: Delete by Pattern

**Goal:** Remove multiple documents matching pattern

**Command:**
```bash
python3 optimusdb_client.py delete --criteria '_filename:.*test.*:regex'
```

**What it does:** Deletes all files with "test" in filename

**Expected Output:**
```
✓ Deleted X document(s)
```

**Use case:** Bulk cleanup of test files, temporary data

**Pattern examples:**
```bash
# Delete all deployment files
python3 optimusdb_client.py delete --criteria '_filename:.*deployment.*:regex'

# Delete all files starting with "temp_"
python3 optimusdb_client.py delete --criteria '_filename:^temp_.*:regex'
```

**⚠️ WARNING:** Always verify pattern matches expected files before deleting!

**Safe practice:**
```bash
# 1. First, see what will be deleted
python3 optimusdb_client.py get --criteria '_filename:.*test.*:regex'

# 2. Verify the list, then delete
python3 optimusdb_client.py delete --criteria '_filename:.*test.*:regex'
```

---

### Scenario 20: Delete All Documents (Clean Slate)

**Goal:** Remove all documents to reset database

**Command:**
```bash
python3 optimusdb_client.py delete-all
```

**What it does:** Deletes every document in the datastore

**Expected Output:**
```
⚠ WARNING: This will delete ALL documents!
Are you sure? (yes/no): yes

Deleting all documents...

Delete result: {
  'deleted_count': 5
}

✓ Deleted 5 document(s)
✓ Database is now empty
```

**Use case:** Reset before new test cycle, cleanup after testing

**Verification:**
```bash
# Check database is empty
python3 optimusdb_client.py get
# Output: Retrieved 0 document(s)

# Count should be 0
python3 optimusdb_client.py get | grep -c '"_id"'
# Output: 0
```

**Skip confirmation (dangerous!):**
```bash
python3 optimusdb_client.py delete-all --confirm
```

---

## Batch Operations

### Bulk Upload

**Upload all YAML files from directory:**

```bash
python3 batch_operations.py bulk-upload toscaSamples/
```

**Custom directory:**
```bash
python3 batch_operations.py bulk-upload /path/to/tosca/files/
```

---

### Export to JSON

**Export all documents:**

```bash
python3 batch_operations.py export backup.json
```

**Export with date:**
```bash
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
```

---

### Import from JSON

**Import documents:**

```bash
python3 batch_operations.py import backup.json
```

---

## Query Operators Reference

| Operator | CLI Syntax | Description | Example |
|----------|-----------|-------------|---------|
| **Exact match** | `field:value` | Exact equality | `_filename:webapp_adt.yaml` |
| **Regex** | `field:pattern:regex` | Pattern match | `_filename:.*test.*:regex` |
| **Greater than** | `field:value:gt` | Numeric > | `capacity:100:gt` |
| **Greater or equal** | `field:value:gte` | Numeric >= | `capacity:100:gte` |
| **Less than** | `field:value:lt` | Numeric < | `capacity:200:lt` |
| **Less or equal** | `field:value:lte` | Numeric <= | `capacity:200:lte` |
| **Not equal** | `field:value:ne` | Not equal | `status:inactive:ne` |
| **AND** | `$and:[{...},{...}]` | All conditions | See Scenario 13 |
| **OR** | `$or:[{...},{...}]` | Any condition | See Scenario 14 |

---

## Complete Workflow Examples

### Workflow 1: Complete Testing Cycle

```bash
# 1. Check initial state
python3 optimusdb_client.py get | grep -c '"_id"'
# Output: 0 (empty)

# 2. Upload all TOSCA files
python3 batch_operations.py bulk-upload toscaSamples/
# Output: 5 files uploaded

# 3. Verify uploads
python3 optimusdb_client.py get | grep '_filename'
# Output: 5 filenames listed

# 4. Query by template name
python3 optimusdb_client.py get --criteria 'metadata.template_name:.*WebApp.*:regex'
# Output: 1 document

# 5. Export for backup
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
# Output: JSON file created

# 6. Cleanup
python3 optimusdb_client.py delete-all
# Output: All deleted

# 7. Verify clean
python3 optimusdb_client.py get | grep -c '"_id"'
# Output: 0
```

---

### Workflow 2: Find and Export Specific Templates

```bash
# 1. Find ADT templates
python3 optimusdb_client.py get --criteria 'metadata.kb_datastore:ADT'

# 2. Find version 1.0.0
python3 optimusdb_client.py get --criteria 'metadata.template_version:1.0.0'

# 3. Complex query: WebApp in ADT
python3 optimusdb_client.py get --criteria '$and:[{"metadata.template_name":".*WebApp.*:regex"},{"metadata.kb_datastore":"ADT"}]'

# 4. Export results
python3 batch_operations.py export adt_templates.json
```

---

### Workflow 3: Cleanup Old Test Files

```bash
# 1. See what test files exist
python3 optimusdb_client.py get --criteria '_filename:.*test.*:regex'

# 2. Count them
python3 optimusdb_client.py get --criteria '_filename:.*test.*:regex' | grep -c '"_id"'

# 3. Delete test files
python3 optimusdb_client.py delete --criteria '_filename:.*test.*:regex'

# 4. Verify deletion
python3 optimusdb_client.py get --criteria '_filename:.*test.*:regex'
# Output: Retrieved 0 document(s)
```

---

## Troubleshooting

### Connection Refused

**Problem:** Cannot connect to OptimusDB server

**Solution:**
```bash
# Test connection
python3 optimusdb_client.py health

# Check URL
python3 optimusdb_client.py --url http://193.225.250.240 health

# Test with curl
curl http://193.225.250.240/swarmkb/agent/status
```

---

### No Documents Found

**Problem:** Query returns 0 documents

**Solutions:**

1. **Check documents exist:**
```bash
python3 optimusdb_client.py get
```

2. **Verify field names:**
```bash
# List all fields
python3 optimusdb_client.py get | grep '"_'
```

3. **Check criteria syntax:**
```bash
# Use regex for flexible matching
python3 optimusdb_client.py get --criteria 'field:.*pattern.*:regex'
```

---

### Upload Failed

**Problem:** File upload does not complete

**Solutions:**

1. **Check file exists:**
```bash
ls -lh toscaSamples/webapp_adt.yaml
```

2. **Use debug logging:**
```bash
python3 optimusdb_client.py --log-level DEBUG upload toscaSamples/webapp_adt.yaml
```

3. **Check file format:**
```bash
# Verify YAML is valid
python3 -c "import yaml; yaml.safe_load(open('toscaSamples/webapp_adt.yaml'))"
```

---

## Best Practices

### 1. Always Check Health First

```bash
python3 optimusdb_client.py health
```

---

### 2. Backup Before Major Operations

```bash
# Before bulk delete
python3 batch_operations.py export "backup_$(date +%Y%m%d).json"
```

---

### 3. Verify Queries Before Deletes

```bash
# 1. See what will be deleted
python3 optimusdb_client.py get --criteria '_filename:.*test.*:regex'

# 2. Then delete
python3 optimusdb_client.py delete --criteria '_filename:.*test.*:regex'
```

---

### 4. Use Debug Logging for Issues

```bash
python3 optimusdb_client.py --log-level DEBUG get --criteria 'field:value'
```

---

### 5. Count Documents Regularly

```bash
# Quick count
python3 optimusdb_client.py get | grep -c '"_id"'
```

---

### 6. Use Meaningful Test File Names

```bash
# Good: Prefix test files for easy cleanup
test_webapp.yaml
test_deployment.yaml

# Then cleanup easily
python3 optimusdb_client.py delete --criteria '_filename:test_.*:regex'
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
4. Verify TOSCA files are valid YAML

**Contact:** Swarmchestrate ICCS Team

---

**Swarmchestrate OptimusDB - JAN 2026** 🚀
