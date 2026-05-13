#!/bin/bash
set -e
echo "=== Stopping TRPG Online ==="
sudo systemctl stop trpgonline
echo "Backend stopped. Nginx remains running."
echo "To stop Nginx as well: sudo systemctl stop nginx"
