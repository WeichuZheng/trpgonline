# TRPG Online — 运维手册

## 服务架构

```
浏览器 → (HTTPS 443) → Nginx → /api/* → Gunicorn (127.0.0.1:8000) → FastAPI
                           → /ws/* → Gunicorn WebSocket
                           → /*    → 静态文件 (frontend/dist/)
```

## 日志位置速查

| 目的 | 位置 | 轮转策略 | 说明 |
|------|------|----------|----------|
| 后端访问日志 | `/var/log/trpgonline/access.log` | 每日, 保留7天 | Gunicorn HTTP 请求 |
| 后端错误日志 | `/var/log/trpgonline/error.log` | 每日, 保留7天 | Gunicorn worker 错误 |
| Nginx 访问日志 | `/var/log/nginx/access.log` | 每日, 保留14天 | 所有 HTTP 流量 |
| Nginx 错误日志 | `/var/log/nginx/error.log` | 每日, 保留14天 | 代理连接错误 |
| 服务日志 | `sudo journalctl -u trpgonline` | systemd 管理 | 启动/崩溃/重启记录 |
| GameLog 数据库 | `database.db` → `game_logs` 表 | 每60分钟清理30天前 | 游戏内事件日志 |

## 常用运维命令

```bash
# 一键脚本（推荐）
cd /home/ubuntu/trpgonline/scripts
./status.sh          # 查看服务状态、内存、磁盘、日志
./start.sh           # 启动所有服务
./stop.sh            # 停止后端（保留 Nginx）
./restart.sh         # 重启后端
./backup.sh          # 备份数据库 + 上传文件到 /home/ubuntu/backups/
./cleanup.sh         # 手动清理旧日志 + VACUUM 数据库

# 直接 systemctl 命令
sudo systemctl status trpgonline     # 后端状态
sudo systemctl restart trpgonline    # 重启后端
sudo systemctl reload nginx          # 重载 Nginx 配置（不中断服务）

# 查看实时日志
sudo journalctl -u trpgonline -f        # 后端实时日志
sudo tail -f /var/log/trpgonline/error.log   # Gunicorn 错误
sudo tail -f /var/log/nginx/access.log       # Nginx 访问日志

# 测试后端健康
curl http://127.0.0.1:8000/health
```

## 服务故障自恢复

- `trpgonline.service` 配置了 `Restart=always` 和 `RestartSec=5`
- 如果后端崩溃，systemd 会在 5 秒后自动重启
- 重启次数无限制（不会进入 Failed 状态）
- 系统重启后服务自动启动（`enabled`）

## 更新部署

```bash
cd /home/ubuntu/trpgonline
git pull
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
sudo systemctl restart trpgonline
```

## 内存与磁盘管理

### 当前资源（部署时）

- 内存: 1.9GB 总量, ~300MB 可用（无 swap）
- 磁盘: 40GB 总量, ~32GB 可用
- 项目大小: ~193MB（含 venv, node_modules, .git）
- 数据库: ~172KB

### 建议配置 swap（服务器内存紧张时）

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 磁盘空间关注点

| 增长源 | 速率 | 清理方式 |
|--------|------|----------|
| `database.db` | ~数MB/月（取决于游戏量） | `./scripts/cleanup.sh` |
| `uploads/` | 取决于上传频率 | 手动检查大文件 |
| `game_logs` 表 | 每条骰子/攻击/日志一条 | 自动清理 30 天前 |
| `/var/log/trpgonline/` | ~数KB/天 | logrotate 自动轮转 |
| `/var/log/nginx/` | ~数百KB/天 | logrotate 自动轮转 |

### 如果磁盘快满

1. `./scripts/cleanup.sh` — 清理数据库旧日志
2. `sudo journalctl --vacuum-time=7d` — 清理 systemd 日志
3. 检查 `uploads/` 目录是否过大

## 备份

- 脚本: `./scripts/backup.sh`
- 备份目录: `/home/ubuntu/backups/`
- 保留最近 7 份数据库备份 + 上传文件备份
- 建议添加 cron: `0 3 * * * /home/ubuntu/trpgonline/scripts/backup.sh`

## 管理员系统

- 首个管理员通过 `.env` 中的 `INITIAL_ADMIN_USERNAME=admin` 配置
- 用此用户名注册的用户自动获得管理员 + GM 权限
- 管理员访问: https://chu2.online/admin（需登录管理员账号）
- 管理员可:
  - 查看所有用户列表
  - 批准/撤销 GM 权限
  - 设置其他用户为管理员
  - 手动清理游戏日志

## 故障排查

### 网站打不开 (502/504)

```bash
# 1. 检查后端是否运行
sudo systemctl status trpgonline
# 2. 如果挂了，重启
sudo systemctl restart trpgonline
# 3. 查看启动日志
sudo journalctl -u trpgonline --no-pager -n 50
```

### Nginx 配置错误

```bash
sudo nginx -t          # 测试配置
sudo systemctl reload nginx  # 重载
```

### SSL 证书过期

```bash
sudo certbot renew --dry-run   # 测试续期
sudo certbot renew             # 强制续期
```
> certbot 已配置自动续期定时任务，正常情况下无需手动操作。

### 内存不足

```bash
# 查看当前内存使用
free -h
# 如果可用内存持续低于 100MB，考虑：
# 1. 添加 swap（见上方）
# 2. 将 gunicorn workers 从 2 改为 1
#    编辑 /etc/systemd/system/trpgonline.service
#    修改 --workers 2 为 --workers 1
#    sudo systemctl daemon-reload && sudo systemctl restart trpgonline
```
