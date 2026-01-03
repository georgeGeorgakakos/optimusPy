# OptimusDB API Specification

**Project:** EU Horizon Europe Grant 101135012 (Swarmchestrate)  
**Version:** 1.0  
**Date:** December 19, 2025

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
  - [1. File Upload](#1-file-upload)
  - [2. TOSCA Queries](#2-tosca-queries)
  - [3. Advanced Queries](#3-advanced-queries)
  - [4. CRUD Operations](#4-crud-operations)
  - [5. Advanced Features](#5-advanced-features)
  - [6. System Operations](#6-system-operations)
  - [7. SQL Operations](#7-sql-operations)
  - [8. Event Management System (EMS)](#8-event-management-system-ems)
- [Query Operators](#query-operators)
- [Query Strategies](#query-strategies)
- [Environment Variables](#environment-variables)

---

## Overview

OptimusDB is a distributed data catalog system designed for managing TOSCA templates and metadata in decentralized environments. This specification covers all API endpoints and operations available in the OptimusDB system.

### Key Features

- **TOSCA Template Management**: Upload, query, and manage TOSCA templates
- **Distributed Queries**: Execute queries across peer-to-peer networks
- **SQL Operations**: Support for standard SQL DML operations
- **CRUD Operations**: Full create, read, update, delete functionality
- **Event Management**: Comprehensive logging and event tracking
- **Performance Monitoring**: Benchmarking and cache statistics

### Base Configuration

- **Base URL**: `http://localhost:18001` (configurable)
- **API Version**: `optimusdb1`
- **Context Path**: `/{context}` (environment-specific)
- **Content-Type**: `application/json`

---

## Getting Started

### Prerequisites

1. OptimusDB instance running
2. Environment variables configured
3. Base64-encoded TOSCA files (for uploads)

### Setup Steps

1. Set the `{{base_url}}` variable (default: `http://localhost:18001`)
2. Set the `{{context}}` variable for your environment
3. Prepare TOSCA files in base64 format
4. Upload TOSCA files using the upload endpoint
5. Execute queries and operations

---

## API Endpoints

### 1. File Upload

Upload TOSCA templates to OptimusDB for storage and querying.

#### Upload TOSCA File

**Endpoint:** `POST /{context}/upload`

**Request Body:**
```json
{
  "file": "<base64_encoded_content>",
  "filename": "template_name.yaml",
  "store_full_structure": true
}
```

**Response:**
```json
{
  "status": 200,
  "data": {
    "template_id": "generated_template_id",
    "queryable": true,
    "storage_location": "dsswres",
    "message": "File uploaded successfully"
  }
}
```

#### Sample TOSCA Templates

The system supports uploading various TOSCA template types:

1. **WebApp ADT** - Microservices application with:
   - 4 Docker containers (frontend, backend, PostgreSQL, Redis)
   - 4 container runtimes
   - 3 policies (scaling, placement, monitoring)
   - Ports: 80, 443, 5432, 6379, 8080

2. **Capacity Profile** - Edge cluster specifications:
   - 32 cores, 128 GB RAM
   - NVIDIA A100 GPU (40 GB)
   - 2 TB NVMe SSD
   - 10 Gbps network
   - Kubernetes runtime

3. **OpenTofu Hybrid** - Infrastructure deployment:
   - Kubernetes namespace
   - Nginx ingress
   - Istio service mesh
   - Prometheus monitoring
   - OpenTofu resource mappings

4. **Deployment Plan** - Release workflow:
   - 5 deployment instructions
   - 9-step deployment workflow
   - 6-step rollback workflow
   - Resource allocation details
   - Health checks

5. **Application Requirements** - ML training workload:
   - GPU requirements: 2-4 GPUs (A100/H100/V100)
   - Memory: 64-128 GB
   - Storage: 1.75 TB
   - Network: 10-25 Gbps
   - 6 comprehensive policies

---

### 2. TOSCA Queries

Query TOSCA templates using various criteria and filters.

#### Get All TOSCA Templates

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "crudget",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": []
}
```

**Description:** Retrieves all TOSCA templates from the DocumentStore.

#### Find by Template ID

**Request Body:**
```json
{
  "method": {
    "cmd": "crudget",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": "template_id_here"
    }
  ]
}
```

#### Find by TOSCA Version

**Request Body:**
```json
{
  "method": {
    "cmd": "crudget",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "tosca_definitions_version": "tosca_simple_yaml_1_3"
    }
  ]
}
```

#### Query with Nested Fields

**Request Body:**
```json
{
  "method": {
    "cmd": "query",
    "argcnt": 0
  },
  "criteria": [
    {
      "location.country": "Greece"
    }
  ],
  "options": {
    "strategy": "LOCAL_THEN_REMOTE_MERGE",
    "time_budget_ms": 1500,
    "annotate_source": true
  }
}
```

---

### 3. Advanced Queries

Complex queries with advanced filtering and distributed operations.

#### Query with Operators

**Request Body:**
```json
{
  "method": {
    "cmd": "query",
    "argcnt": 0
  },
  "criteria": [
    {
      "type": "solar",
      "status": "operational",
      "capacity_mw": {"$gte": 500}
    }
  ],
  "options": {
    "strategy": "LOCAL_THEN_REMOTE_MERGE",
    "time_budget_ms": 1500,
    "annotate_source": true
  }
}
```

#### Distributed Query with Remote-Only Strategy

**Request Body:**
```json
{
  "method": {
    "cmd": "query"
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": {"$regex": "pattern"}
    }
  ],
  "options": {
    "strategy": "REMOTE_ONLY",
    "consistency": "BEST_EFFORT",
    "include_local": false,
    "annotate_source": true,
    "time_budget_ms": 1200
  }
}
```

---

### 4. CRUD Operations

Full CRUD (Create, Read, Update, Delete) functionality for document management.

#### Create (Insert) Document

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "crudput",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": "unique_document_id",
      "name": "Document Name",
      "type": "document_type",
      "capacity_mw": 500,
      "location": {
        "country": "Greece",
        "region": "Attica",
        "coordinates": {
          "lat": 37.9838,
          "lon": 23.7275
        }
      },
      "status": "operational",
      "commissioned_date": "2024-06-15"
    }
  ]
}
```

**Response:**
```json
{
  "status": 200,
  "data": "Successfully inserted document with ID: unique_document_id"
}
```

#### Read (Query) Document

**Request Body:**
```json
{
  "method": {
    "cmd": "crudget",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": "unique_document_id"
    }
  ]
}
```

#### Update Document

**Request Body:**
```json
{
  "method": {
    "cmd": "crudupdate",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": "unique_document_id"
    }
  ],
  "UpdateData": [
    {
      "status": "maintenance",
      "maintenance_reason": "Scheduled panel cleaning",
      "capacity_mw": 550
    }
  ]
}
```

**Note:** The `_id` field is preserved during updates. An `_updated_at` timestamp is automatically added.

#### Delete Document

**Request Body:**
```json
{
  "method": {
    "cmd": "cruddelete",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": "unique_document_id"
    }
  ]
}
```

#### Delete All Documents

**Request Body:**
```json
{
  "method": {
    "cmd": "cruddelete",
    "argcnt": 1
  },
  "dstype": "dsswres",
  "criteria": [
    {
      "_id": {"$regex": "^.*$"}
    }
  ]
}
```

---

### 5. Advanced Features

Advanced query strategies and distributed system features.

#### Query Strategies

OptimusDB supports multiple query execution strategies:

##### LOCAL_ONLY
Query only the local node's cache.

```json
{
  "method": {"cmd": "query"},
  "dstype": "dsswres",
  "criteria": [{"field": "value"}],
  "options": {
    "strategy": "LOCAL_ONLY",
    "time_budget_ms": 500
  }
}
```

##### REMOTE_ONLY
Query only remote peers, excluding local data.

```json
{
  "options": {
    "strategy": "REMOTE_ONLY",
    "consistency": "BEST_EFFORT",
    "include_local": false,
    "annotate_source": true,
    "time_budget_ms": 1200
  }
}
```

##### LOCAL_THEN_REMOTE_MERGE
Query local cache first, then merge with remote results.

```json
{
  "options": {
    "strategy": "LOCAL_THEN_REMOTE_MERGE",
    "time_budget_ms": 1500,
    "annotate_source": true
  }
}
```

##### REMOTE_THEN_LOCAL_FALLBACK
Query remote peers first, fall back to local if needed.

```json
{
  "options": {
    "strategy": "REMOTE_THEN_LOCAL_FALLBACK",
    "time_budget_ms": 2000
  }
}
```

#### Consistency Levels

- **BEST_EFFORT**: Fast responses, may be incomplete
- **EVENTUAL**: Wait for eventual consistency
- **STRONG**: Wait for strong consistency guarantees

---

### 6. System Operations

System health, monitoring, and administrative operations.

#### Check Health

**Endpoint:** `GET /{context}/health`

**Response:**
```json
{
  "status": "healthy",
  "uptime": "24h15m30s",
  "version": "1.0.0"
}
```

#### Get Cluster Status

**Endpoint:** `GET /{context}/cluster/status`

**Response:**
```json
{
  "total_peers": 8,
  "connected_peers": 7,
  "coordinator": "12D3KooWXXX...",
  "this_node": {
    "peer_id": "12D3KooWYYY...",
    "role": "follower",
    "uptime": "12h45m"
  }
}
```

#### Get Peer List

**Endpoint:** `GET /{context}/cluster/peers`

**Response:**
```json
{
  "peers": [
    {
      "peer_id": "12D3KooWXXX...",
      "role": "coordinator",
      "address": "/ip4/192.168.1.10/tcp/4001",
      "latency_ms": 15
    }
  ]
}
```

#### Get Logs

**Endpoint:** `GET /{context}/log?date=YYYY-MM-DD&hour=HH`

**Query Parameters:**
- `date`: Date in YYYY-MM-DD format (UTC)
- `hour`: Hour in 24-hour format (00-23)

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-12-04T22:15:30Z",
      "level": "INFO",
      "message": "Query executed successfully",
      "source": "query_engine"
    }
  ]
}
```

#### Get Benchmarks

**Endpoint:** `GET /{context}/benchmarks`

**Requirements:** OptimusDB must be started with `-benchmark` flag

**Response:**
```json
[
  {
    "node_id": "12D3KooWXXX...",
    "cpu_usage": 15.3,
    "memory_usage": 512.5,
    "disk_usage": 2048.7,
    "network_rx": 1024,
    "network_tx": 2048,
    "query_latency_ms": 45,
    "replication_lag_ms": 120
  }
]
```

#### Get Benchmark Data (Command)

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "benchmark",
    "argcnt": 0
  }
}
```

**Response:**
```json
{
  "status": 200,
  "data": {
    "node_id": "12D3KooWXXX...",
    "cpu_usage_percent": 15.3,
    "memory_usage_mb": 512.5,
    "disk_usage_mb": 2048.7,
    "uptime_seconds": 3600,
    "queries_processed": 1250,
    "avg_query_latency_ms": 45
  }
}
```

#### Cache Statistics

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "cachestats",
    "argcnt": 0
  }
}
```

**Response:**
```json
{
  "status": 200,
  "data": {
    "cache_size": 1250,
    "hit_rate": 0.65,
    "miss_rate": 0.35,
    "total_hits": 8125,
    "total_misses": 4375,
    "evictions": 250
  }
}
```

#### Clear Cache

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "clearcache",
    "argcnt": 0
  }
}
```

#### Agent Inventory

**Endpoint:** `POST /{context}/agent/inventory`

**Description:** Returns agent inventory (node resources, datasets, services) and current status (Follower/Coordinator).

---

### 7. SQL Operations

Execute SQL DML operations on the local SQLite database with automatic peer fallback.

#### SQL SELECT

**Endpoint:** `POST /{context}/command`

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "SELECT * FROM products WHERE category = 'Electronics' AND price > 100"
}
```

#### SQL INSERT

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "INSERT INTO products (id, name, category, price, stock) VALUES (101, 'Gaming Laptop', 'Electronics', 1299.99, 15)"
}
```

#### SQL UPDATE

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "UPDATE products SET price = 1199.99, stock = 20 WHERE id = 101"
}
```

#### SQL DELETE

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "DELETE FROM products WHERE stock = 0 AND status = 'discontinued'"
}
```

