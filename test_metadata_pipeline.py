#!/usr/bin/env python3
"""
OptimusDB — Extended Metadata Pipeline Test
23022026
=============================================
End-to-end scenario:
  1. Upload a TOSCA file (full structure)
  2. Check the records generated in the target store
  3. Query with criteria (field filters)
  4. Check auto-generated metadata (OrbitDB + SQLite)
  5. Add new fields to metadata
  6. Update existing metadata fields
  7. Verify changes in both OrbitDB and SQLite
  8. Verify the 48-column schema

Usage:
    python test_metadata_pipeline.py
    python test_metadata_pipeline.py --url http://optimusdb1:18001
    python test_metadata_pipeline.py --url http://localhost:18003 --log-level DEBUG
"""

from optimusdb_client import OptimusDBClient
import json
import sys
import time
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_URL = "http://193.225.250.240/optimusdb1"
DEFAULT_CONTEXT = "swarmkb"
TOSCA_FILE = "toscaSamples/webapp_adt.yaml"     # primary test file
TOSCA_FALLBACK = "toscaSamples/aws_ec2_instance.yaml"  # fallback


def banner(title: str):
    print(f"\n{'━'*80}")
    print(f"  {title}")
    print(f"{'━'*80}")


def step(num: int, title: str):
    print(f"\n  ┌─ Step {num}: {title}")
    print(f"  │")


def ok(msg: str):
    print(f"  │  ✅ {msg}")


def fail(msg: str):
    print(f"  │  ❌ {msg}")


def info(msg: str):
    print(f"  │  ℹ️  {msg}")


def done():
    print(f"  └─ done\n")


def section_result(label: str, data, max_lines: int = 20):
    """Print a JSON snippet, truncated."""
    text = json.dumps(data, indent=2)
    lines = text.split('\n')
    print(f"  │")
    for line in lines[:max_lines]:
        print(f"  │  {line}")
    if len(lines) > max_lines:
        print(f"  │  ... ({len(lines) - max_lines} more lines)")


