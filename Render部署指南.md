# 🚀 Render.com 部署指南

## 📋 前提条件

- ✅ GitHub账号（推荐）或 GitLab账号
- ✅ Render账号（免费注册：https://render.com）
- ✅ 已获取的Google OAuth凭证

---

## 🎯 部署步骤（完整版）

### 步骤1: 准备GitHub仓库

#### 方案A: 创建新仓库（推荐）

1. 访问 https://github.com/new
2. 创建一个新仓库（可以是private）
3. **不要**初始化README、.gitignore或license

#### 方案B: 使用现有仓库

如果已有仓库，跳过此步骤。

---

### 步骤2: 推送代码到GitHub

在项目目录打开PowerShell，运行：

```powershell
# 初始化Git（如果还没有）
git init

# 添加GitHub远程仓库（替换YOUR_USERNAME和YOUR_REPO）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit for Render deployment"

# 推送到GitHub
git push -u origin main
```

---

### 步骤3: 在Render创建服务

1. **访问Render Dashboard**: https://dashboard.render.com

2. **点击 "New" → "Web Service"**

3. **连接GitHub仓库**:
   - 首次使用需要授权Render访问GitHub
   - 选择您刚创建的仓库
   - 点击 "Connect"

4. **配置服务**:
   
   **基本信息**:
   ```
   Name: gemini-api-proxy (或您喜欢的名字)
   Region: Oregon (美国) 或 Singapore (亚洲)
   Branch: main
   ```

   **构建设置**:
   ```
   Runtime: Docker
   Dockerfile Path: Dockerfile (默认)
   Docker Context: . (默认)
   ```

   **计划选择**:
   ```
   Plan: Free
   ```

5. **点击 "Create Web Service"**

---

### 步骤4: 配置环境变量

服务创建后，在服务页面：

1. **点击左侧 "Environment"**

2. **添加以下环境变量**:

   **变量1: GEMINI_AUTH_PASSWORD**
   ```
   Value: 123456
   ```

   **变量2: GOOGLE_CLOUD_PROJECT**
   ```
   Value: gen-lang-client-0008465735
   ```

   **变量3: GEMINI_CREDENTIALS**（整个JSON，一行）
   ```json
   {"client_id":"681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j.apps.googleusercontent.com","client_secret":"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","token":"YOUR_TOKEN","refresh_token":"YOUR_REFRESH_TOKEN","scopes":["https://www.googleapis.com/auth/cloud-platform","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"],"token_uri":"https://oauth2.googleapis.com/token","expiry":"2025-10-20T08:52:49.255671+00:00","project_id":"deductive-tractor-kxfg6"}
   ```

   **注意**: 用您自己的 `oauth_creds.json` 内容替换

3. **点击 "Save Changes"**

---

### 步骤5: 等待部署

- 配置环境变量后会自动触发重新部署
- 等待3-5分钟（首次部署较慢）
- 查看 "Logs" 标签页监控部署进度

---

### 步骤6: 获取服务URL

部署成功后：

1. 在服务页面顶部找到您的URL
2. 格式通常是: `https://gemini-api-proxy-xxxx.onrender.com`
3. 健康检查: `https://YOUR_SERVICE.onrender.com/health`
4. API地址: `https://YOUR_SERVICE.onrender.com/v1`

---

## 🔧 在Cursor中配置

```
Settings → Models → Add Custom Model

Provider: OpenAI Compatible
Base URL: https://YOUR_SERVICE.onrender.com/v1
API Key: 123456
Model: gemini-2.5-flash
```

---

## ⚙️ 高级配置（可选）

### 自定义域名

1. 在Render服务页面，点击 "Settings"
2. 找到 "Custom Domain" 部分
3. 添加您的域名并配置DNS

### 自动部署

- 默认情况下，推送到GitHub会自动触发部署
- 可以在 "Settings" → "Build & Deploy" 中配置

### 健康检查

Render会自动使用 `/health` 端点进行健康检查（已在代码中配置）

---

