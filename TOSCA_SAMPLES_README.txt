================================================================================
TOSCA SAMPLE FILES FOR OPTIMUSDB TESTING
================================================================================

Total Files: 55 TOSCA Templates
Format: YAML (TOSCA Simple Profile YAML 1.3)
Purpose: Testing OptimusDB bulk upload, replication, and query capabilities

================================================================================
FILE CATEGORIES
================================================================================

WEB APPLICATIONS (4 files):
  - web_app_wordpress.yaml       : WordPress with MySQL
  - web_app_nodejs.yaml          : Node.js Express with MongoDB
  - web_app_django.yaml          : Django with PostgreSQL
  - web_app_react_spa.yaml       : React SPA with FastAPI backend

MICROSERVICES (7 files):
  - microservice_order_service.yaml         : Go-based order API
  - microservice_user_service.yaml          : Spring Boot authentication
  - microservice_payment_service.yaml       : FastAPI payment processor
  - microservice_notification_service.yaml  : Node.js with Kafka
  - microservice_analytics_service.yaml     : Scala Akka analytics
  - microservice_inventory_service.yaml     : Rust inventory management
  - (additional microservices...)

CONTAINERS & KUBERNETES (10 files):
  - container_nginx_deployment.yaml
  - k8s_deployment_webapp.yaml
  - k8s_statefulset_database.yaml
  - k8s_daemonset_monitoring.yaml
  - k8s_cronjob_backup.yaml
  - k8s_ingress_routing.yaml
  - k8s_configmap_settings.yaml
  - k8s_secret_credentials.yaml
  - k8s_persistentvolume_storage.yaml
  - k8s_hpa_autoscaling.yaml

CLOUD INFRASTRUCTURE (10 files):
  AWS:
    - aws_ec2_instance.yaml
    - aws_rds_database.yaml
    - aws_s3_bucket.yaml
    - aws_lambda_function.yaml
  
  Azure:
    - azure_vm_instance.yaml
    - azure_sql_database.yaml
    - azure_storage_account.yaml
  
  GCP:
    - gcp_compute_instance.yaml
    - gcp_cloud_sql.yaml
    - gcp_cloud_storage.yaml

IOT & EDGE COMPUTING (10 files):
  - iot_sensor_network.yaml
  - iot_smart_home.yaml
  - iot_industrial_monitoring.yaml
  - edge_video_analytics.yaml
  - edge_5g_deployment.yaml
  - edge_cdn_cache.yaml
  - edge_ar_application.yaml
  - (additional IoT/Edge templates...)

AI/ML (3 files):
  - ml_training_cluster.yaml       : PyTorch training on GPU cluster
  - ml_inference_service.yaml      : BERT inference service
  - ai_chatbot_deployment.yaml     : GPT-4 chatbot with vector DB

MONITORING (3 files):
  - monitoring_prometheus_stack.yaml
  - monitoring_elk_stack.yaml
  - monitoring_apm_service.yaml

SECURITY (3 files):
  - security_waf_deployment.yaml
  - security_ids_deployment.yaml
  - security_vault_secrets.yaml

DATABASES (5 files):
  - database_cassandra_cluster.yaml
  - database_timeseries_influxdb.yaml
  - database_graph_neo4j.yaml
  - database_redis_cluster.yaml
  - database_cockroachdb.yaml

MESSAGE QUEUES (2 files):
  - message_queue_kafka_cluster.yaml
  - message_queue_rabbitmq.yaml

CI/CD (2 files):
  - cicd_jenkins_pipeline.yaml
  - cicd_gitlab_runner.yaml

================================================================================
USAGE INSTRUCTIONS
================================================================================

1. EXTRACT THE ZIP FILE:
   unzip tosca_samples_55_files.zip
   cd tosca_samples

2. UPLOAD TO OPTIMUSDB (All 55 files):
   cd /opt/iccs/Scripts/Demo/HACKATHON/optimusPy
   python3 batch_operations.py bulk-upload /path/to/tosca_samples/

