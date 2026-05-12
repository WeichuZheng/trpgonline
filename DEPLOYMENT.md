# TRPG Online 部署操作手册

## 适用环境
- Ubuntu 22.04 LTS（推荐）/ 20.04 LTS
- 其他 Linux 发行版需自行调整包管理器命令

## 前置条件
- 一台 VPS（1核2G/10G SSD 以上）
- 一个域名（可选，建议使用 Cloudflare 代理/CDN，后续配置）
- SSH 连接到服务器

---

## 一、基础环境安装

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y \
  python3 python3-pip python3-venv \
  nginx certbot python3-certbot-nginx \
  curl git

# 安装 Node.js 20.x（前端构建用）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 验证
node --version   # 应显示 v20.x
python3 --version
```

---

## 二、部署代码

```bash
# 克隆仓库
sudo mkdir -p /var/www
sudo chown $USER:$USER /var/www
git clone https://github.com/WeichuZheng/trpgonline.git /var/www/trpgonline
cd /var/www/trpgonline
```

---

## 三、后端部署

### 3.1 创建 Python 虚拟环境

```bash
cd /var/www/trpgonline
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> 如果项目根目录没有 `requirements.txt`，可手动安装：
> ```bash
> pip install fastapi uvicorn gunicorn sqlalchemy aiosqlite python-jose[cryptography] passlib[bcrypt] python-multipart Pillow pydantic pydantic-settings
> ```

### 3.2 配置环境变量

```bash
# 创建 .env 文件
cat > .env << 'EOF'
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./database.db

# JWT 密钥 —— 务必修改为自己的随机字符串！
SECRET_KEY=此处填写随机生成的密钥

# 调试模式（部署时改为 false）
DEBUG=false

# CORS 允许的来源（部署时填写实际域名）
CORS_ORIGINS=https://你的域名.com

# 文件上传目录
UPLOAD_DIR=uploads

# 最大文件大小（字节，10MB）
MAX_FILE_SIZE=10485760
EOF
```

**生成安全的 JWT 密钥**：
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```
将输出复制到 `.env` 中的 `SECRET_KEY=` 后面。

### 3.3 创建上传目录

```bash
mkdir -p /var/www/trpgonline/uploads/{avatars,images,maps}
```

### 3.4 初始化数据库

```bash
cd /var/www/trpgonline
source venv/bin/activate
python init_db.py
```

### 3.5 创建 systemd 服务

```bash
sudo tee /etc/systemd/system/trpgonline.service > /dev/null << 'EOF'
[Unit]
Description=TRPG Online FastAPI Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/trpgonline
Environment="PATH=/var/www/trpgonline/venv/bin"
ExecStart=/var/www/trpgonline/venv/bin/gunicorn \
    backend.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/trpgonline/access.log \
    --error-logfile /var/log/trpgonline/error.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### 3.6 启动后端服务

```bash
# 创建日志目录
sudo mkdir -p /var/log/trpgonline

# 设置权限
sudo chown -R www-data:www-data /var/www/trpgonline
sudo chown -R www-data:www-data /var/log/trpgonline

# 启动
sudo systemctl daemon-reload
sudo systemctl enable trpgonline
sudo systemctl start trpgonline

# 检查状态
sudo systemctl status trpgonline
```

---

## 四、前端构建

```bash
cd /var/www/trpgonline/frontend
npm install

# 构建生产版本（输出到 frontend/dist/）
npm run build
```

> 构建产物在 `/var/www/trpgonline/frontend/dist/`，包含 `index.html` 和 `assets/` 目录。

---

## 五、Nginx 配置

### 5.1 创建站点配置