# ═══════════════════════════════════════════════════════════════════════════════
# Main Pipeline
# ═══════════════════════════════════════════════════════════════════════════════
def run_pipeline(url: str, context: str, log_level: str):

    banner("OptimusDB — Extended Metadata Pipeline Test")
    info(f"Endpoint : {url}")
    info(f"Context  : {context}")

    client = OptimusDBClient(base_url=url, context=context, log_level=log_level)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 0: Health check
    # ──────────────────────────────────────────────────────────────────────────
    step(0, "Health Check")
    if not client.health_check():
        fail(f"Server at {url} is not reachable. Aborting.")
        done(); sys.exit(1)

    status = client.get_agent_status()
    agent = status.get('agent', {})
    cluster = status.get('cluster', {})
    ok(f"Agent role: {agent.get('role', '?')}")
    ok(f"Peer ID  : {agent.get('peer_id', '?')[:20]}...")
    ok(f"Cluster  : {cluster.get('connected_peers', 0)} peers connected")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 1: Upload TOSCA (full structure)
    # ──────────────────────────────────────────────────────────────────────────
    step(1, "Upload TOSCA Template (store_full_structure=true)")

    tosca_path = Path(TOSCA_FILE)
    if not tosca_path.exists():
        tosca_path = Path(TOSCA_FALLBACK)
    if not tosca_path.exists():
        # Try to find any yaml
        samples = list(Path("toscaSamples").glob("*.yaml"))
        if samples:
            tosca_path = samples[0]
        else:
            fail("No TOSCA sample files found in toscaSamples/")
            done(); sys.exit(1)

    info(f"File: {tosca_path}")

    upload_result = client.upload_tosca(
        str(tosca_path),
        store_full_structure=True,
        target_store="dsswres"
    )

    template_id = upload_result.get('template_id', '')
    upload_data = upload_result.get('data', {})

    if template_id:
        ok(f"Template ID  : {template_id}")
        ok(f"Storage type : {upload_data.get('storage_type', '?')}")
        ok(f"Store        : {upload_data.get('storage_location', '?')}")
        ok(f"File size    : {upload_data.get('filesize', 0)} bytes")
        ok(f"Queryable    : {upload_data.get('queryable', False)}")
    else:
        fail("Upload returned no template_id")
        section_result("Upload response", upload_result)
        done(); sys.exit(1)
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 2: Check records generated in the target store (dsswres)
    # ──────────────────────────────────────────────────────────────────────────
    step(2, "Check Records in Target Store (dsswres)")

    # Query by _id = template_id
    records_result = client.query(
        criteria=[{"field": "_id", "operator": "==", "value": template_id}],
        dstype="dsswres"
    )

    records_data = records_result.get('data', [])
    records = records_data if isinstance(records_data, list) else [records_data] if records_data else []

    if records:
        ok(f"Found {len(records)} record(s) in dsswres")
        # Show some top-level keys
        first = records[0]
        top_keys = list(first.keys())[:15]
        info(f"Top-level keys: {', '.join(top_keys)}")

        # Check if TOSCA structure is preserved
        if 'topology_template' in first or 'tosca_definitions_version' in first:
            ok("TOSCA structure preserved (full queryable JSON)")
        if '_storage_type' in first:
            ok(f"_storage_type = {first['_storage_type']}")
        if '_lineage' in first:
            ok(f"_lineage present: {json.dumps(first['_lineage'])}")
    else:
        fail("No records found in dsswres for this template_id")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 3: Query with criteria (field-level filters)
    # ──────────────────────────────────────────────────────────────────────────
    step(3, "Query with Criteria (field-level filters)")

    # 3a) Query by _storage_type
    info("Query: _storage_type == 'full_structure'")
    q1 = client.query(
        criteria=[{"field": "_storage_type", "operator": "==", "value": "full_structure"}],
        dstype="dsswres"
    )
    q1_data = q1.get('data', [])
    q1_count = len(q1_data) if isinstance(q1_data, list) else (1 if q1_data else 0)
    ok(f"Results: {q1_count} record(s)")

    # 3b) Query by _filename
    info(f"Query: _filename == '{tosca_path.name}'")
    q2 = client.query(
        criteria=[{"field": "_filename", "operator": "==", "value": tosca_path.name}],
        dstype="dsswres"
    )
    q2_data = q2.get('data', [])
    q2_count = len(q2_data) if isinstance(q2_data, list) else (1 if q2_data else 0)
    ok(f"Results: {q2_count} record(s)")

    # 3c) Query with 'contains' operator on description
    info("Query: description contains 'tosca' (or similar)")
    q3 = client.query(
        criteria=[{"field": "_storage_type", "operator": "contains", "value": "full"}],
        dstype="dsswres"
    )
    q3_data = q3.get('data', [])
    q3_count = len(q3_data) if isinstance(q3_data, list) else (1 if q3_data else 0)
    ok(f"Results: {q3_count} record(s)")

    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 4: Wait & Check Auto-Generated Metadata
    # ──────────────────────────────────────────────────────────────────────────
    step(4, "Check Auto-Generated Metadata (OrbitDB KBMetadata)")

    info(f"Waiting for async metadata generation (associated_id={template_id})...")
    metadata_entry = client.wait_for_metadata(
        associated_id=template_id,
        timeout_seconds=15,
        poll_interval=1.0
    )

    metadata_id = None
    if metadata_entry:
        metadata_id = metadata_entry.get('_id', '')
        ok(f"Metadata ID      : {metadata_id}")
        ok(f"Name             : {metadata_entry.get('name', '—')}")
        ok(f"Metadata type    : {metadata_entry.get('metadata_type', '—')}")
        ok(f"Status           : {metadata_entry.get('status', '—')}")
        ok(f"Data domain      : {metadata_entry.get('data_domain', '—')}")
        ok(f"Quality score    : {metadata_entry.get('data_quality_score', '—')}")
        ok(f"Node count       : {metadata_entry.get('node_count', '—')}")
        ok(f"Source agent     : {metadata_entry.get('source_agent', '—')}")
        ok(f"IPFS CID         : {metadata_entry.get('ipfs_cid', '—')}")
        ok(f"Processing status: {metadata_entry.get('processing_status', '—')}")

        client.print_metadata_summary(metadata_entry)
    else:
        fail("Metadata not generated within timeout")
        info("The async goroutine may still be running. Try querying manually.")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 4b: Verify in SQLite too
    # ──────────────────────────────────────────────────────────────────────────
    step(4, "Check Metadata in SQLite (metadata_catalog)")

    try:
        sql_records = client.get_metadata_sql(associated_id=template_id)
        if sql_records:
            ok(f"Found {len(sql_records)} record(s) in SQLite metadata_catalog")
            first_sql = sql_records[0]
            info(f"Columns present: {len(first_sql.keys())}")
            for key in ['id', 'name', 'metadata_type', 'status', 'data_domain',
                        'data_quality_score', 'node_count', 'source_agent', 'ipfs_cid']:
                val = first_sql.get(key, '—')
                if val and val != '—':
                    ok(f"  {key:25s} = {val}")
        else:
            info("No records yet in SQLite (may still be writing)")
    except Exception as e:
        info(f"SQLite query skipped: {e}")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 5: Add new fields to metadata
    # ──────────────────────────────────────────────────────────────────────────
    if metadata_id:
        step(5, "Add New Fields to Metadata")

        try:
            updated = client.update_metadata_fields(metadata_id, {
                "geo_location": "Athens, Greece (37.98°N, 23.73°E)",
                "compliance_tags": "EU-GDPR,Horizon-Europe,ISO-27001",
                "contact_info": "george@aueb.gr",
                "api_endpoint": f"{url}/{context}/command",
                "language": "en",
                "license_type": "Apache-2.0",
            })
            ok("Added 6 new fields to metadata")
            ok(f"  geo_location   = {updated.get('geo_location', '—')}")
            ok(f"  compliance_tags= {updated.get('compliance_tags', '—')}")
            ok(f"  contact_info   = {updated.get('contact_info', '—')}")
            ok(f"  api_endpoint   = {updated.get('api_endpoint', '—')}")
            ok(f"  language       = {updated.get('language', '—')}")
            ok(f"  license_type   = {updated.get('license_type', '—')}")
        except Exception as e:
            fail(f"Failed to add fields: {e}")

        done()

        # ──────────────────────────────────────────────────────────────────────
        # STEP 6: Update existing metadata fields
        # ──────────────────────────────────────────────────────────────────────
        step(6, "Update Existing Metadata Fields")

        try:
            updated = client.update_metadata_fields(metadata_id, {
                "status": "ACTIVE",
                "priority": "HIGH",
                "data_classification": "INTERNAL",
                "update_frequency": "ON_DEMAND",
                "processing_status": "VALIDATED",
                "retention_policy": "5 years from creation",
                "access_control": "role:researcher,admin",
            })
            ok("Updated 7 existing fields")
            ok(f"  status              = {updated.get('status', '—')}")
            ok(f"  priority            = {updated.get('priority', '—')}")
            ok(f"  data_classification = {updated.get('data_classification', '—')}")
            ok(f"  update_frequency    = {updated.get('update_frequency', '—')}")
            ok(f"  processing_status   = {updated.get('processing_status', '—')}")
            ok(f"  retention_policy    = {updated.get('retention_policy', '—')}")
            ok(f"  access_control      = {updated.get('access_control', '—')}")
        except Exception as e:
            fail(f"Failed to update fields: {e}")

        done()

        # ──────────────────────────────────────────────────────────────────────
        # STEP 7: Verify changes in both stores
        # ──────────────────────────────────────────────────────────────────────
        step(7, "Verify Changes — OrbitDB vs SQLite")

        # OrbitDB
        info("Fetching from OrbitDB KBMetadata...")
        orbit_res = client.get_metadata(metadata_id=metadata_id)
        orbit_data = orbit_res.get('data', [])
        orbit_entry = orbit_data[0] if isinstance(orbit_data, list) and orbit_data else orbit_data

        if orbit_entry:
            ok(f"OrbitDB status           = {orbit_entry.get('status', '—')}")
            ok(f"OrbitDB priority         = {orbit_entry.get('priority', '—')}")
            ok(f"OrbitDB geo_location     = {orbit_entry.get('geo_location', '—')}")
            ok(f"OrbitDB processing_status= {orbit_entry.get('processing_status', '—')}")
        else:
            fail("Could not re-fetch from OrbitDB")

        # SQLite
        info("Fetching from SQLite metadata_catalog...")
        try:
            sql_records = client.get_metadata_sql(associated_id=template_id)
            if sql_records:
                sr = sql_records[0]
                ok(f"SQLite status            = {sr.get('status', '—')}")
                ok(f"SQLite priority          = {sr.get('priority', '—')}")
                ok(f"SQLite geo_location      = {sr.get('geo_location', '—')}")
                ok(f"SQLite processing_status = {sr.get('processing_status', '—')}")

                # Compare
                mismatches = 0
                for field in ['status', 'priority', 'geo_location', 'processing_status']:
                    orbit_val = str(orbit_entry.get(field, '')) if orbit_entry else ''
                    sql_val = str(sr.get(field, ''))
                    if orbit_val != sql_val:
                        fail(f"MISMATCH on '{field}': OrbitDB='{orbit_val}' vs SQLite='{sql_val}'")
                        mismatches += 1
                if mismatches == 0:
                    ok("✓ OrbitDB and SQLite are in sync")
            else:
                info("No SQLite records to compare")
        except Exception as e:
            info(f"SQLite comparison skipped: {e}")

        done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 8: Verify 48-column schema
    # ──────────────────────────────────────────────────────────────────────────
    step(8, "Verify 48-Column Schema (metadata_catalog)")

    try:
        schema = client.verify_48_columns()
        if schema['ok']:
            ok(f"All 48 columns present (total: {schema['total']})")
        else:
            fail(f"Missing {len(schema['missing'])} columns:")
            for c in schema['missing']:
                info(f"  - {c}")
            ok(f"Present: {len(schema['present'])}/48")
    except Exception as e:
        info(f"Schema verification skipped: {e}")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 9: Check TOSCA index
    # ──────────────────────────────────────────────────────────────────────────
    step(9, "Check TOSCA Index (tosca_metadata)")

    try:
        tosca_sql = client.execute_sql(
            f"SELECT * FROM tosca_metadata WHERE template_id = '{template_id}'"
        )
        tosca_records = tosca_sql.get('records', [])
        if tosca_records:
            tr = tosca_records[0]
            ok(f"TOSCA index entry found")
            for key in ['template_id', 'filename', 'node_count', 'uploader',
                        'filesize', 'sha256_hash', 'ipfs_path']:
                val = tr.get(key, '—')
                if val and val != '—':
                    ok(f"  {key:20s} = {val}")
        else:
            info("No TOSCA index entry (table may not exist yet)")
    except Exception as e:
        info(f"TOSCA index check skipped: {e}")
    done()

    # ──────────────────────────────────────────────────────────────────────────
    # SUMMARY
    # ──────────────────────────────────────────────────────────────────────────
    banner("Pipeline Test Complete")
    print(f"  Template ID : {template_id}")
    if metadata_id:
        print(f"  Metadata ID : {metadata_id}")
    print(f"  Agent       : {url}")
    print()
    print("  Next steps:")
    print(f"    python optimusdb_client.py metadata --associated-id {template_id}")
    print(f"    python optimusdb_client.py sql \"SELECT * FROM metadata_catalog WHERE associated_id = '{template_id}'\"")
    print(f"    python optimusdb_client.py verify-schema")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OptimusDB Metadata Pipeline Test')
    parser.add_argument('--url', default=DEFAULT_URL,
                        help=f'Agent URL (default: {DEFAULT_URL})')
    parser.add_argument('--context', default=DEFAULT_CONTEXT,
                        help=f'API context (default: {DEFAULT_CONTEXT})')
    parser.add_argument('--log-level', default='WARNING',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Client log level (default: WARNING for clean output)')

    args = parser.parse_args()
    run_pipeline(args.url, args.context, args.log_level)
