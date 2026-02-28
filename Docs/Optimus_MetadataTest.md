# OptimusDB Metadata Workflow — Test Report

**Date:** 28 February 2026
**Tester:** George Georgakakos (ICCS)
**Environment:** 3-node OptimusDB cluster (Swarmchestrate)
**Server:** `http://193.225.250.240/optimusdb1` / context: `swarmkb`
**Client:** `optimusdb_client.py` (patched, commit `ad4e9db`)

---

## 1. Test File

```
File:    toscaSamples/webapp_adt.yaml
Size:    5,850 bytes
Content: Microservices web application (Nginx, Python API, PostgreSQL, Redis)
```

---

## 2. Cluster Status

```
Agent:     Qmd9eVtqx7jThaTDG5vioZya7sFgU2nuQFGPejXPEBEzbi
Role:      Coordinator / Leader
Term:      8
Peers:     3 total (1 coordinator + 2 followers)
Connected: 2/2 followers connected
Health:    CPU 11.5%, Memory 72.57/402.94 MB
```

| Peer | Role | CPU | Memory | Score |
|------|------|-----|--------|-------|
| `Qmd9eV...` | Coordinator/Leader | 11.5% | 72.57 MB | 45.73 |
| `QmVXKj...` | Follower | 5.4% | 64.74 MB | 43.94 |
| `QmReim...` | Follower | 9.0% | 67.21 MB | 41.22 |

---

## 3. Test Execution

All tests executed at **19:21–19:46 UTC** on 28 February 2026 from `ubuntu@epm-server`.

---

### Step 0 — Health Check

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='DEBUG')
print(client.health_check())
"
```

**Result:** ✅ PASS
```
2026-02-28 19:21:41 - OptimusDB - INFO - ✓ Server is healthy
True
```

---

### Step 1 — Upload TOSCA File

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
import json
client = OptimusDBClient(log_level='INFO')
result = client.upload_tosca('toscaSamples/webapp_adt.yaml', store_full_structure=True)
print(json.dumps(result, indent=2))
"
```

**Result:** ✅ PASS
```
Template ID:      bdb857c8d4994b0b
Storage type:     full_structure
Queryable:        true
Storage location: dsswres
Indexed fields:   62 sample fields returned
```

**Key response fields:**
```json
{
  "data": {
    "filename": "webapp_adt.yaml",
    "filesize": 5850,
    "message": "TOSCA uploaded with full queryable structure",
    "queryable": true,
    "storage_location": "dsswres",
    "template_id": "bdb857c8d4994b0b"
  },
  "status": 200
}
```

---

### Step 2 — Query Auto-Generated Metadata

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='INFO')
result = client.get_metadata(associated_id='bdb857c8d4994b0b')
data = result.get('data', [])
entries = data if isinstance(data, list) else [data] if data else []
print(f'Entries found: {len(entries)}')
if entries and entries[0]:
    client.print_metadata_summary(entries[0])
"
```

**Result:** ✅ PASS
```
Entries found: 1

──────────────────────────────────────────────────────────────────────
  Metadata Entry: meta-tosca-f6da11b425bf0362
──────────────────────────────────────────────────────────────────────

  Core:
    name                           = WebApp-MicroservicesApplication
    author                         = Swarmchestrate Orchestrator
    metadata_type                  = tosca_resource
    status                         = active
    version                        = 1.0.0
    description                    = Sample Application Description TOSCA Template ...

  Relations:
    associated_id                  = bdb857c8d4994b0b
    component                      = tosca-template
    behaviour                      = infrastructure-definition

  Classification:
    data_domain                    = cloud_orchestration
    data_classification            = consortium
    language                       = en
    license_type                   = consortium-only

  Quality:
    data_quality_score             = 1
    priority                       = medium
    node_count                     = 8
    file_size_bytes                = 5850
    record_count                   = 8

  Temporal:
    created_at                     = 2026-02-28T19:23:14Z
    updated_at                     = 2026-02-28T19:23:14Z
    update_frequency               = on-demand

  Provenance:
    source_agent                   = /usr/local/bin/optimusdb
    source_pod                     = optimusdb1
    source_ip                      = 10.42.0.104
    ipfs_cid                       = /ipfs/QmaryAmqjq8U1qFVqhnGf9ioh4izTkFjyGPVXFRQzAPGjS
    processing_status              = published
```

---

### Step 3 — Verify Upload in Main Data Store

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='INFO')
result = client.get(criteria=[{'_id': 'bdb857c8d4994b0b'}], dstype='dsswres')
data = result.get('data', [])
entries = data if isinstance(data, list) else [data] if data else []
print(f'Documents found: {len(entries)}')
if entries:
    doc = entries[0]
    keys = [k for k in doc.keys()][:15]
    print(f'  top fields: {keys}')
"
```

**Result:** ✅ PASS
```
Documents found: 1
  _id: bdb857c8d4994b0b
  top fields: ['_filename', '_id', '_imported_at', '_lineage', '_original_yaml',
               '_storage_type', 'description', 'imports', 'metadata',
               'topology_template', 'tosca_definitions_version']
```

---

