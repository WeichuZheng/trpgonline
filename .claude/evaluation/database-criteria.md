# 数据库验收标准

本标准适用于跑团网站项目的数据库开发验收。

## 1. 数据表设计

### 1.1 用户表 (users)
- [ ] id - 主键，自增
- [ ] username - 用户名，唯一索引
- [ ] password_hash - 密码哈希值
- [ ] email - 邮箱，唯一索引
- [ ] role - 角色类型（GM/Player）
- [ ] created_at - 创建时间
- [ ] updated_at - 更新时间
- [ ] last_login_at - 最后登录时间

### 1.2 房间表 (rooms)
- [ ] id - 主键，自增
- [ ] name - 房间名称
- [ ] description - 房间描述
- [ ] gm_id - 主持人ID，外键关联users
- [ ] status - 房间状态（open/closed）
- [ ] max_players - 最大玩家数（默认8）
- [ ] created_at - 创建时间
- [ ] closed_at - 关闭时间

### 1.3 房间参与者表 (room_participants)
- [ ] id - 主键，自增
- [ ] room_id - 房间ID，外键关联rooms
- [ ] user_id - 用户ID，外键关联users
- [ ] joined_at - 加入时间
- [ ] left_at - 离开时间
- [ ] UNIQUE(room_id, user_id) - 防止重复加入

### 1.4 消息表 (messages)
- [ ] id - 主键，自增
- [ ] room_id - 房间ID，外键关联rooms
- [ ] user_id - 发送者ID，外键关联users
- [ ] type - 消息类型（text/system/dice）
- [ ] content - 消息内容
- [ ] created_at - 发送时间
- [ ] 索引：room_id + created_at 用于分页查询

### 1.5 角色卡牌表 (characters)
- [ ] id - 主键，自增
- [ ] user_id - 玩家ID，外键关联users
- [ ] room_id - 房间ID，外键关联rooms
- [ ] name - 角色名称
- [ ] race - 种族
- [ ] class - 职业
- [ ] level - 等级
- [ ] hp - 生命值
- [ ] max_hp - 最大生命值
- [ ] attributes - 属性 JSON（力量、敏捷、智力等）
- [ ] skills - 技能 JSON
- [ ] inventory - 物品栏 JSON
- [ ] created_at - 创建时间
- [ ] updated_at - 更新时间

### 1.6 骰子记录表 (dice_rolls)
- [ ] id - 主键，自增
- [ ] room_id - 房间ID，外键关联rooms
- [ ] user_id - 投掷者ID，外键关联users
- [ ] character_id - 角色ID，外键关联characters
- [ ] dice_type - 骰子类型（D4/D6/D8/D10/D12/D20/D100）
- [ ] dice_count - 骰子数量
- [ ] modifier - 修饰值
- [ ] result - 投掷结果
- [ ] created_at - 投掷时间

## 2. 索引设计

### 2.1 性能索引
- [ ] users.username 唯一索引
- [ ] users.email 唯一索引
- [ ] messages.room_id + messages.created_at 复合索引
- [ ] characters.room_id 索引
- [ ] characters.user_id 索引

### 2.2 外键约束
- [ ] room_participants.room_id -> rooms.id
- [ ] room_participants.user_id -> users.id
- [ ] messages.room_id -> rooms.id
- [ ] messages.user_id -> users.id
- [ ] characters.room_id -> rooms.id
- [ ] characters.user_id -> users.id

## 3. 数据完整性

### 3.1 约束验证
- [ ] 房间最大人数限制为8人
- [ ] 用户名长度 3-20 字符
- [ ] 密码长度 >= 6 字符
- [ ] 房间名称长度 1-50 字符

### 3.2 级联操作
- [ ] 删除房间时级联删除消息和参与者
- [ ] 删除用户时级联删除角色卡牌

## 4. 安全性

### 4.1 密码存储
- [ ] 使用强哈希算法（bcrypt/argon2）
- [ ] 不存储明文密码

### 4.2 敏感数据
- [ ] 邮箱等敏感信息加密存储（如需要）
- [ ] 日志中不记录敏感信息

## 5. 性能优化

### 5.1 查询优化
- [ ] 房间列表查询使用分页
- [ ] 消息历史使用游标分页
- [ ] 避免 SELECT * 查询

### 5.2 读写分离（如适用）
- [ ] 读操作与写操作分离
- [ ] 缓存策略合理

## 6. 备份与恢复

### 6.1 数据备份
- [ ] 定期自动备份策略
- [ ] 备份可恢复性验证

### 6.2 迁移策略
- [ ] 数据库版本管理
- [ ] 迁移脚本可回滚

## 7. 日志与监控

### 7.1 审计日志
- [ ] 记录用户登录日志
- [ ] 记录重要数据变更
- [ ] 记录房间创建/关闭操作

### 7.2 监控指标
- [ ] 查询响应时间监控
- [ ] 连接池使用情况
- [ ] 慢查询日志