3. UPLOAD SPECIFIC CATEGORY:
   # Just Kubernetes files
   python3 batch_operations.py bulk-upload /path/to/tosca_samples/k8s_*.yaml
   
   # Just cloud infrastructure
   python3 batch_operations.py bulk-upload /path/to/tosca_samples/{aws,azure,gcp}_*.yaml

4. VERIFY UPLOAD:
   # Count total documents
   python3 optimusdb_client.py get | jq '.response | length'
   
   # Expected: 55 (if all uploaded)

5. QUERY BY TYPE:
   # Find all Kubernetes deployments
   python3 optimusdb_client.py get --criteria '{"type": {"$contains": "Kubernetes"}}'
   
   # Find all cloud resources
   python3 optimusdb_client.py get --criteria '{"type": {"$regex": "AWS|Azure|GCP"}}'

================================================================================
FILE CHARACTERISTICS
================================================================================

- All files are valid TOSCA YAML 1.3 format
- Diverse complexity levels (simple → complex)
- Realistic property values and configurations
- Include relationships, requirements, capabilities
- Cover multiple infrastructure types
- Suitable for testing:
  * Bulk uploads
  * Replication across nodes
  * Query performance
  * Nested JSON queries
  * Metadata extraction
  * Full-text search

================================================================================
TESTING SCENARIOS
================================================================================

SCENARIO 1: Cluster Replication Test
  1. Upload all 55 files to optimusdb1
  2. Check optimusdb1: should have 55 docs
  3. Check optimusdb2: should have 55 docs (after sync)
  4. Check optimusdb3: should have 55 docs (after sync)

SCENARIO 2: Query Performance Test
  1. Upload all 55 files
  2. Query by nested paths (e.g., properties.version)
  3. Query with operators ($gte, $regex, $contains)
  4. Measure response time

SCENARIO 3: Metadata Enrichment Test
  1. Upload all 55 files
  2. Check KBMetadata store for auto-generated metadata
  3. Verify lineage relationships

SCENARIO 4: Delete and Update Operations
  1. Upload all 55 files
  2. Delete 10 random files
  3. Update 10 random files
  4. Verify counts: 45 docs total, 10 modified

================================================================================
TEMPLATE STRUCTURE EXAMPLES
================================================================================

SIMPLE TEMPLATE (AWS EC2):
  - 1 compute node
  - Basic properties
  - ~15 lines

MEDIUM TEMPLATE (Web App):
  - 3-4 nodes
  - Requirements/relationships
  - ~50 lines

COMPLEX TEMPLATE (ELK Stack):
  - 5+ nodes
  - Multiple relationships
  - Advanced configurations
  - ~100+ lines

================================================================================
EXPECTED BEHAVIOR IN OPTIMUSDB
================================================================================

After uploading all 55 files:

1. DsSWres store should contain:
   - 55 TOSCA template documents
   - Each with _id, template_name, type, properties
   - Each with _created_at timestamp

2. KBMetadata store should contain:
   - 55 metadata records (one per template)
   - Auto-generated descriptions (if TinyLlama enabled)
   - Searchable fields extracted

3. All nodes should show:
   - Identical document counts (55)
   - Same _id values
   - Consistent query results

================================================================================
TROUBLESHOOTING
================================================================================

If upload count is less than 55:
  1. Check logs for insertion errors
  2. Verify retry logic is working
  3. Check forceIndexRebuild() is called
  4. Verify cluster-wide sync signals

If nodes show different counts:
  1. Apply cluster sync fix (broadcastSyncSignal)
  2. Check libp2p peer connectivity
  3. Verify OrbitDB replication is working

If queries return incomplete results:
  1. Force Load() on all nodes
  2. Check index rebuild status
  3. Verify GossipSub is propagating entries

================================================================================
SUPPORT
================================================================================

These templates are designed to thoroughly test OptimusDB's:
- PutAll bug fixes
- Cluster replication
- Index synchronization
- Query capabilities
- Metadata extraction
- Full-stack TOSCA support

For issues or questions, check OptimusDB logs and verify all fixes are deployed.

================================================================================