### Step 4a — Query Metadata by ID (CRUD / OrbitDB)

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='INFO')
result = client.get_metadata(metadata_id='meta-tosca-f6da11b425bf0362')
data = result.get('data', [])
entries = data if isinstance(data, list) else [data] if data else []
print(f'Found: {len(entries)} record(s)')
if entries and entries[0]:
    e = entries[0]
    print(f'  _id: {e.get(\"_id\")}')
    print(f'  name: {e.get(\"name\")}')
    print(f'  associated_id: {e.get(\"associated_id\")}')
    print(f'  status: {e.get(\"status\")}')
"
```

**Result:** ✅ PASS
```
Found: 1 record(s)
  _id: meta-tosca-f6da11b425bf0362
  name: WebApp-MicroservicesApplication
  associated_id: bdb857c8d4994b0b
  status: active
```

---

### Step 4b — Query Metadata via SQL

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
import json
client = OptimusDBClient(log_level='INFO')
result = client.execute_sql(\"SELECT id, name, associated_id, status, data_domain, node_count FROM metadata_catalog WHERE associated_id = 'bdb857c8d4994b0b'\")
records = result.get('records', [])
print(f'Rows: {len(records)}')
for r in records:
    print(json.dumps(r, indent=2))
"
```

**Result:** ✅ PASS
```
Rows: 1
{
  "associated_id": "bdb857c8d4994b0b",
  "data_domain": "cloud_orchestration",
  "id": "meta-tosca-f6da11b425bf0362",
  "name": "WebApp-MicroservicesApplication",
  "node_count": 8,
  "status": "active"
}
```

---

### Step 5 — Update Metadata Field

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='INFO')
updated = client.update_metadata_fields('meta-tosca-f6da11b425bf0362', {
    'description': 'Production-grade microservices TOSCA template with Nginx, Python, PostgreSQL and Redis'
})
print(f'updated_at: {updated.get(\"updated_at\")}')
print(f'description: {updated.get(\"description\")}')
"
```

**Result:** ✅ PASS
```
2026-02-28 19:45:16 - ✓ OrbitDB KBMetadata updated
2026-02-28 19:45:16 - ✓ SQLite metadata_catalog updated
updated_at: 2026-02-28T19:45:15.686434Z
description: Production-grade microservices TOSCA template with Nginx, Python, PostgreSQL and Redis
```

---

### Step 6 — Add New Metadata Field

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
client = OptimusDBClient(log_level='INFO')
updated = client.add_metadata_field('meta-tosca-f6da11b425bf0362', 'geo_location', 'Athens, Greece')
print(f'geo_location: {updated.get(\"geo_location\")}')
"
```

**Result:** ✅ PASS
```
2026-02-28 19:45:44 - ✓ OrbitDB KBMetadata updated
2026-02-28 19:45:44 - ✓ SQLite metadata_catalog updated
geo_location: Athens, Greece
```

---

### Final Verification — SQL Confirms All Changes

**Command:**
```bash
python3 -c "
from optimusdb_client import OptimusDBClient
import json
client = OptimusDBClient(log_level='WARNING')
result = client.execute_sql(\"SELECT id, name, description, geo_location, status, node_count, updated_at FROM metadata_catalog WHERE id = 'meta-tosca-f6da11b425bf0362'\")
for r in result.get('records', []):
    print(json.dumps(r, indent=2))
"
```

**Result:** ✅ PASS
```json
{
  "description": "Production-grade microservices TOSCA template with Nginx, Python, PostgreSQL and Redis",
  "geo_location": "Athens, Greece",
  "id": "meta-tosca-f6da11b425bf0362",
  "name": "WebApp-MicroservicesApplication",
  "node_count": 8,
  "status": "active",
  "updated_at": "2026-02-28T19:45:44.043361Z"
}
```

---

## 4. Test Summary

| Step | Description | Result |
|------|------------|--------|
| 0 | Health check | ✅ PASS |
| 1 | Upload TOSCA | ✅ PASS |
| 2 | Metadata by associated_id | ✅ PASS |
| 3 | Verify data in dsswres | ✅ PASS |
| 4a | Metadata by ID (CRUD) | ✅ PASS |
| 4b | Metadata via SQL | ✅ PASS |
| 5 | Update metadata field | ✅ PASS |
| 6 | Add new metadata field | ✅ PASS |
| ✓ | Final SQL verification | ✅ PASS |

**Result: 8/8 PASS**

---

## 5. Data Flow Verified

```
Upload TOSCA ─────────────┬──▶ dsswres (OrbitDB)        ← Step 1, 3
  (webapp_adt.yaml)       │
                          └──▶ KBMetadata (OrbitDB)      ← Step 2, 4a (auto-generated)
                               │
                               └──▶ metadata_catalog      ← Step 4b (SQLite mirror)
                                    (SQLite)
                                         │
           ┌─────────────────────────────┘
           ▼
   Update/Add fields ────▶ OrbitDB + SQLite (dual-write)  ← Step 5, 6
```


---

**Project:** OptimusDB — EU Horizon Europe Grant 101135012 (Swarmchestrate)
**Repository:** https://github.com/georgeGeorgakakos/optimusPy