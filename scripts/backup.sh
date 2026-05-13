#!/bin/bash
set -e
BACKUP_DIR="/home/ubuntu/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "=== TRPG Online Backup ==="

echo "[1/2] Backing up database..."
cp /home/ubuntu/trpgonline/database.db "$BACKUP_DIR/database_$TIMESTAMP.db"

echo "[2/2] Backing up uploads..."
tar -czf "$BACKUP_DIR/uploads_$TIMESTAMP.tar.gz" \
  -C /home/ubuntu/trpgonline uploads/ \
  --warning=no-file-changed 2>/dev/null || true

echo ""
echo "--- Rotation (keeping last 7) ---"
ls -t "$BACKUP_DIR"/database_*.db 2>/dev/null | tail -n +8 | xargs -r rm -v
ls -t "$BACKUP_DIR"/uploads_*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm -v

echo ""
DB_FILE="$BACKUP_DIR/database_$TIMESTAMP.db"
echo "Backup complete!"
echo "  Database: $DB_FILE ($(du -h "$DB_FILE" | cut -f1))"
echo "  Uploads:  $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz ($(du -h "$BACKUP_DIR/uploads_$TIMESTAMP.tar.gz" 2>/dev/null | cut -f1))"