#### Complex SQL Query

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "SELECT category, COUNT(*) as count, AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price FROM products WHERE stock > 0 GROUP BY category HAVING COUNT(*) > 5 ORDER BY avg_price DESC"
}
```

#### Query Data Catalog

**Request Body:**
```json
{
  "method": {
    "argcnt": 2,
    "cmd": "sqldml"
  },
  "args": ["dummy1", "dummy2"],
  "dstype": "dsswres",
  "sqldml": "SELECT * FROM datacatalog;",
  "graph_traversal": [{}],
  "criteria": []
}
```

#### Insert to Data Catalog

**Request Body:**
```json
{
  "method": {
    "argcnt": 2,
    "cmd": "sqldml"
  },
  "args": ["dummy1", "dummy2"],
  "dstype": "dsswres",
  "sqldml": "INSERT INTO datacatalog (_id, author, metadata_type, component, behaviour, relationships, associated_id, name, description, tags, status, created_by, created_at, updated_at, related_ids, priority, scheduling_info, sla_constraints, ownership_details, audit_trail) VALUES ('123776', 'John Doe', 'Type A', 'Component X', 'Passive', 'Relation A', '456789', 'Sample Name', 'Sample Description', 'tag1,tag2', 'Active', 'Admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'related-123', 'High', 'Scheduled', 'SLA-001', 'Owner-001', 'Audit Trail Info');",
  "graph_traversal": [{}],
  "criteria": []
}
```

#### Query Logging Context

**Request Body:**
```json
{
  "method": {
    "argcnt": 2,
    "cmd": "sqldml"
  },
  "args": ["dummy1", "dummy2"],
  "dstype": "dsswres",
  "sqldml": "SELECT timestamp, level, message, source FROM optimusLogger WHERE date = '2025-12-04' AND hour = 22 ORDER BY timestamp DESC;",
  "graph_traversal": [{}],
  "criteria": []
}
```

#### List All Uploaded Files

**Request Body:**
```json
{
  "method": {
    "cmd": "sqldml",
    "argcnt": 1
  },
  "sqldml": "SELECT id, template_id, filename, filesize_bytes, content_sha256, uploader, source_pod, created_at FROM toscametadata ORDER BY created_at DESC;"
}
```

---

### 8. Event Management System (EMS)

Comprehensive event logging and management system.

#### Get EMS Info

**Endpoint:** `GET /{context}/ems`

**Description:** Get EMS endpoint information and capabilities.

#### Get EMS Logs

**Endpoint:** `GET /{context}/ems/logs`

**Query Parameters:**
- `limit`: Number of logs to return (1-1000)
- `level`: Log level filter (INFO|WARN|ERROR|DEBUG)
- `since_min`: Last N minutes (1-1440)

**Example:**
```
GET /{context}/ems/logs?limit=50&level=ERROR&since_min=60
```

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-12-04T22:30:15Z",
      "level": "ERROR",
      "message": "Connection timeout to peer",
      "source": "network_manager",
      "context": {
        "peer_id": "12D3KooWXXX...",
        "retry_count": 3
      }
    }
  ]
}
```

