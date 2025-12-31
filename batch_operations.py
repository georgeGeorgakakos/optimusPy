#!/usr/bin/env python3
"""
Batch operations helper for OptimusDB.
Useful for bulk uploads, cleanup, and data migration.
"""

from optimusdb_client import OptimusDBClient
import json
import os
from pathlib import Path
import sys

def bulk_upload_tosca(directory: str, client: OptimusDBClient):
    """Upload all TOSCA files from a directory."""
    tosca_dir = Path(directory)

    if not tosca_dir.exists():
        print(f"Directory not found: {directory}")
        return

    # Find all YAML files
    yaml_files = list(tosca_dir.glob("*.yaml")) + list(tosca_dir.glob("*.yml"))

    if not yaml_files:
        print(f"No YAML files found in {directory}")
        return

    print(f"Found {len(yaml_files)} YAML file(s)")
    print("=" * 80)

    successful = 0
    failed = 0

    for yaml_file in yaml_files:
        print(f"\nUploading: {yaml_file.name}")
        try:
            result = client.upload_tosca(str(yaml_file))
            print(f"✓ Success: {yaml_file.name}")
            successful += 1
        except Exception as e:
            print(f"✗ Failed: {yaml_file.name} - {str(e)}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"Upload Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(yaml_files)}")
    print("=" * 80)

def export_to_json(output_file: str, client: OptimusDBClient, dstype: str = "dsswres"):
    """Export all documents to a JSON file."""
    print(f"Exporting documents from {dstype} to {output_file}")

    result = client.get(dstype=dstype)
    documents = result.get('data', [])

    if not documents:
        print("No documents to export")
        return

    # Write to file
    with open(output_file, 'w') as f:
        json.dump(documents, f, indent=2)

    print(f"✓ Exported {len(documents)} document(s) to {output_file}")

def import_from_json(input_file: str, client: OptimusDBClient, dstype: str = "dsswres"):
    """Import documents from a JSON file."""
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    print(f"Importing documents from {input_file}")

    with open(input_file, 'r') as f:
        documents = json.load(f)

    if not isinstance(documents, list):
        documents = [documents]

    print(f"Found {len(documents)} document(s) to import")

    # Import in batches
    batch_size = 100
    total = len(documents)

    for i in range(0, total, batch_size):
        batch = documents[i:i+batch_size]
        print(f"Importing batch {i//batch_size + 1} ({len(batch)} documents)...")

        try:
            result = client.create(documents=batch, dstype=dstype)
            print(f"✓ Batch imported successfully")
        except Exception as e:
            print(f"✗ Batch failed: {str(e)}")

    print(f"✓ Import completed: {total} document(s)")

def cleanup_by_pattern(pattern: str, client: OptimusDBClient, dstype: str = "dsswres"):
    """Delete documents matching a pattern."""
    print(f"Searching for documents matching pattern: {pattern}")

    # Query first
    result = client.get(criteria=[{"_id": {"$regex": pattern}}], dstype=dstype)
    documents = result.get('data', [])

    if not documents:
        print("No documents match the pattern")
        return

    print(f"Found {len(documents)} document(s) to delete:")
    for doc in documents[:10]:  # Show first 10
        print(f"  - {doc.get('_id', 'unknown')}")

    if len(documents) > 10:
        print(f"  ... and {len(documents) - 10} more")

    # Confirm
    response = input(f"\nDelete {len(documents)} document(s)? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled")
        return

    # Delete
    delete_result = client.delete(criteria=[{"_id": {"$regex": pattern}}], dstype=dstype)
    client.print_result(delete_result, "Cleanup Result")

def main():
    """Main entry point for batch operations."""
    import argparse

    parser = argparse.ArgumentParser(description='OptimusDB Batch Operations')
    parser.add_argument('--url', default='http://localhost:8080',
                        help='OptimusDB base URL')
    parser.add_argument('--context', default='optimusdb',
                        help='API context')

    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # Bulk upload
    upload_parser = subparsers.add_parser('bulk-upload', help='Upload all TOSCA files from directory')
    upload_parser.add_argument('directory', help='Directory containing TOSCA files')

    # Export
    export_parser = subparsers.add_parser('export', help='Export documents to JSON')
    export_parser.add_argument('output', help='Output JSON file')
    export_parser.add_argument('--dstype', default='dsswres', help='Datastore type')

    # Import
    import_parser = subparsers.add_parser('import', help='Import documents from JSON')
    import_parser.add_argument('input', help='Input JSON file')
    import_parser.add_argument('--dstype', default='dsswres', help='Datastore type')

    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Delete documents by pattern')
    cleanup_parser.add_argument('pattern', help='Regex pattern for _id')
    cleanup_parser.add_argument('--dstype', default='dsswres', help='Datastore type')

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        sys.exit(1)

    # Initialize client
    client = OptimusDBClient(base_url=args.url, context=args.context, log_level='INFO')

    # Health check
    if not client.health_check():
        print("Server is not reachable. Exiting.")
        sys.exit(1)

    # Execute operation
    if args.operation == 'bulk-upload':
        bulk_upload_tosca(args.directory, client)
    elif args.operation == 'export':
        export_to_json(args.output, client, args.dstype)
    elif args.operation == 'import':
        import_from_json(args.input, client, args.dstype)
    elif args.operation == 'cleanup':
        cleanup_by_pattern(args.pattern, client, args.dstype)

if __name__ == '__main__':
    main()