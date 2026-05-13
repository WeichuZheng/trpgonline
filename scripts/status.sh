#!/bin/bash
echo "=========================================="
echo "  TRPG Online — Status Dashboard"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""
echo "--- System Resources ---"
echo "Memory:"
free -h | grep -E "^(Mem|Swap)"
echo ""
echo "Disk:"
df -h / | tail -1
echo ""
echo "--- Project Disk Usage ---"
du -sh /home/ubuntu/trpgonline/ 2>/dev/null
du -sh /home/ubuntu/trpgonline/database.db 2>/dev/null
du -sh /home/ubuntu/trpgonline/uploads/ 2>/dev/null
du -sh /var/log/trpgonline/ 2>/dev/null
echo ""
echo "--- Service Status ---"
if systemctl is-active --quiet trpgonline; then
  echo "  trpgonline: RUNNING (pid $(systemctl show -p MainPID trpgonline | cut -d= -f2))"
else
  echo "  trpgonline: STOPPED"
fi
if systemctl is-active --quiet nginx; then
  echo "  nginx: RUNNING"
else
  echo "  nginx: STOPPED"
fi
echo ""
echo "--- Health Check ---"
curl -s -o /dev/null -w "  Backend: HTTP %{http_code}\n" http://127.0.0.1:8000/health 2>/dev/null || echo "  Backend: UNREACHABLE"
echo ""
echo "--- Recent Errors (gunicorn) ---"
tail -5 /var/log/trpgonline/error.log 2>/dev/null || echo "  (no errors)"
echo ""
echo "--- Recent Errors (nginx) ---"
tail -3 /var/log/nginx/error.log 2>/dev/null | grep -i error || echo "  (no recent errors)"
echo ""
echo "--- Database ---"
DB_SIZE=$(ls -lh /home/ubuntu/trpgonline/database.db 2>/dev/null | awk '{print $5}')
echo "  database.db: $DB_SIZE"
echo ""
echo "--- Backups ---"
ls -lt /home/ubuntu/backups/database_*.db 2>/dev/null | head -3 || echo "  (no backups yet)"
echo ""
