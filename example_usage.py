#!/usr/bin/env python3
"""
Example usage of OptimusDB Python client.
Demonstrates all major operations.
"""

from optimusdb_client import OptimusDBClient
import json

# Initialize client
client = OptimusDBClient(
    base_url="http://193.225.250.240",
    context="swarmkb",
    log_level="INFO"
)

print("="*80)
print("OptimusDB Python Client - Example Usage")
print("="*80)

# 1. Health Check
print("\n1. Health Check")
print("-" * 40)
is_healthy = client.health_check()

if not is_healthy:
    print("Server is not reachable. Exiting.")
    exit(1)

# 2. Get Agent Status
print("\n2. Get Agent Status")
print("-" * 40)
status = client.get_agent_status()
client.print_result(status, "Agent Status")

# 3. Get All Documents
print("\n3. Get All Documents")
print("-" * 40)
all_docs = client.get()
if isinstance(all_docs.get('data'), list):
    client.print_documents(all_docs['data'])

# 4. Create Sample Documents
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
        "metadata": {
            "installation_date": "2025-02-01",
            "vendor": "WindPower Ltd"
        }
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

# 5. Query with Regex
print("\n5. Query with Regex Pattern")
print("-" * 40)
regex_result = client.get(criteria=[{"name": {"$regex": "^Solar.*"}}])
if isinstance(regex_result.get('data'), list):
    client.print_documents(regex_result['data'])

# 6. Query with Numeric Filter
print("\n6. Query with Numeric Filter (capacity > 100)")
print("-" * 40)
numeric_result = client.get(criteria=[{"capacity": {"$gt": 100}}])
if isinstance(numeric_result.get('data'), list):
    client.print_documents(numeric_result['data'])

# 7. Query Nested Fields
print("\n7. Query Nested Fields")
print("-" * 40)
nested_result = client.get(criteria=[{"metadata.vendor": "SolarTech Inc"}])
if isinstance(nested_result.get('data'), list):
    client.print_documents(nested_result['data'])

# 8. Update Documents
print("\n8. Update Document Status")
print("-" * 40)
update_result = client.update(
    criteria=[{"type": "test"}],
    update_data=[{"status": "completed", "test_date": "2025-12-31"}]
)
client.print_result(update_result, "Update Result")

# 9. Verify Update
print("\n9. Verify Update")
print("-" * 40)
verify_result = client.get(criteria=[{"type": "test"}])
if isinstance(verify_result.get('data'), list):
    client.print_documents(verify_result['data'])

# 10. Delete Test Documents
print("\n10. Delete Test Documents")
print("-" * 40)
delete_result = client.delete(criteria=[{"type": "test"}])
client.print_result(delete_result, "Delete Result")

# 11. Upload TOSCA File (if exists)
print("\n11. Upload TOSCA File (Example)")
print("-" * 40)
tosca_file = "toscaSamples/webapp_adt.yaml"
try:
    upload_result = client.upload_tosca(tosca_file)
    client.print_result(upload_result, "Upload Result")
except FileNotFoundError:
    print(f"TOSCA file '{tosca_file}' not found. Skipping upload example.")

# 12. Advanced Query with Logical Operators
print("\n12. Advanced Query with Logical Operators")
print("-" * 40)
advanced_result = client.get(criteria=[{
    "$and": [
        {"type": "renewable_energy"},
        {"capacity": {"$gt": 100}}
    ]
}])
if isinstance(advanced_result.get('data'), list):
    client.print_documents(advanced_result['data'])

# 13. Get Peer Information
print("\n13. Get Peer Information")
print("-" * 40)
try:
    peers = client.get_peers()
    client.print_result(peers, "Discovered Peers")
except:
    print("Could not retrieve peer information")



# 14. Final Document Count
print("\n14. Final Document Count")
print("-" * 40)
final_docs = client.get()
count = len(final_docs.get('data', []))
print(f"\nTotal documents in database: {count}")

print("\n" + "="*80)
print("Example completed successfully!")
print("="*80)