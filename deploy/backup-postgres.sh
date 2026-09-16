#!/usr/bin/env sh
set -eu

: "${PGHOST:?PGHOST is required}"
: "${PGPORT:?PGPORT is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGDATABASE:?PGDATABASE is required}"

backup_dir=${BACKUP_DIR:-/var/backups/coreerp}
timestamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_file="${backup_dir}/coreerp_${timestamp}.dump"

mkdir -p "$backup_dir"
pg_dump --format=custom --file="$backup_file"
sha256sum "$backup_file" > "${backup_file}.sha256"
printf 'Backup criado: %s\n' "$backup_file"