#### Get EMS Events

**Endpoint:** `GET /{context}/ems/events`

**Query Parameters:**
- `limit`: Number of events to return (1-1000)
- `since_min`: Last N minutes (1-1440)

**Example:**
```
GET /{context}/ems/events?limit=50&since_min=30
```

**Description:** Retrieve events from the `ems_events` table.

#### Execute EMS SQL

**Endpoint:** `GET /{context}/ems/sql`

**Query Parameters:**
- `query`: SQL query to execute on EMS database

**Description:** Execute custom SQL queries against the EMS database.

---

## Query Operators

OptimusDB supports the following query operators for filtering and matching:

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$gte` | Greater than or equal | `{"price": {"$gte": 100}}` |
| `$gt` | Greater than | `{"capacity": {"$gt": 500}}` |
| `$lte` | Less than or equal | `{"price": {"$lte": 1000}}` |
| `$lt` | Less than | `{"stock": {"$lt": 10}}` |
| `$ne` | Not equal | `{"status": {"$ne": "inactive"}}` |

### Pattern Matching

| Operator | Description | Example |
|----------|-------------|---------|
| `$regex` | Regular expression match | `{"name": {"$regex": "^Gaming.*"}}` |

### Combined Example

```json
{
  "criteria": [
    {
      "price": {"$gte": 100, "$lte": 1000},
      "name": {"$regex": "^Gaming.*"},
      "category": "Electronics",
      "stock": {"$gt": 0}
    }
  ]
}
```

---

## Query Strategies

OptimusDB supports multiple query execution strategies to optimize performance based on use case:

### Strategy Types

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `LOCAL_ONLY` | Query local cache only | Fast reads, local data sufficient |
| `REMOTE_ONLY` | Query remote peers only | Testing, verification, exclude local |
| `LOCAL_THEN_REMOTE_MERGE` | Local first, merge remote | Balanced performance |
| `REMOTE_THEN_LOCAL_FALLBACK` | Remote first, local fallback | Prioritize latest distributed data |

### Query Options

```json
{
  "options": {
    "strategy": "LOCAL_THEN_REMOTE_MERGE",
    "consistency": "BEST_EFFORT",
    "include_local": true,
    "annotate_source": true,
    "time_budget_ms": 1500
  }
}
```

**Parameters:**
- `strategy`: Query execution strategy (see table above)
- `consistency`: `BEST_EFFORT` | `EVENTUAL` | `STRONG`
- `include_local`: Include local node in results (default: true)
- `annotate_source`: Add source peer information to results (default: false)
- `time_budget_ms`: Maximum query execution time in milliseconds

---

## Environment Variables

The Postman collection uses the following environment variables:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `base_url` | OptimusDB base URL | `http://localhost:18001` |
| `context` | Environment context | `swarmkb` or `production` |
| `webapp_template_id` | WebApp template ID | Auto-set after upload |
| `capacity_template_id` | Capacity profile template ID | Auto-set after upload |
| `opentofu_template_id` | OpenTofu template ID | Auto-set after upload |
| `deployment_template_id` | Deployment plan template ID | Auto-set after upload |
| `requirements_template_id` | Requirements template ID | Auto-set after upload |
| `dataStore` | Data store type | `dsswres` |
| `timestamp` | Current timestamp | Auto-generated |
| `isoTimestamp` | ISO 8601 timestamp | Auto-generated |
| `uuid` | Unique identifier | Auto-generated |

