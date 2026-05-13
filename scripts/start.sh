#!/bin/bash
set -e
echo "=== TRPG Online 一键启动 ==="
echo "Starting Nginx..."
sudo systemctl start nginx
echo "Starting TRPG Online backend..."
sudo systemctl start trpgonline
sleep 2
echo ""
echo "Service status:"
sudo systemctl status trpgonline --no-pager -l | head -5
echo ""
echo "Nginx status:"
sudo systemctl status nginx --no-pager -l | head -3
echo ""
curl -s -o /dev/null -w "Health check: HTTP %{http_code}\n" http://127.0.0.1:8000/health
echo "Done. Visit https://chu2.online"