```bash
sudo tee /etc/nginx/sites-available/trpgonline > /dev/null << 'EOF'
server {
    listen 80;
    server_name 你的域名.com;   # ← 改为实际域名（或用服务器IP）

    # 前端 HTML —— 不缓存（入口文件）
    location / {
        root /var/www/trpgonline/frontend/dist;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }

    # 前端静态资源 —— 长期缓存（文件名带内容哈希）
    location /assets/ {
        root /var/www/trpgonline/frontend/dist;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 上传的图片 —— 缓存 + 允许重新验证
    location /uploads/ {
        root /var/www/trpgonline;
        expires 7d;
        add_header Cache-Control "public, must-revalidate";
    }

    # API —— 反向代理到 FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 20m;
    }

    # WebSocket —— 升级连接
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
EOF
```

### 5.2 启用站点

```bash
# 删除默认站点
sudo rm -f /etc/nginx/sites-enabled/default

# 启用 TRPG 站点
sudo ln -s /etc/nginx/sites-available/trpgonline /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

---

## 六、配置 HTTPS（使用 Let's Encrypt 免费证书）

```bash
# 确保域名已解析到服务器 IP
# 然后运行：
sudo certbot --nginx -d 你的域名.com

# 自动续期（certbot 默认会添加 cron 任务）
sudo certbot renew --dry-run
```

> 如果暂时没有域名，跳过此步骤，直接用 `http://服务器IP` 访问。

---

## 七、防火墙配置

```bash
# 开放 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# SSH 保持开放
sudo ufw allow 22/tcp

# 启用防火墙
sudo ufw enable
```

> **注意**：不要开放 8000 端口。API 只通过 Nginx 反代访问，不直接暴露。

---

## 八、验证部署

```bash
# 1. 后端健康检查
curl http://127.0.0.1:8000/docs

# 2. Nginx 前端访问
curl http://127.0.0.1/

# 3. systemd 服务状态
sudo systemctl status trpgonline

# 4. 查看日志
sudo journalctl -u trpgonline -f
```

在浏览器中访问 `http://你的域名.com`（或 `http://服务器IP`）确认能看到登录页面。

---

## 九、运维命令速查

```bash
# 查看服务状态
sudo systemctl status trpgonline

# 重启后端
sudo systemctl restart trpgonline

# 查看后端实时日志
sudo journalctl -u trpgonline -f

# 查看 Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# 重新构建前端（代码更新后）
cd /var/www/trpgonline
git pull
cd frontend && npm install && npm run build

# 重启 Nginx
sudo systemctl reload nginx
```

---

## 十、更新部署流程

```bash
cd /var/www/trpgonline
git pull

# 更新 Python 依赖（如有变化）
source venv/bin/activate
pip install -r requirements.txt

# 更新前端
cd frontend && npm install && npm run build && cd ..

# 重启后端
sudo systemctl restart trpgonline
```

---

## 十一、备份建议

```bash
# 创建每日备份脚本
sudo tee /etc/cron.daily/trpg-backup > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/trpgonline"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d)

# 备份数据库
cp /var/www/trpgonline/database.db $BACKUP_DIR/database-$DATE.db

# 备份上传文件
tar -czf $BACKUP_DIR/uploads-$DATE.tar.gz -C /var/www/trpgonline uploads/

# 保留最近 7 天的备份
find $BACKUP_DIR -type f -mtime +7 -delete
EOF

sudo chmod +x /etc/cron.daily/trpg-backup
```

---

## 十二、CDN 配置（后续步骤）

> CDN 在上云后单独配置，此处为预留说明：

1. **Cloudflare**：将域名的 DNS 指向 Cloudflare，开启橙色代理
2. **缓存规则**：
   - `/assets/*` → 强缓存 30 天
   - `/uploads/*` → 缓存 7 天
   - `/api/*` 和 `/ws` → 不缓存
3. **SSL**：Cloudflare 端设置为 Full (Strict)

详细 CDN 缓存在服务器稳定运行后再配置，可在带宽不足时节省 80%+ 流量。

---

**文档版本**: 1.0
**适用版本**: Phase 1-6 完整版
**最后更新**: 2026-05-12
