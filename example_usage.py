#!/usr/bin/env python3
"""
Example usage of OptimusDB Python client.
Demonstrates all major operations including extended metadata.
"""

from optimusdb_client import OptimusDBClient
import json

# ═══════════════════════════════════════════════════════════════════════════════
# Initialize client — pointing to optimusdb1
# ═══════════════════════════════════════════════════════════════════════════════
client = OptimusDBClient(
    base_url="http://193.225.250.240/optimusdb1",
    context="swarmkb",
    log_level="INFO"
)

print("=" * 80)
print("OptimusDB Python Client — Example Usage")
print("=" * 80)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Health Check
# ─────────────────────────────────────────────────────────────────────────────
print("\n1. Health Check")
print("-" * 40)
is_healthy = client.health_check()
if not is_healthy:
    print("Server is not reachable. Exiting.")
    exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Agent Status
# ─────────────────────────────────────────────────────────────────────────────
print("\n2. Get Agent Status")
print("-" * 40)
status = client.get_agent_status()
agent = status.get('agent', {})
print(f"  Role    : {agent.get('role', '?')}")
print(f"  Peer ID : {agent.get('peer_id', '?')[:20]}...")
print(f"  Cluster : {status.get('cluster', {}).get('connected_peers', 0)} peers")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Get All Documents
# ─────────────────────────────────────────────────────────────────────────────
print("\n3. Get All Documents (dsswres)")
print("-" * 40)
all_docs = client.get()
if isinstance(all_docs.get('data'), list):
    print(f"  Total documents: {len(all_docs['data'])}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Create Sample Documents
# ─────────────────────────────────────────────────────────────────────────────
print("\n4. Create Sample Documents")
print("-" * 40)
sample_docs = [
    {
        "name": "Solar Panel Array 1",
        "type": "renewable_energy",
        "capacity": 150,
        "location": "Athens",
        "status": "active",
        "metadata": {
            "installation_date": "2025-01-01",
            "vendor": "SolarTech Inc"
        }
    },
    {
        "name": "Wind Turbine 1",
        "type": "renewable_energy",
        "capacity": 200,
        "location": "Thessaloniki",
        "status": "active",
    },
    {
        "name": "Test Equipment",
        "type": "test",
        "capacity": 50,
        "location": "Lab",
        "status": "testing"
    }
]
create_result = client.create(sample_docs)
client.print_result(create_result, "Create Result")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Query with Regex
# ─────────────────────────────────────────────────────────────────────────────
print("\n5. Query with Regex (name starts with 'Solar')")
print("-" * 40)
regex_result = client.get(criteria=[{"name": {"$regex": "^Solar.*"}}])
if isinstance(regex_result.get('data'), list):
    client.print_documents(regex_result['data'])

# ─────────────────────────────────────────────────────────────────────────────
# 6. Upload TOSCA File
# ─────────────────────────────────────────────────────────────────────────────
print("\n6. Upload TOSCA File (full structure)")
print("-" * 40)
tosca_file = "toscaSamples/webapp_adt.yaml"
try:
    upload_result = client.upload_tosca(
        tosca_file,
        store_full_structure=True,
        target_store="dsswres"
    )
    template_id = upload_result.get('template_id', '')
    print(f"  Template ID: {template_id}")
    print(f"  Queryable  : {upload_result.get('data', {}).get('queryable', '?')}")
except FileNotFoundError:
    print(f"  TOSCA file '{tosca_file}' not found. Skipping.")
    template_id = None

# ─────────────────────────────────────────────────────────────────────────────
# 7. Check Auto-Generated Metadata
# ─────────────────────────────────────────────────────────────────────────────
if template_id:
    print("\n7. Check Auto-Generated Metadata")
    print("-" * 40)
    meta = client.wait_for_metadata(template_id, timeout_seconds=10)
    if meta:
        client.print_metadata_summary(meta)
    else:
        print("  Metadata not yet available (goroutine may still be running)")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Query Metadata with Criteria
# ─────────────────────────────────────────────────────────────────────────────
print("\n8. Query All Metadata Entries")
print("-" * 40)
all_meta = client.get_metadata()
meta_data = all_meta.get('data', [])
entries = meta_data if isinstance(meta_data, list) else [meta_data] if meta_data else []
print(f"  Total metadata entries: {len(entries)}")
for e in entries[:3]:
    print(f"    {e.get('_id', '?')[:30]}  type={e.get('metadata_type', '?')}  status={e.get('status', '?')}")

# ─────────────────────────────────────────────────────────────────────────────
# 9. SQL Query (metadata_catalog)
# ─────────────────────────────────────────────────────────────────────────────
print("\n9. SQL Query — metadata_catalog")
print("-" * 40)
try:
    sql_result = client.execute_sql(
        "SELECT id, name, metadata_type, status, data_domain, node_count "
        "FROM metadata_catalog ORDER BY created_at DESC LIMIT 5"
    )
    records = sql_result.get('records', [])
    print(f"  {len(records)} row(s)")
    for r in records:
        print(f"    {r}")
except Exception as e:
    print(f"  SQL query skipped: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 10. Verify 48-Column Schema
# ─────────────────────────────────────────────────────────────────────────────
print("\n10. Verify 48-Column Schema")
print("-" * 40)
try:
    schema = client.verify_48_columns()
    if schema['ok']:
        print(f"  ✓ All 48 columns present (total: {schema['total']})")
    else:
        print(f"  ✗ Missing: {schema['missing']}")
except Exception as e:
    print(f"  Schema check skipped: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 11. Delete Test Documents
# ─────────────────────────────────────────────────────────────────────────────
print("\n11. Cleanup — Delete Test Documents")
print("-" * 40)
delete_result = client.delete(criteria=[{"type": "test"}])
client.print_result(delete_result, "Delete Result")

# ─────────────────────────────────────────────────────────────────────────────
# 12. Peers
# ─────────────────────────────────────────────────────────────────────────────
print("\n12. Peer Information")
print("-" * 40)
try:
    peers = client.get_peers()
    print(f"  Peers: {len(peers) if isinstance(peers, list) else '?'}")
except Exception:
    print("  Could not retrieve peer information")

print("\n" + "=" * 80)
print("Example completed successfully!")
print("=" * 80)