## 🚨 重要提示

### 免费套餐限制

✅ **优点**:
- 750小时/月免费运行时间
- 足够个人使用

⚠️ **限制**:
- **会休眠**: 15分钟无请求后自动休眠
- **冷启动**: 首次请求需要30秒唤醒
- **带宽**: 100GB/月

### 防止休眠（可选）

**方法1: 使用Uptime监控服务**
- 推荐: https://uptimerobot.com （免费）
- 每5分钟ping一次您的健康检查端点
- 保持服务始终运行

**方法2: 升级到付费套餐**
- $7/月起，不会休眠
- 更好的性能

---

## 🐛 故障排查

### 问题1: 部署失败

**症状**: 构建过程中出错

**解决**:
1. 查看 "Logs" 标签页的详细错误信息
2. 确认 `Dockerfile` 和 `requirements.txt` 正确
3. 检查所有文件都已推送到GitHub

### 问题2: 服务启动失败

**症状**: 部署成功但服务无法访问

**解决**:
1. 检查环境变量是否正确配置
2. 确认 `GEMINI_CREDENTIALS` 是有效的JSON格式
3. 查看运行日志中的错误信息

### 问题3: OAuth凭证过期

**症状**: 一段时间后服务无法调用Gemini API

**解决**:
1. 本地重新运行OAuth授权
2. 更新 `GEMINI_CREDENTIALS` 环境变量
3. 手动触发重新部署

### 问题4: 响应很慢

**症状**: 第一次请求等待很久

**解决**:
- 这是正常的，免费套餐会休眠
- 休眠后首次请求需要30秒唤醒
- 使用Uptime监控服务保持活跃

---

## 📊 监控和日志

### 查看日志

1. 在服务页面点击 "Logs"
2. 实时查看应用输出
3. 可以搜索和过滤日志

### 性能监控

1. 点击 "Metrics" 标签页
2. 查看CPU、内存、请求数等指标

---

## 🔄 更新部署

### 自动更新（推荐）

1. 在本地修改代码
2. 提交并推送到GitHub:
   ```bash
   git add .
   git commit -m "Update code"
   git push
   ```
3. Render自动检测并重新部署

### 手动触发

1. 在Render服务页面
2. 点击 "Manual Deploy" → "Deploy latest commit"

---

## 💰 费用说明

### 免费套餐
- **价格**: $0/月
- **限制**: 750小时/月，会休眠
- **适合**: 个人使用、开发测试

### Starter套餐
- **价格**: $7/月
- **优势**: 不休眠，更快响应
- **适合**: 轻度生产使用

### Standard套餐
- **价格**: $25/月
- **优势**: 更多资源，更高并发
- **适合**: 重度使用

---

## 🎉 部署完成检查清单

完成部署后，确认以下项目：

- [ ] ✅ 服务成功启动（状态为 "Live"）
- [ ] ✅ 健康检查通过（访问 `/health` 返回 healthy）
- [ ] ✅ 环境变量已配置（3个必需变量）
- [ ] ✅ 在Cursor中配置完成
- [ ] ✅ 测试简单对话成功
- [ ] ✅ 测试Function Calling成功
- [ ] ✅ （可选）配置Uptime监控防止休眠

---

## 📚 相关资源

- **Render文档**: https://render.com/docs
- **Docker部署指南**: https://render.com/docs/docker
- **环境变量管理**: https://render.com/docs/environment-variables
- **自定义域名**: https://render.com/docs/custom-domains

---

## 💡 提示和技巧

1. **使用render.yaml**: 项目根目录的 `render.yaml` 可以简化配置
2. **查看日志**: 遇到问题先看日志，90%的问题能找到答案
3. **分阶段测试**: 先确保健康检查通过，再测试具体功能
4. **备份凭证**: 保存好 `oauth_creds.json`，避免重新授权
5. **监控使用**: 定期检查免费额度使用情况

---

**最后更新**: 2025-10-20  
**版本**: 1.0

祝部署顺利！🚀

