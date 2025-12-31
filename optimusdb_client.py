#!/usr/bin/env python3
"""
OptimusDB Python Client
A comprehensive client for interacting with OptimusDB distributed catalog system.

Features:
- Full CRUD operations (Create, Read, Update, Delete)
- TOSCA file upload support
- Query with filters, regex, operators
- Logging and debugging
- CLI interface
"""

import requests
import json
import logging
import argparse
import os
import sys
import base64
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
from datetime import datetime
import time


class OptimusDBClient:
    """Main client class for OptimusDB operations."""

    def __init__(self,
                 base_url: str = "http://193.225.250.240",
                 context: str = "swarmkb",
                 timeout: int = 30,
                 log_level: str = "INFO"):
        """
        Initialize OptimusDB client.

        Args:
            base_url: Base URL of OptimusDB server
            context: API context path
            timeout: Request timeout in seconds
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.base_url = base_url.rstrip('/')
        self.context = context
        self.timeout = timeout
        self.command_url = f"{self.base_url}/{self.context}/command"
        self.upload_url = f"{self.base_url}/{self.context}/upload"

        # Setup logging
        self.setup_logging(log_level)

        self.logger.info(f"OptimusDB Client initialized")
        self.logger.info(f"Server: {self.base_url}")
        self.logger.info(f"Context: {self.context}")

    def setup_logging(self, log_level: str):
        """Configure logging with colors and formatting."""
        # Create logger
        self.logger = logging.getLogger('OptimusDB')
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))

        # Format with colors
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def _execute_command(self, method: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute a command against OptimusDB.

        Args:
            method: Method dictionary with 'cmd' and 'argcnt'
            **kwargs: Additional parameters (criteria, dstype, args, etc.)

        Returns:
            Response dictionary
        """
        payload = {
            "method": method,
            **kwargs
        }

        self.logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(
                self.command_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )

            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response body: {response.text}")

            response.raise_for_status()
            result = response.json()

            self.logger.info(f"Command '{method['cmd']}' executed successfully")
            return result

        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout after {self.timeout} seconds")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse response JSON: {str(e)}")
            raise

    # ============================================================================
    # CRUD OPERATIONS
    # ============================================================================

    def get(self,
            criteria: Optional[List[Dict[str, Any]]] = None,
            dstype: str = "dsswres") -> Dict[str, Any]:
        """
        Get documents from OptimusDB.

        Args:
            criteria: Query criteria (empty for all documents)
            dstype: Datastore type (dsswres, dsswresaloc, kbmetadata, etc.)

        Returns:
            Response with matching documents

        Examples:
            # Get all documents
            client.get()

            # Get by ID
            client.get(criteria=[{"_id": "12345"}])

            # Get with regex
            client.get(criteria=[{"_id": {"$regex": "^tosca_"}}])

            # Get with nested field
            client.get(criteria=[{"metadata.kb_datastore": "ADT"}])
        """
        if criteria is None:
            criteria = []

        self.logger.info(f"Getting documents from {dstype}")
        if criteria:
            self.logger.debug(f"Criteria: {json.dumps(criteria, indent=2)}")

        result = self._execute_command(
            method={"cmd": "crudget", "argcnt": 1},
            dstype=dstype,
            criteria=criteria
        )

        count = len(result.get('data', [])) if isinstance(result.get('data'), list) else 0
        self.logger.info(f"Retrieved {count} document(s)")

        return result

    def create(self,
               documents: List[Dict[str, Any]],
               dstype: str = "dsswres") -> Dict[str, Any]:
        """
        Create (insert) documents into OptimusDB.

        Args:
            documents: List of documents to insert
            dstype: Datastore type

        Returns:
            Response with operation result

        Example:
            client.create([
                {"name": "Solar Panel A", "capacity": 100},
                {"name": "Wind Turbine B", "capacity": 200}
            ])
        """
        self.logger.info(f"Creating {len(documents)} document(s) in {dstype}")

        result = self._execute_command(
            method={"cmd": "crudput", "argcnt": 1},
            dstype=dstype,
            criteria=documents
        )

        self.logger.info("Documents created successfully")
        return result

    def update(self,
               criteria: List[Dict[str, Any]],
               update_data: List[Dict[str, Any]],
               dstype: str = "dsswres") -> Dict[str, Any]:
        """
        Update documents in OptimusDB.

        Args:
            criteria: Query criteria to match documents
            update_data: Update data to apply
            dstype: Datastore type

        Returns:
            Response with update count

        Example:
            client.update(
                criteria=[{"_id": "12345"}],
                update_data=[{"status": "active", "updated_at": "2025-12-31"}]
            )
        """
        self.logger.info(f"Updating documents in {dstype}")
        self.logger.debug(f"Criteria: {json.dumps(criteria, indent=2)}")
        self.logger.debug(f"Update data: {json.dumps(update_data, indent=2)}")

        result = self._execute_command(
            method={"cmd": "crudupdate", "argcnt": 1},
            criteria=criteria,
            UpdateData=update_data
        )

        self.logger.info("Update completed")
        return result

    def delete(self,
               criteria: List[Dict[str, Any]],
               dstype: str = "dsswres") -> Dict[str, Any]:
        """
        Delete documents from OptimusDB.

        Args:
            criteria: Query criteria to match documents to delete
            dstype: Datastore type

        Returns:
            Response with deletion count

        Examples:
            # Delete by ID
            client.delete(criteria=[{"_id": "12345"}])

            # Delete all with regex
            client.delete(criteria=[{"_id": {"$regex": ".*"}}])

            # Delete with conditions
            client.delete(criteria=[{"status": "inactive"}])
        """
        self.logger.info(f"Deleting documents from {dstype}")
        self.logger.debug(f"Criteria: {json.dumps(criteria, indent=2)}")

        result = self._execute_command(
            method={"cmd": "cruddelete", "argcnt": 1},
            criteria=criteria
        )

        self.logger.info("Delete completed")
        return result

    def delete_all(self, dstype: str = "dsswres") -> Dict[str, Any]:
        """
        Delete ALL documents from a datastore (convenience method).

        Args:
            dstype: Datastore type

        Returns:
            Response with deletion count

        Warning:
            This will delete ALL documents! Use with caution.
        """
        self.logger.warning(f"Deleting ALL documents from {dstype}")
        return self.delete(criteria=[{"_id": {"$regex": ".*"}}], dstype=dstype)

    # ============================================================================
    # QUERY OPERATIONS
    # ============================================================================

    def query(self,
              criteria: List[Dict[str, Any]],
              options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Advanced query with strategy options.

        Args:
            criteria: Query criteria
            options: Query options (strategy, consistency, time_budget_ms, etc.)

        Returns:
            Response with matching documents

        Example:
            client.query(
                criteria=[{"type": "renewable_energy"}],
                options={
                    "strategy": "PARALLEL_MERGE",
                    "time_budget_ms": 2000,
                    "include_local": True
                }
            )
        """
        self.logger.info("Executing advanced query")

        payload = {
            "method": {"cmd": "query", "argcnt": 0},
            "criteria": criteria
        }

        if options:
            payload["options"] = options
            self.logger.debug(f"Query options: {json.dumps(options, indent=2)}")

        result = self._execute_command(**payload)
        return result

    # ============================================================================
    # TOSCA OPERATIONS
    # ============================================================================

    def upload_tosca(self, file_path: str, store_full_structure: bool = True) -> Dict[str, Any]:
        """
        Upload a TOSCA YAML file to OptimusDB.

        Args:
            file_path: Path to TOSCA YAML file
            store_full_structure: If True, creates queryable structured documents.
                                 If False, stores as binary blob (legacy mode).

        Returns:
            Response with upload result

        Example:
            # Upload with full structure (queryable)
            client.upload_tosca("webapp_adt.yaml", store_full_structure=True)

            # Upload as blob (legacy mode)
            client.upload_tosca("webapp_adt.yaml", store_full_structure=False)
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.logger.info(f"Uploading TOSCA file: {file_path}")
        self.logger.info(f"Full structure mode: {store_full_structure}")

        try:
            # Read file
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Validate YAML
            try:
                yaml_data = yaml.safe_load(file_content)
                self.logger.debug(f"YAML validated successfully")
            except yaml.YAMLError as e:
                self.logger.error(f"Invalid YAML: {str(e)}")
                raise

            # Base64 encode the file (matching shell script behavior)
            file_b64 = base64.b64encode(file_content).decode('utf-8')

            # Create JSON payload with base64 file and filename
            payload = {
                "file": file_b64,
                "filename": file_path.name,
                "store_full_structure": store_full_structure
            }

            self.logger.debug(f"Uploading to {self.upload_url}")
            self.logger.debug(f"Filename: {file_path.name}")
            self.logger.debug(f"File size: {len(file_content)} bytes")
            self.logger.debug(f"Base64 size: {len(file_b64)} characters")
            self.logger.debug(f"Store full structure: {store_full_structure}")

            # Send as JSON (not multipart/form-data)
            response = requests.post(
                self.upload_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )

            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response: {response.text}")

            response.raise_for_status()

            # Parse JSON response
            try:
                result = response.json()

                # Extract template_id from various possible locations
                template_id = (
                        result.get('data', {}).get('template_id') or
                        result.get('template_id') or
                        result.get('data', {}).get('templateId') or
                        result.get('templateId')
                )

                if template_id:
                    self.logger.info(f"Template ID: {template_id}")
                    result['template_id'] = template_id
                else:
                    self.logger.warning("No template_id in response")

                # Log storage information
                storage_info = result.get('data', {})
                if storage_info.get('queryable') is False:
                    self.logger.warning("⚠️  File uploaded in LEGACY MODE (not queryable)")
                    self.logger.warning("⚠️  Use store_full_structure=True for queryable documents")
                elif storage_info.get('queryable') is True:
                    self.logger.info("✓ File uploaded with full structure (queryable)")

            except json.JSONDecodeError:
                result = {"status": "success", "message": response.text}

            self.logger.info(f"TOSCA file uploaded successfully: {file_path.name}")
            return result

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Upload failed: {str(e)}")
            raise

    # ============================================================================
    # UTILITY OPERATIONS
    # ============================================================================

    def get_agent_status(self) -> Dict[str, Any]:
        """Get OptimusDB agent status including cluster information."""
        self.logger.info("Getting agent status")

        try:
            response = requests.get(
                f"{self.base_url}/{self.context}/agent/status",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to get status: {str(e)}")
            raise

    def get_peers(self) -> Dict[str, Any]:
        """Get list of discovered peers."""
        self.logger.info("Getting peer list")

        try:
            response = requests.get(
                f"{self.base_url}/{self.context}/peers",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to get peers: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check if OptimusDB server is reachable.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/{self.context}/agent/status",
                timeout=5
            )
            healthy = response.status_code == 200

            if healthy:
                self.logger.info("✓ Server is healthy")
            else:
                self.logger.warning(f"✗ Server returned status {response.status_code}")

            return healthy
        except Exception as e:
            self.logger.error(f"✗ Server unreachable: {str(e)}")
            return False

    # ============================================================================
    # PRETTY PRINTING
    # ============================================================================

    def print_result(self, result: Dict[str, Any], title: str = "Result"):
        """
        Pretty print operation result.

        Args:
            result: Result dictionary to print
            title: Title for the output
        """
        print(f"\n{'='*80}")
        print(f"{title}")
        print(f"{'='*80}")

        # Status
        status = result.get('status', 'unknown')
        print(f"Status: {status}")

        # Data
        data = result.get('data')
        if data is not None:
            if isinstance(data, str):
                print(f"\n{data}")
            elif isinstance(data, list):
                print(f"\nDocuments: {len(data)}")
                if data:
                    print(f"\n{json.dumps(data, indent=2)}")
            else:
                print(f"\n{json.dumps(data, indent=2)}")

        print(f"{'='*80}\n")

    def print_documents(self, documents: List[Dict[str, Any]], max_display: int = 10):
        """
        Pretty print documents list.

        Args:
            documents: List of documents
            max_display: Maximum number of documents to display in full
        """
        count = len(documents)
        print(f"\n{'='*80}")
        print(f"Retrieved {count} document(s)")
        print(f"{'='*80}")

        if count == 0:
            print("No documents found")
            return

        # Show summary
        print("\nDocument IDs:")
        for i, doc in enumerate(documents, 1):
            doc_id = doc.get('_id', 'unknown')
            doc_type = doc.get('document_type', doc.get('type', 'N/A'))
            print(f"  {i}. {doc_id} ({doc_type})")

        # Show full documents (limited)
        if count <= max_display:
            print(f"\nFull documents:")
            print(json.dumps(documents, indent=2))
        else:
            print(f"\nShowing first {max_display} documents:")
            print(json.dumps(documents[:max_display], indent=2))
            print(f"\n... and {count - max_display} more")

        print(f"{'='*80}\n")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='OptimusDB Python Client - Interact with OptimusDB distributed catalog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get all documents
  python optimusdb_client.py get
  
  # Get with criteria
  python optimusdb_client.py get --criteria '_id:tosca_.*:regex'
  
  # Upload TOSCA file
  python optimusdb_client.py upload webapp_adt.yaml
  
  # Delete documents
  python optimusdb_client.py delete --criteria '_id:test_.*:regex'
  
  # Delete all documents (WARNING!)
  python optimusdb_client.py delete-all
  
  # Check server health
  python optimusdb_client.py health
  
  # Get cluster status
  python optimusdb_client.py status
        """
    )

    parser.add_argument('--url', default='http://193.225.250.240',
                        help='OptimusDB base URL (default: http://193.225.250.240)')
    parser.add_argument('--context', default='swarmkb',
                        help='API context (default: swarmkb)')
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Logging level')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # GET command
    get_parser = subparsers.add_parser('get', help='Get documents')
    get_parser.add_argument('--criteria', nargs='+',
                            help='Query criteria in format field:value or field:value:operator')
    get_parser.add_argument('--dstype', default='dsswres',
                            help='Datastore type')

    # CREATE command
    create_parser = subparsers.add_parser('create', help='Create documents')
    create_parser.add_argument('--json', required=True,
                               help='JSON string or file path with documents')
    create_parser.add_argument('--dstype', default='dsswres',
                               help='Datastore type')

    # UPDATE command
    update_parser = subparsers.add_parser('update', help='Update documents')
    update_parser.add_argument('--criteria', nargs='+', required=True,
                               help='Query criteria')
    update_parser.add_argument('--data', required=True,
                               help='Update data as JSON string or file')
    update_parser.add_argument('--dstype', default='dsswres',
                               help='Datastore type')

    # DELETE command
    delete_parser = subparsers.add_parser('delete', help='Delete documents')
    delete_parser.add_argument('--criteria', nargs='+', required=True,
                               help='Query criteria')
    delete_parser.add_argument('--dstype', default='dsswres',
                               help='Datastore type')

    # DELETE ALL command
    delete_all_parser = subparsers.add_parser('delete-all',
                                              help='Delete ALL documents (dangerous!)')
    delete_all_parser.add_argument('--dstype', default='dsswres',
                                   help='Datastore type')
    delete_all_parser.add_argument('--confirm', action='store_true',
                                   help='Skip confirmation prompt')

    # UPLOAD command
    upload_parser = subparsers.add_parser('upload', help='Upload TOSCA file')
    upload_parser.add_argument('file', help='Path to TOSCA YAML file')
    upload_parser.add_argument('--store-full-structure', action='store_true', default=True,
                               help='Store as queryable structured documents (default: True)')
    upload_parser.add_argument('--legacy-mode', action='store_true',
                               help='Store as binary blob (legacy mode, not queryable)')

    # STATUS command
    subparsers.add_parser('status', help='Get agent status')

    # PEERS command
    subparsers.add_parser('peers', help='Get peer list')

    # HEALTH command
    subparsers.add_parser('health', help='Check server health')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize client
    client = OptimusDBClient(
        base_url=args.url,
        context=args.context,
        log_level=args.log_level
    )

    try:
        # Execute command
        if args.command == 'get':
            criteria = parse_criteria(args.criteria) if args.criteria else []
            result = client.get(criteria=criteria, dstype=args.dstype)

            if isinstance(result.get('data'), list):
                client.print_documents(result['data'])
            else:
                client.print_result(result, "GET Result")

        elif args.command == 'create':
            documents = parse_json_arg(args.json)
            if not isinstance(documents, list):
                documents = [documents]
            result = client.create(documents=documents, dstype=args.dstype)
            client.print_result(result, "CREATE Result")

        elif args.command == 'update':
            criteria = parse_criteria(args.criteria)
            update_data = parse_json_arg(args.data)
            if not isinstance(update_data, list):
                update_data = [update_data]
            result = client.update(criteria=criteria, update_data=update_data, dstype=args.dstype)
            client.print_result(result, "UPDATE Result")

        elif args.command == 'delete':
            criteria = parse_criteria(args.criteria)
            result = client.delete(criteria=criteria, dstype=args.dstype)
            client.print_result(result, "DELETE Result")

        elif args.command == 'delete-all':
            if not args.confirm:
                response = input(f"⚠️  Delete ALL documents from {args.dstype}? Type 'yes' to confirm: ")
                if response.lower() != 'yes':
                    print("Cancelled")
                    sys.exit(0)

            result = client.delete_all(dstype=args.dstype)
            client.print_result(result, "DELETE ALL Result")

        elif args.command == 'upload':
            # Determine storage mode
            store_full_structure = not args.legacy_mode if hasattr(args, 'legacy_mode') else True

            result = client.upload_tosca(args.file, store_full_structure=store_full_structure)
            client.print_result(result, "UPLOAD Result")

        elif args.command == 'status':
            result = client.get_agent_status()
            client.print_result(result, "Agent Status")

        elif args.command == 'peers':
            result = client.get_peers()
            client.print_result(result, "Peer List")

        elif args.command == 'health':
            is_healthy = client.health_check()
            sys.exit(0 if is_healthy else 1)

    except Exception as e:
        client.logger.error(f"Command failed: {str(e)}")
        sys.exit(1)


def parse_criteria(criteria_list: List[str]) -> List[Dict[str, Any]]:
    """
    Parse criteria from command line arguments.

    Format: field:value or field:value:operator

    Examples:
        _id:12345                -> [{"_id": "12345"}]
        _id:tosca_.*:regex      -> [{"_id": {"$regex": "tosca_.*"}}]
        capacity:100:gt         -> [{"capacity": {"$gt": 100}}]
    """
    criteria = {}

    for item in criteria_list:
        parts = item.split(':', 2)

        if len(parts) == 2:
            # Simple equality
            field, value = parts
            criteria[field] = value
        elif len(parts) == 3:
            # With operator
            field, value, operator = parts

            # Try to convert to number if possible
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep as string

            criteria[field] = {f"${operator}": value}
        else:
            raise ValueError(f"Invalid criteria format: {item}")

    return [criteria] if criteria else []


def parse_json_arg(json_arg: str) -> Any:
    """Parse JSON argument (either JSON string or file path)."""
    # Check if it's a file
    if os.path.exists(json_arg):
        with open(json_arg, 'r') as f:
            return json.load(f)
    else:
        # Parse as JSON string
        return json.loads(json_arg)


if __name__ == '__main__':
    main()