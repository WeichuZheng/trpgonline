#!/bin/bash
set -e
echo "=== Restarting TRPG Online ==="
sudo systemctl restart trpgonline
echo "Reloading Nginx..."
sudo nginx -t > /dev/null 2>&1 && sudo systemctl reload nginx
sleep 2
curl -s -o /dev/null -w "Health check: HTTP %{http_code}\n" http://127.0.0.1:8000/health
echo "Services restarted."
