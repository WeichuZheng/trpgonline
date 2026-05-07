# API 验收标准

本标准适用于跑团网站项目的后端API开发验收。

## 1. 认证API

### 1.1 用户注册
- [ ] `POST /api/auth/register` - 用户注册接口
- [ ] 请求参数：username, password, email, role(GM/Player)
- [ ] 密码需加密存储
- [ ] 用户名唯一性验证
- [ ] 返回：用户ID或错误信息

### 1.2 用户登录
- [ ] `POST /api/auth/login` - 用户登录接口
- [ ] 请求参数：username, password
- [ ] 验证成功后返回Token
- [ ] 返回：access_token, user_info

### 1.3 用户登出
- [ ] `POST /api/auth/logout` - 用户登出接口
- [ ] 清除服务器端Session
- [ ] 返回：success/error

## 2. 房间API

### 2.1 房间管理
- [ ] `POST /api/rooms` - 创建房间（需GM权限）
- [ ] `GET /api/rooms` - 获取房间列表
- [ ] `GET /api/rooms/:id` - 获取房间详情
- [ ] `DELETE /api/rooms/:id` - 关闭房间（GM权限）
- [ ] `POST /api/rooms/:id/join` - 加入房间
- [ ] `POST /api/rooms/:id/leave` - 离开房间

### 2.2 房间数据
- [ ] 返回房间名称、描述、GM信息
- [ ] 返回当前在线玩家列表
- [ ] 返回房间状态（开放中/已关闭）

## 3. 消息API

### 3.1 实时消息
- [ ] `WebSocket /ws/room/:id` - 房间WebSocket连接
- [ ] 支持多人实时消息推送
- [ ] 消息类型：普通消息、系统消息、骰子结果
- [ ] 消息格式：{type, sender, content, timestamp}

### 3.2 消息历史
- [ ] `GET /api/rooms/:id/messages` - 获取历史消息
- [ ] 支持分页加载
- [ ] 返回最近50条消息

## 4. 角色卡牌API

### 4.1 角色管理
- [ ] `POST /api/characters` - 创建角色卡牌
- [ ] `GET /api/characters/:id` - 获取角色信息
- [ ] `PUT /api/characters/:id` - 更新角色信息
- [ ] `DELETE /api/characters/:id` - 删除角色

### 4.2 角色数据
- [ ] 角色属性（生命值、攻击力、防御力等）
- [ ] 角色装备和物品
- [ ] 角色技能列表

## 5. 骰子API

### 5.1 骰子系统
- [ ] `POST /api/dice/roll` - 投掷骰子
- [ ] 支持多种骰子类型（D4, D6, D8, D10, D12, D20, D100）
- [ ] 支持骰子修饰值
- [ ] 返回：骰子结果、总和、角色名

## 6. 性能要求

### 6.1 响应时间
- [ ] API平均响应时间 < 200ms
- [ ] WebSocket消息推送延迟 < 100ms

### 6.2 并发支持
- [ ] 支持同时在线 6-8 名用户
- [ ] 单个房间支持 8 人同时通信
- [ ] 系统总并发支持 50+ 用户

## 7. 安全要求

### 7.1 认证授权
- [ ] 所有API需要身份验证（除登录/注册）
- [ ] GM权限API需验证GM角色
- [ ] JWT Token过期时间合理设置

### 7.2 输入验证
- [ ] 所有输入参数进行验证
- [ ] 防止SQL注入
- [ ] 防止XSS攻击
- [ ] 请求体大小限制

### 7.3 速率限制
- [ ] 登录接口限流（防止暴力破解）
- [ ] API接口限流

## 8. 错误处理

### 8.1 HTTP状态码
- [ ] 200 - 成功
- [ ] 201 - 创建成功
- [ ] 400 - 请求参数错误
- [ ] 401 - 未认证
- [ ] 403 - 权限不足
- [ ] 404 - 资源不存在
- [ ] 500 - 服务器内部错误

### 8.2 错误响应格式
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```