#!/usr/bin/env bash
###############################################################################
#  OptimusDB Extended Metadata Tester
#  -----------------------------------
#  Interactive shell for testing the 48-field metadata system.
#
#  Usage:
#    chmod +x test_metadata.sh
#    ./test_metadata.sh                    # default: localhost:18001
#    ./test_metadata.sh localhost:18003    # target a specific agent
#
#  Requires: curl, jq, base64
###############################################################################
set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; B='\033[0;34m'
C='\033[0;36m'; M='\033[0;35m'; W='\033[1;37m'; D='\033[0;90m'; N='\033[0m'

# ── Config ───────────────────────────────────────────────────────────────────
AGENT="${1:-localhost:18001}"
CTX="optimusdb"
BASE="http://${AGENT}/${CTX}"
LAST_TEMPLATE_ID=""
LAST_META_ID=""

# ── Helpers ──────────────────────────────────────────────────────────────────
hr()    { printf "${D}%.0s─${N}" {1..72}; echo; }
hdr()   { hr; printf "  ${Y}%s${N}\n" "$1"; hr; }
ok()    { printf "  ${G}✓${N} %s\n" "$1"; }
fail()  { printf "  ${R}✗${N} %s\n" "$1"; }
info()  { printf "  ${C}ℹ${N} %s\n" "$1"; }
warn()  { printf "  ${Y}⚠${N} %s\n" "$1"; }
dim()   { printf "  ${D}%s${N}\n" "$1"; }
bold()  { printf "  ${W}%s${N}\n" "$1"; }

# POST JSON helper — returns body, sets $HTTP_CODE
post() {
  local url="$1" body="$2"
  local tmp; tmp=$(mktemp)
  HTTP_CODE=$(curl -s -o "$tmp" -w '%{http_code}' \
    -X POST -H 'Content-Type: application/json' \
    -d "$body" "$url" 2>/dev/null) || true
  cat "$tmp"; rm -f "$tmp"
}

# GET helper
get() {
  local url="$1"
  local tmp; tmp=$(mktemp)
  HTTP_CODE=$(curl -s -o "$tmp" -w '%{http_code}' "$url" 2>/dev/null) || true
  cat "$tmp"; rm -f "$tmp"
}

# Pretty-print JSON (truncated)
ppjson() {
  local max="${2:-80}"
  if command -v jq &>/dev/null; then
    echo "$1" | jq -C . 2>/dev/null | head -n "$max"
  else
    echo "$1" | head -c 2000
  fi
}

pause() {
  echo
  read -rp "  Press Enter to continue..." _
  echo
}

# ── Dependency check ─────────────────────────────────────────────────────────
for cmd in curl jq base64; do
  if ! command -v "$cmd" &>/dev/null; then
    echo -e "${R}ERROR:${N} '$cmd' is required but not found."; exit 1
  fi
done

###############################################################################
#                              TEST  FUNCTIONS
###############################################################################

