#!/bin/bash
set -e
DB_PATH="/home/ubuntu/trpgonline/database.db"

echo "=== TRPG Online Cleanup ==="
echo ""

echo "[1/3] Deleting GameLog entries older than 30 days..."
if [ -f "$DB_PATH" ]; then
    BEFORE=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM game_logs;" 2>/dev/null || echo 0)
    sqlite3 "$DB_PATH" "DELETE FROM game_logs WHERE created_at < datetime('now', '-30 days', '+8 hours');" 2>/dev/null
    AFTER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM game_logs;" 2>/dev/null || echo 0)
    DELETED=$((BEFORE - AFTER))
    echo "  Before: $BEFORE, After: $AFTER, Deleted: $DELETED"
else
    echo "  Database not found at $DB_PATH"
fi

echo ""
echo "[2/3] Truncating gunicorn logs..."
for f in /var/log/trpgonline/access.log /var/log/trpgonline/error.log; do
    if [ -f "$f" ]; then
        SIZE=$(du -h "$f" | cut -f1)
        sudo truncate -s 0 "$f" 2>/dev/null && echo "  $f truncated (was $SIZE)" || echo "  $f: skip (permission denied)"
    fi
done

echo ""
echo "[3/3] Vacuuming database..."
sqlite3 "$DB_PATH" "VACUUM;" 2>/dev/null
echo "  VACUUM complete."

echo ""
echo "=== Cleanup done ==="