### Base64 File Variables

For file uploads, prepare the following base64-encoded TOSCA files:

- `webapp_adt_base64`
- `capacity_profile_base64`
- `opentofu_hybrid_base64`
- `deployment_plan_base64`
- `app_requirements_base64`

---

## Response Format

All API responses follow a standard format:

### Success Response

```json
{
  "status": 200,
  "data": {
    // Response data varies by endpoint
  },
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "status": 400,
  "error": "Error description",
  "details": "Additional error details"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Testing Workflow

### Recommended Test Sequence

1. **Upload Phase**
   - Upload all 5 TOSCA templates
   - Verify template IDs are saved

2. **Query Phase**
   - Test simple queries (get all, find by ID)
   - Test complex queries (nested fields, operators)
   - Test distributed queries (different strategies)

3. **CRUD Phase**
   - Insert test documents
   - Query inserted documents
   - Update documents and verify changes
   - Delete documents

4. **Advanced Phase**
   - Test query strategies
   - Test SQL operations
   - Monitor performance with benchmarks
   - Check cache statistics

5. **System Phase**
   - Check cluster health
   - Review logs
   - Monitor EMS events

---

## Best Practices

1. **Always set environment variables** before running queries
2. **Upload TOSCA files first** before attempting queries
3. **Use appropriate query strategies** based on your use case
4. **Monitor cache statistics** to optimize performance
5. **Set reasonable time budgets** for distributed queries
6. **Use annotate_source** when debugging distributed queries
7. **Check cluster status** before running large-scale operations
8. **Review EMS logs** for troubleshooting

---

## Support and Documentation

For additional support and documentation:

- **GitHub Repository**: [OptimusDB Repository]
- **Project Website**: EU Horizon Europe Grant 101135012
- **Issue Tracker**: [Submit Issues]
- **Documentation**: [Full Documentation]

---

## License

This project is part of the EU Horizon Europe Grant 101135012 (Swarmchestrate).

---

**Last Updated:** December 19, 2025  
**Specification Version:** 1.0