# ─────────────────────────────────────────────────────────────────────────────
# 1. TEST CONNECTION
# ─────────────────────────────────────────────────────────────────────────────
test_connection() {
  hdr "1. Test Connection → ${AGENT}"
  local res; res=$(get "${BASE}/agent/status")
  if [[ "$HTTP_CODE" == "200" ]]; then
    local role peer_id peers
    role=$(echo "$res" | jq -r '.agent.role // "?"')
    peer_id=$(echo "$res" | jq -r '.agent.peer_id // "?"' | cut -c1-16)
    peers=$(echo "$res" | jq -r '.cluster.connected_peers // 0')
    ok "Connected — role=${role}  peer=${peer_id}...  cluster_peers=${peers}"
  else
    fail "Connection failed (HTTP ${HTTP_CODE})"
    dim "$res"
    return 1
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPLOAD TOSCA (full structure → triggers metadata auto-generation)
# ─────────────────────────────────────────────────────────────────────────────
upload_tosca() {
  local store="${1:-dsswres}"
  hdr "2. Upload TOSCA Template (store_full_structure=true, target=${store})"

  # Sample TOSCA
  local yaml
  yaml=$(cat <<'YAML'
tosca_definitions_version: tosca_simple_yaml_1_3

metadata:
  template_name: solar-farm-athens-test
  template_author: OptimusDB-Tester
  template_version: "1.0"

description: Test solar farm template for extended metadata verification

topology_template:
  node_templates:
    solar_panel_array:
      type: tosca.nodes.Compute
      properties:
        capacity_kw: 500
        panel_type: monocrystalline
        location: Athens-Attica
        latitude: 37.9838
        longitude: 23.7275
      capabilities:
        host:
          properties:
            num_cpus: 4
            mem_size: 8 GB

    inverter_unit:
      type: tosca.nodes.Compute
      properties:
        max_power_kw: 600
        efficiency: 0.97
      requirements:
        - dependency: solar_panel_array

    monitoring_sensor:
      type: tosca.nodes.Compute
      properties:
        sensor_type: irradiance
        sampling_rate_hz: 1
        protocol: MQTT
      requirements:
        - dependency: solar_panel_array
YAML
  )

  local encoded; encoded=$(echo "$yaml" | base64 -w0 2>/dev/null || echo "$yaml" | base64 2>/dev/null)

  local payload
  payload=$(jq -n \
    --arg file "$encoded" \
    --arg store "$store" \
    '{file: $file, filename: "test-solar-farm.yaml", store_full_structure: true, target_store: $store}')

  info "Uploading $(echo "$yaml" | wc -c) bytes..."
  local res; res=$(post "${BASE}/upload" "$payload")

  if [[ "$HTTP_CODE" == "200" ]]; then
    LAST_TEMPLATE_ID=$(echo "$res" | jq -r '.data.template_id // empty')
    local storage; storage=$(echo "$res" | jq -r '.data.storage_type // "?"')
    local fsize; fsize=$(echo "$res" | jq -r '.data.filesize // 0')
    ok "Upload successful"
    ok "  template_id : ${LAST_TEMPLATE_ID}"
    ok "  storage_type: ${storage}"
    ok "  filesize    : ${fsize} bytes"
    ok "  store       : ${store}"

    local fields; fields=$(echo "$res" | jq -r '.data.sample_fields // [] | length')
    ok "  queryable fields: ${fields}"
  else
    fail "Upload failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 20
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. UPLOAD CUSTOM YAML
# ─────────────────────────────────────────────────────────────────────────────
upload_custom_tosca() {
  hdr "2b. Upload Custom TOSCA File"
  read -rp "  Path to YAML file: " fpath
  if [[ ! -f "$fpath" ]]; then
    fail "File not found: $fpath"; return 1
  fi

  read -rp "  Target store [dsswres]: " store
  store="${store:-dsswres}"

  local encoded; encoded=$(base64 -w0 "$fpath" 2>/dev/null || base64 "$fpath" 2>/dev/null)
  local fname; fname=$(basename "$fpath")

  local payload
  payload=$(jq -n \
    --arg file "$encoded" \
    --arg fn "$fname" \
    --arg store "$store" \
    '{file: $file, filename: $fn, store_full_structure: true, target_store: $store}')

  info "Uploading ${fname}..."
  local res; res=$(post "${BASE}/upload" "$payload")

  if [[ "$HTTP_CODE" == "200" ]]; then
    LAST_TEMPLATE_ID=$(echo "$res" | jq -r '.data.template_id // empty')
    ok "Upload successful — template_id=${LAST_TEMPLATE_ID}"
    ppjson "$res" 30
  else
    fail "Upload failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 20
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. WAIT FOR ASYNC METADATA GENERATION
# ─────────────────────────────────────────────────────────────────────────────
wait_for_metadata() {
  hdr "3. Wait for Async Metadata Generation"
  if [[ -z "$LAST_TEMPLATE_ID" ]]; then
    warn "No template_id — upload first"; return 1
  fi

  info "Waiting for goroutine to finish (associated_id=${LAST_TEMPLATE_ID})..."

  local attempts=0 max=15
  while (( attempts < max )); do
    sleep 1
    ((attempts++))

    local query
    query=$(jq -n --arg tid "$LAST_TEMPLATE_ID" \
      '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"associated_id", operator:"==", value:$tid}]}')

    local res; res=$(post "${BASE}/command" "$query")
    local count; count=$(echo "$res" | jq -r '.data | if type == "array" then length else 0 end' 2>/dev/null || echo 0)

    if (( count > 0 )); then
      LAST_META_ID=$(echo "$res" | jq -r '.data[0]._id // empty')
      ok "Metadata found after ${attempts}s — id=${LAST_META_ID}"
      return 0
    fi

    dim "  attempt ${attempts}/${max} — not yet..."
  done

  warn "Metadata not found after ${max}s (goroutine may still be running)"
}

# ─────────────────────────────────────────────────────────────────────────────
# 5. QUERY METADATA IN ORBITDB
# ─────────────────────────────────────────────────────────────────────────────
query_metadata_orbitdb() {
  hdr "4. Query Metadata — OrbitDB KBMetadata"

  local tid="${1:-$LAST_TEMPLATE_ID}"
  if [[ -z "$tid" ]]; then
    read -rp "  Enter template_id (associated_id) to search: " tid
  fi

  local query
  query=$(jq -n --arg tid "$tid" \
    '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"associated_id", operator:"==", value:$tid}]}')

  local res; res=$(post "${BASE}/command" "$query")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.data | if type == "array" then length else 0 end' 2>/dev/null || echo 0)
    ok "Results: ${count}"
    if (( count > 0 )); then
      LAST_META_ID=$(echo "$res" | jq -r '.data[0]._id // empty')
      echo
      ppjson "$(echo "$res" | jq '.data[0]')" 60
    fi
  else
    fail "Query failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 10
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 6. QUERY METADATA IN SQLITE
# ─────────────────────────────────────────────────────────────────────────────
query_metadata_sqlite() {
  hdr "5. Query Metadata — SQLite metadata_catalog"

  local tid="${1:-$LAST_TEMPLATE_ID}"
  local sql
  if [[ -n "$tid" ]]; then
    sql="SELECT id, name, metadata_type, status, data_domain, data_quality_score, node_count, ipfs_cid, source_agent, created_at FROM metadata_catalog WHERE associated_id = '${tid}'"
  else
    sql="SELECT id, name, metadata_type, status, data_domain, data_quality_score, node_count, source_agent, created_at FROM metadata_catalog ORDER BY created_at DESC LIMIT 10"
  fi

  info "SQL: ${sql}"
  local res; res=$(post "${BASE}/ems/sql" "$(jq -n --arg s "$sql" '{sql:$s}')")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.records | length' 2>/dev/null || echo 0)
    ok "Results: ${count}"
    echo
    ppjson "$res" 40
  else
    fail "Query failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 10
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 7. VERIFY ALL 48 COLUMNS IN SQLITE
# ─────────────────────────────────────────────────────────────────────────────
verify_48_columns() {
  hdr "6. Verify 48-Column Schema (metadata_catalog)"

  local res; res=$(post "${BASE}/ems/sql" '{"sql":"PRAGMA table_info(metadata_catalog)"}')

  if [[ "$HTTP_CODE" != "200" ]]; then
    fail "Could not read schema (HTTP ${HTTP_CODE})"; return 1
  fi

  local cols; cols=$(echo "$res" | jq -r '.records | length' 2>/dev/null || echo 0)

  if (( cols >= 48 )); then
    ok "Schema has ${cols} columns (≥48) ✓"
  elif (( cols > 0 )); then
    warn "Schema has only ${cols} columns — migration may not have run"
  else
    fail "metadata_catalog table not found or empty schema"
    return 1
  fi

  # Expected columns
  local expected=(
    id author metadata_type component behaviour relationships
    associated_id name description tags status created_by
    created_at updated_at related_ids priority scheduling_info
    sla_constraints ownership_details audit_trail data_domain
    data_classification geo_location temporal_coverage data_quality_score
    schema_version content_hash file_format file_size_bytes record_count
    update_frequency retention_policy access_control compliance_tags
    provenance_chain processing_status api_endpoint version parent_id
    expiry_date language license_type contact_info node_count ipfs_cid
    source_agent source_pod source_ip
  )

  local actual; actual=$(echo "$res" | jq -r '.records[].name' 2>/dev/null)
  local missing=0

  for col in "${expected[@]}"; do
    if echo "$actual" | grep -qw "$col"; then
      dim "  ✓ ${col}"
    else
      fail "  MISSING: ${col}"
      ((missing++))
    fi
  done

  echo
  if (( missing == 0 )); then
    ok "All 48 expected columns present"
  else
    fail "${missing} columns missing"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 8. VERIFY TOSCA INDEX TABLE
# ─────────────────────────────────────────────────────────────────────────────
verify_tosca_index() {
  hdr "7. Verify TOSCA Index (tosca_metadata table)"

  local tid="${1:-$LAST_TEMPLATE_ID}"
  local sql
  if [[ -n "$tid" ]]; then
    sql="SELECT * FROM tosca_metadata WHERE template_id = '${tid}'"
  else
    sql="SELECT * FROM tosca_metadata ORDER BY rowid DESC LIMIT 5"
  fi

  local res; res=$(post "${BASE}/ems/sql" "$(jq -n --arg s "$sql" '{sql:$s}')")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.records | length' 2>/dev/null || echo 0)
    ok "TOSCA index entries: ${count}"
    echo
    ppjson "$res" 30
  else
    fail "Query failed (HTTP ${HTTP_CODE})"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 9. EDIT A METADATA FIELD (OrbitDB)
# ─────────────────────────────────────────────────────────────────────────────
edit_metadata_field() {
  hdr "8. Edit Metadata Field"

  local meta_id="${1:-$LAST_META_ID}"
  if [[ -z "$meta_id" ]]; then
    read -rp "  Enter metadata _id: " meta_id
  fi

  # First fetch current doc
  local query
  query=$(jq -n --arg mid "$meta_id" \
    '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"_id", operator:"==", value:$mid}]}')

  local res; res=$(post "${BASE}/command" "$query")
  local count; count=$(echo "$res" | jq -r '.data | if type == "array" then length else 0 end' 2>/dev/null || echo 0)

  if (( count == 0 )); then
    fail "Metadata entry not found: ${meta_id}"; return 1
  fi

  local doc; doc=$(echo "$res" | jq '.data[0]')
  info "Current entry:"
  echo "$doc" | jq -C '{ _id, name, status, metadata_type, data_domain, data_quality_score, priority, tags }' 2>/dev/null
  echo

  # Show available fields
  bold "Editable fields (grouped):"
  echo
  printf "  ${C}Core:${N}        name, description, metadata_type, status, version, tags, author\n"
  printf "  ${C}Relations:${N}   associated_id, parent_id, related_ids, component, behaviour\n"
  printf "  ${C}Classif:${N}     data_domain, data_classification, language, license_type, file_format\n"
  printf "  ${C}Quality:${N}     data_quality_score, priority, record_count, node_count\n"
  printf "  ${C}Temporal:${N}    temporal_coverage, update_frequency, expiry_date, retention_policy\n"
  printf "  ${C}Governance:${N}  access_control, compliance_tags, contact_info\n"
  printf "  ${C}Infra:${N}       geo_location, processing_status, api_endpoint, provenance_chain\n"
  echo

  read -rp "  Field to edit: " field
  if [[ -z "$field" ]]; then return; fi

  local current; current=$(echo "$doc" | jq -r --arg f "$field" '.[$f] // "∅"')
  info "Current value of '${field}': ${current}"

  read -rp "  New value: " newval
  if [[ -z "$newval" ]]; then warn "Empty — cancelled"; return; fi

  # Update the doc
  local updated; updated=$(echo "$doc" | jq \
    --arg f "$field" --arg v "$newval" \
    '. + {($f): $v, updated_at: (now | todate)}')

  local put_payload
  put_payload=$(jq -n --argjson doc "$updated" \
    '{method:{cmd:"put"}, dstype:"kbmetadata", args:[$doc | tostring]}')

  info "Saving to OrbitDB..."
  local put_res; put_res=$(post "${BASE}/command" "$put_payload")

  if [[ "$HTTP_CODE" == "200" ]]; then
    ok "OrbitDB updated"
  else
    fail "OrbitDB update failed"
  fi

  # Also update SQLite
  local safe_val; safe_val=$(echo "$newval" | sed "s/'/''/g")
  local update_sql="UPDATE metadata_catalog SET ${field} = '${safe_val}', updated_at = datetime('now') WHERE id = '${meta_id}'"
  info "Saving to SQLite..."
  local sql_res; sql_res=$(post "${BASE}/ems/sql" "$(jq -n --arg s "$update_sql" '{sql:$s}')")
  ok "SQLite updated"

  echo
  bold "Updated entry:"
  echo "$updated" | jq -C '{ _id, name, status, metadata_type, data_domain, data_quality_score, priority, (.["'"$field"'"] // empty) }' 2>/dev/null || ppjson "$updated" 20
}

# ─────────────────────────────────────────────────────────────────────────────
# 10. BATCH EDIT MULTIPLE FIELDS
# ─────────────────────────────────────────────────────────────────────────────
batch_edit_metadata() {
  hdr "9. Batch Edit — Multiple Fields"

  local meta_id="${1:-$LAST_META_ID}"
  if [[ -z "$meta_id" ]]; then
    read -rp "  Enter metadata _id: " meta_id
  fi

  # Fetch current doc
  local query
  query=$(jq -n --arg mid "$meta_id" \
    '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"_id", operator:"==", value:$mid}]}')

  local res; res=$(post "${BASE}/command" "$query")
  local doc; doc=$(echo "$res" | jq '.data[0]')

  if [[ "$doc" == "null" ]]; then
    fail "Metadata entry not found"; return 1
  fi

  info "Enter field=value pairs (one per line, empty line to finish):"
  echo

  local updates="{}"
  local sql_sets=""
  local count=0

  while true; do
    read -rp "  field=value: " line
    [[ -z "$line" ]] && break

    local f="${line%%=*}"
    local v="${line#*=}"
    f=$(echo "$f" | xargs)  # trim
    v=$(echo "$v" | xargs)

    if [[ -z "$f" || -z "$v" ]]; then
      warn "Invalid format, use: field_name=new_value"; continue
    fi

    updates=$(echo "$updates" | jq --arg f "$f" --arg v "$v" '. + {($f): $v}')
    local safe_v; safe_v=$(echo "$v" | sed "s/'/''/g")
    if (( count > 0 )); then sql_sets+=", "; fi
    sql_sets+="${f} = '${safe_v}'"
    ((count++))
    dim "  queued: ${f} → ${v}"
  done

  if (( count == 0 )); then warn "No changes"; return; fi

  # Merge updates into doc
  local updated; updated=$(echo "$doc" | jq --argjson u "$updates" '. + $u + {updated_at: (now | todate)}')

  # Save to OrbitDB
  local put_payload
  put_payload=$(jq -n --argjson doc "$updated" \
    '{method:{cmd:"put"}, dstype:"kbmetadata", args:[$doc | tostring]}')

  info "Saving ${count} fields to OrbitDB..."
  post "${BASE}/command" "$put_payload" > /dev/null
  ok "OrbitDB updated"

  # Save to SQLite
  local update_sql="UPDATE metadata_catalog SET ${sql_sets}, updated_at = datetime('now') WHERE id = '${meta_id}'"
  info "Saving ${count} fields to SQLite..."
  post "${BASE}/ems/sql" "$(jq -n --arg s "$update_sql" '{sql:$s}')" > /dev/null
  ok "SQLite updated"

  bold "Updated ${count} fields on ${meta_id}"
}

# ─────────────────────────────────────────────────────────────────────────────
# 11. CUSTOM ORBITDB QUERY
# ─────────────────────────────────────────────────────────────────────────────
custom_query() {
  hdr "10. Custom OrbitDB Query"

  read -rp "  Datastore [kbmetadata]: " ds
  ds="${ds:-kbmetadata}"

  local criteria="[]"
  local i=0
  while true; do
    read -rp "  Criterion field (empty to finish): " field
    [[ -z "$field" ]] && break
    read -rp "  Operator [==]: " op
    op="${op:-==}"
    read -rp "  Value: " val

    criteria=$(echo "$criteria" | jq --arg f "$field" --arg o "$op" --arg v "$val" \
      '. + [{field:$f, operator:$o, value:$v}]')
    ((i++))
  done

  local query
  query=$(jq -n --arg ds "$ds" --argjson c "$criteria" \
    '{method:{cmd:"query"}, dstype:$ds, criteria:$c}')

  info "Query: $(echo "$query" | jq -c .)"
  local res; res=$(post "${BASE}/command" "$query")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.data | if type == "array" then length else 1 end' 2>/dev/null || echo 0)
    ok "Results: ${count}"
    echo
    ppjson "$(echo "$res" | jq '.data')" 60
  else
    fail "Query failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 15
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 12. CUSTOM SQL
# ─────────────────────────────────────────────────────────────────────────────
custom_sql() {
  hdr "11. Custom SQL Query"
  read -rp "  SQL> " sql
  if [[ -z "$sql" ]]; then return; fi

  local res; res=$(post "${BASE}/ems/sql" "$(jq -n --arg s "$sql" '{sql:$s}')")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.records | length' 2>/dev/null || echo 0)
    ok "Results: ${count}"
    echo
    ppjson "$res" 60
  else
    fail "Query failed (HTTP ${HTTP_CODE})"
    ppjson "$res" 15
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 13. CLUSTER-WIDE REPLICATION CHECK
# ─────────────────────────────────────────────────────────────────────────────
cluster_replication_check() {
  hdr "12. Cluster-Wide Replication Check"

  local tid="${1:-$LAST_TEMPLATE_ID}"
  if [[ -z "$tid" ]]; then
    read -rp "  Enter template_id to check across cluster: " tid
  fi

  local ports=(18001 18002 18003 18004 18005 18006 18007 18008)
  local host; host=$(echo "$AGENT" | cut -d: -f1)

  echo
  printf "  ${W}%-12s %-8s %-12s %-20s${N}\n" "AGENT" "STATUS" "FOUND?" "META_ID"
  hr

  for port in "${ports[@]}"; do
    local url="http://${host}:${port}/${CTX}/command"
    local query
    query=$(jq -n --arg tid "$tid" \
      '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"associated_id", operator:"==", value:$tid}]}')

    local res; res=$(post "$url" "$query" 2>/dev/null)

    if [[ "$HTTP_CODE" == "200" ]]; then
      local count; count=$(echo "$res" | jq -r '.data | if type == "array" then length else 0 end' 2>/dev/null || echo 0)
      local mid="—"
      if (( count > 0 )); then
        mid=$(echo "$res" | jq -r '.data[0]._id // "?"' | cut -c1-20)
      fi

      if (( count > 0 )); then
        printf "  ${G}%-12s %-8s %-12s %-20s${N}\n" ":${port}" "OK" "YES (${count})" "$mid"
      else
        printf "  ${Y}%-12s %-8s %-12s %-20s${N}\n" ":${port}" "OK" "NO" "—"
      fi
    else
      printf "  ${D}%-12s %-8s %-12s %-20s${N}\n" ":${port}" "SKIP" "—" "—"
    fi
  done
}

# ─────────────────────────────────────────────────────────────────────────────
# 14. MESH STATUS
# ─────────────────────────────────────────────────────────────────────────────
mesh_status() {
  hdr "13. Mesh Status"
  local res; res=$(get "${BASE}/debug/optimusdb/mesh")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local health; health=$(echo "$res" | jq -r '.mesh_health.status // "?"')
    local coverage; coverage=$(echo "$res" | jq -r '.mesh_health.coverage_percent // "?"')
    local connected; connected=$(echo "$res" | jq -r '.libp2p.connected_peers // 0')
    local discovered; discovered=$(echo "$res" | jq -r '.discovery.discovered_count // 0')

    ok "Health: ${health}  Coverage: ${coverage}%  Peers: ${connected}/${discovered}"
    echo
    echo "$res" | jq -C '.diagnostics' 2>/dev/null
  else
    fail "Mesh status unavailable (HTTP ${HTTP_CODE})"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 15. FULL PIPELINE TEST (automated)
# ─────────────────────────────────────────────────────────────────────────────
full_pipeline_test() {
  hdr "FULL PIPELINE TEST"
  bold "Running automated end-to-end test..."
  echo

  # Step 1: Connection
  test_connection || { fail "Cannot continue without connection"; return 1; }
  echo

  # Step 2: Upload
  upload_tosca "dsswres"
  echo

  # Step 3: Wait for metadata
  wait_for_metadata
  echo

  # Step 4: Verify OrbitDB
  query_metadata_orbitdb "$LAST_TEMPLATE_ID"
  echo

  # Step 5: Verify SQLite metadata_catalog
  query_metadata_sqlite "$LAST_TEMPLATE_ID"
  echo

  # Step 6: Verify TOSCA index
  verify_tosca_index "$LAST_TEMPLATE_ID"
  echo

  # Step 7: Verify schema
  verify_48_columns
  echo

  # Step 8: Check cluster replication
  cluster_replication_check "$LAST_TEMPLATE_ID"
  echo

  hdr "PIPELINE TEST COMPLETE"
  if [[ -n "$LAST_META_ID" ]]; then
    ok "template_id = ${LAST_TEMPLATE_ID}"
    ok "metadata_id = ${LAST_META_ID}"
    info "Use option [8] to edit fields or [9] for batch edit"
  else
    warn "Metadata may still be generating — try [4] or [5] in a moment"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# 16. SHOW FULL ENTRY (all 48 fields)
# ─────────────────────────────────────────────────────────────────────────────
show_full_entry() {
  hdr "Show Full Metadata Entry (all 48 fields)"

  local meta_id="${1:-$LAST_META_ID}"
  if [[ -z "$meta_id" ]]; then
    read -rp "  Enter metadata _id: " meta_id
  fi

  info "Fetching from SQLite (all columns)..."
  local sql="SELECT * FROM metadata_catalog WHERE id = '${meta_id}'"
  local res; res=$(post "${BASE}/ems/sql" "$(jq -n --arg s "$sql" '{sql:$s}')")

  if [[ "$HTTP_CODE" == "200" ]]; then
    local count; count=$(echo "$res" | jq -r '.records | length' 2>/dev/null || echo 0)
    if (( count > 0 )); then
      ok "Entry found — all fields:"
      echo
      echo "$res" | jq -C '.records[0]' 2>/dev/null
    else
      warn "Not found in SQLite — trying OrbitDB..."
      local query
      query=$(jq -n --arg mid "$meta_id" \
        '{method:{cmd:"query"}, dstype:"kbmetadata", criteria:[{field:"_id", operator:"==", value:$mid}]}')
      res=$(post "${BASE}/command" "$query")
      ppjson "$(echo "$res" | jq '.data[0]')" 80
    fi
  else
    fail "Query failed"
  fi
}

###############################################################################
#                            INTERACTIVE  MENU
###############################################################################
show_menu() {
  echo
  printf "${M}╔══════════════════════════════════════════════════════╗${N}\n"
  printf "${M}║${N}  ${W}OptimusDB Extended Metadata Tester${N}                 ${M}║${N}\n"
  printf "${M}║${N}  ${D}Agent: ${C}${AGENT}${N}                          ${M}║${N}\n"
  printf "${M}╠══════════════════════════════════════════════════════╣${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${Y} 0)${N}  Full Pipeline Test (automated)                ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Connection ──${N}                                   ${M}║${N}\n"
  printf "${M}║${N}  ${G} 1)${N}  Test Connection                               ${M}║${N}\n"
  printf "${M}║${N}  ${G} 2)${N}  Switch Agent                                  ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Upload ──${N}                                       ${M}║${N}\n"
  printf "${M}║${N}  ${G} 3)${N}  Upload Sample TOSCA                           ${M}║${N}\n"
  printf "${M}║${N}  ${G} 4)${N}  Upload Custom YAML File                       ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Query & Browse ──${N}                               ${M}║${N}\n"
  printf "${M}║${N}  ${G} 5)${N}  Query Metadata (OrbitDB)                      ${M}║${N}\n"
  printf "${M}║${N}  ${G} 6)${N}  Query Metadata (SQLite)                       ${M}║${N}\n"
  printf "${M}║${N}  ${G} 7)${N}  Show Full Entry (all 48 fields)               ${M}║${N}\n"
  printf "${M}║${N}  ${G} 8)${N}  Custom OrbitDB Query                          ${M}║${N}\n"
  printf "${M}║${N}  ${G} 9)${N}  Custom SQL Query                              ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Edit ──${N}                                         ${M}║${N}\n"
  printf "${M}║${N}  ${G}10)${N}  Edit Single Field                             ${M}║${N}\n"
  printf "${M}║${N}  ${G}11)${N}  Batch Edit (multiple fields)                  ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Verification ──${N}                                 ${M}║${N}\n"
  printf "${M}║${N}  ${G}12)${N}  Verify 48-Column Schema                      ${M}║${N}\n"
  printf "${M}║${N}  ${G}13)${N}  Verify TOSCA Index                            ${M}║${N}\n"
  printf "${M}║${N}  ${G}14)${N}  Wait for Async Metadata                       ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${C}── Cluster ──${N}                                      ${M}║${N}\n"
  printf "${M}║${N}  ${G}15)${N}  Cluster Replication Check                     ${M}║${N}\n"
  printf "${M}║${N}  ${G}16)${N}  Mesh Status                                   ${M}║${N}\n"
  printf "${M}║${N}                                                      ${M}║${N}\n"
  printf "${M}║${N}  ${R} q)${N}  Quit                                          ${M}║${N}\n"
  printf "${M}╚══════════════════════════════════════════════════════╝${N}\n"

  if [[ -n "$LAST_TEMPLATE_ID" ]]; then
    dim "  Last template_id: ${LAST_TEMPLATE_ID}"
  fi
  if [[ -n "$LAST_META_ID" ]]; then
    dim "  Last metadata_id: ${LAST_META_ID}"
  fi
  echo
}

main() {
  clear 2>/dev/null || true
  printf "${W}OptimusDB Extended Metadata Tester${N}\n"
  dim "Agent: ${AGENT}  Context: ${CTX}"
  echo

  while true; do
    show_menu
    read -rp "  Select [0-16, q]: " choice

    case "$choice" in
      0)  full_pipeline_test ;;
      1)  test_connection ;;
      2)  read -rp "  New agent (host:port): " new_agent
          if [[ -n "$new_agent" ]]; then
            AGENT="$new_agent"
            BASE="http://${AGENT}/${CTX}"
            ok "Switched to ${AGENT}"
          fi ;;
      3)  read -rp "  Target store [dsswres]: " st
          upload_tosca "${st:-dsswres}" ;;
      4)  upload_custom_tosca ;;
      5)  query_metadata_orbitdb ;;
      6)  query_metadata_sqlite ;;
      7)  show_full_entry ;;
      8)  custom_query ;;
      9)  custom_sql ;;
      10) edit_metadata_field ;;
      11) batch_edit_metadata ;;
      12) verify_48_columns ;;
      13) verify_tosca_index ;;
      14) wait_for_metadata ;;
      15) cluster_replication_check ;;
      16) mesh_status ;;
      q|Q) echo; ok "Bye!"; exit 0 ;;
      *)  warn "Invalid choice" ;;
    esac

    pause
  done
}

# ── Run ──────────────────────────────────────────────────────────────────────
main