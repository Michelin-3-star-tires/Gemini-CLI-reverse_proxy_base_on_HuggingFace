# Google OAuth 凭证获取完整教程

本教程将指导您一步步获取使用 geminicli2api 所需的 Google OAuth 凭证。

## 📋 前置条件

- ✅ 拥有Google账号
- ✅ 可以访问 [Google Cloud Console](https://console.cloud.google.com/)
- ✅ 基本的浏览器操作能力

## 🎯 目标

获取包含以下信息的OAuth凭证：
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "scopes": ["https://www.googleapis.com/auth/cloud-platform"],
  "token_uri": "https://oauth2.googleapis.com/token",
  "project_id": "your-project-id"
}
```

---

## 🚀 方法一：使用项目自带OAuth流程（推荐）

### 步骤1：创建Google Cloud项目

1. **访问Google Cloud Console**
   - 打开浏览器访问：https://console.cloud.google.com/
   - 使用您的Google账号登录

2. **创建新项目**
   - 点击顶部的 "选择项目"
   - 点击 "新建项目"
   - 输入项目名称（例如：`gemini-api-proxy`）
   - 点击 "创建"
   - 等待项目创建完成（约10-30秒）

3. **记录项目ID**
   - 在项目列表中找到您刚创建的项目
   - 记录下项目ID（通常在项目名称下方显示）
   - 示例：`gemini-api-proxy-12345`

### 步骤2：启用必要的API

1. **导航到API库**
   - 在左侧菜单中，点击 "API和服务" → "库"

2. **启用以下API**（搜索并逐个启用）：
   - **Generative Language API** (Gemini API)
     - 搜索 "Generative Language"
     - 点击进入，点击 "启用"
   
   - **Cloud AI Platform API**
     - 搜索 "Cloud AI Platform"
     - 点击进入，点击 "启用"
   
   - **Cloud Resource Manager API**
     - 搜索 "Cloud Resource Manager"
     - 点击进入，点击 "启用"

   > 注意：API启用可能需要1-2分钟生效

### 步骤3：配置OAuth同意屏幕

1. **导航到OAuth同意屏幕**
   - 点击 "API和服务" → "OAuth同意屏幕"

2. **选择用户类型**
   - 选择 "外部"（External）
   - 点击 "创建"

3. **填写应用信息**
   - **应用名称**：输入任意名称（例如：`Gemini API Proxy`）
   - **用户支持电子邮件**：选择您的Gmail邮箱
   - **开发者联系信息**：输入您的Gmail邮箱
   - 点击 "保存并继续"

4. **配置范围**
   - 点击 "添加或移除范围"
   - 搜索并添加：
     - `.../auth/cloud-platform`
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
   - 点击 "更新"
   - 点击 "保存并继续"

5. **添加测试用户**
   - 点击 "添加用户"
   - 输入您的Gmail邮箱
   - 点击 "添加"
   - 点击 "保存并继续"

6. **完成配置**
   - 检查摘要信息
   - 点击 "返回控制面板"

### 步骤4：创建OAuth 2.0客户端ID

1. **导航到凭据页面**
   - 点击 "API和服务" → "凭据"

2. **创建凭据**
   - 点击顶部的 "+ 创建凭据"
   - 选择 "OAuth 2.0 客户端 ID"

3. **配置客户端**
   - **应用类型**：选择 "桌面应用"
   - **名称**：输入任意名称（例如：`Desktop Client`）
   - 点击 "创建"

4. **保存凭据**
   - 会弹出包含Client ID和Client Secret的对话框
   - **重要**：记录下这两个值
   - 也可以点击 "下载JSON"，保存凭据文件

### 步骤5：首次运行获取Token

#### 方式A：通过Docker运行（推荐）

1. **创建 `.env` 文件**
   ```bash
   GEMINI_AUTH_PASSWORD=your_secure_password
   PORT=8888
   GOOGLE_CLOUD_PROJECT=your-project-id  # 第一步记录的项目ID
   ```

2. **启动服务**
   ```bash
   docker-compose up
   ```

3. **完成OAuth授权**
   - 终端会显示一个URL
   - 复制URL到浏览器打开
   - 选择您的Google账号
   - 点击 "允许"授权
   - 看到 "OAuth authentication successful!" 即成功

4. **获取凭证文件**
   - 服务会自动生成 `oauth_creds.json` 文件
   - 查看文件内容：
     ```bash
     cat oauth_creds.json
     ```

#### 方式B：通过Python运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   export GEMINI_AUTH_PASSWORD=your_password
   export GOOGLE_CLOUD_PROJECT=your-project-id
   ```

3. **运行应用**
   ```bash
   python app.py
   ```

4. **完成OAuth授权**（同方式A的步骤3）

5. **查看凭证**
   ```bash
   cat oauth_creds.json
   ```

### 步骤6：配置环境变量

1. **复制凭证JSON内容**
   - 打开 `oauth_creds.json`
   - 复制全部内容

2. **更新 `.env` 文件**
   ```bash
   GEMINI_AUTH_PASSWORD=your_secure_password
   PORT=8888
   GEMINI_CREDENTIALS='{"client_id":"...","refresh_token":"..."}'
   ```

   > 注意：将整个JSON对象作为字符串，用单引号包裹

---

## 🔧 方法二：使用Google OAuth Playground

如果方法一遇到问题，可以使用OAuth Playground手动获取token。

### 步骤1-4：同方法一

完成Google Cloud项目创建、API启用、OAuth配置和客户端创建。

### 步骤5：使用OAuth Playground

1. **访问OAuth Playground**
   - 打开：https://developers.google.com/oauthplayground/

2. **配置OAuth**
   - 点击右上角的齿轮图标（Settings）
   - 勾选 "Use your own OAuth credentials"
   - 输入您的 `OAuth Client ID`
   - 输入您的 `OAuth Client secret`
   - 点击 "Close"

3. **选择API范围**
   - 在左侧 "Step 1" 中
   - 找到并勾选：
     - `https://www.googleapis.com/auth/cloud-platform`
     - `https://www.googleapis.com/auth/userinfo.email`
     - `https://www.googleapis.com/auth/userinfo.profile`
   - 点击 "Authorize APIs"

4. **授权**
   - 选择您的Google账号
   - 点击 "允许"
   - 会跳转回OAuth Playground

5. **交换授权码**
   - 在 "Step 2" 中
   - 点击 "Exchange authorization code for tokens"
   - 会生成 `access_token` 和 `refresh_token`

6. **复制Token**
   - 复制 `refresh_token`（这是最重要的）
   - 复制 `access_token`

### 步骤6：手动构建凭证JSON

创建凭证JSON文件：
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "token": "access-token-from-playground",
  "refresh_token": "refresh-token-from-playground",
  "scopes": [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
  ],
  "token_uri": "https://oauth2.googleapis.com/token",
  "project_id": "your-project-id"
}
```

---

## ✅ 验证凭证

### 测试凭证是否有效

1. **启动服务**
   ```bash
   docker-compose up -d
   ```

2. **检查日志**
   ```bash
   docker-compose logs
   ```

   成功的日志应包含：
   ```
   Successfully onboarded with project ID: your-project-id
   Gemini proxy server started successfully
   ```

3. **测试API**
   ```bash
   curl http://localhost:8888/health
   ```

   应返回：
   ```json
   {"status":"healthy","service":"geminicli2api"}
   ```

4. **测试认证**
   ```bash
   curl -X GET http://localhost:8888/v1/models \
     -H "Authorization: Bearer your_password"
   ```

   应返回模型列表。

---

## 🔒 安全最佳实践

### 凭证管理

1. **永不公开凭证**
   - ❌ 不要提交 `oauth_creds.json` 到Git
   - ❌ 不要在公开聊天中分享凭证
   - ❌ 不要在截图中暴露凭证

2. **使用环境变量**
   - ✅ 始终通过环境变量传递凭证
   - ✅ 使用 `.env` 文件（已在 `.gitignore` 中）
   - ✅ 生产环境使用密钥管理服务

3. **定期轮换**
   - ✅ 定期更新OAuth token
   - ✅ 如果凭证泄露，立即撤销并重新生成

### 项目安全

1. **最小权限原则**
   - 只启用必需的API
   - 只授予必需的权限范围

2. **监控使用**
   - 定期检查API使用量
   - 启用Google Cloud的计费警报

---

## ❓ 常见问题

### Q1: 授权后显示 "redirect_uri_mismatch"

**原因**：OAuth客户端配置的重定向URI不匹配

**解决方案**：
1. 返回 Google Cloud Console → "凭据"
2. 编辑OAuth客户端
3. 确保 "授权的重定向URI" 中包含 `http://localhost:8080`
4. 保存并重试

### Q2: API启用后仍然报错 "API not enabled"

**原因**：API启用需要时间生效

**解决方案**：
- 等待2-5分钟后重试
- 刷新Google Cloud Console页面
- 确认项目切换正确

### Q3: refresh_token为空或null

**原因**：未正确设置OAuth同意屏幕或未使用`access_type=offline`

**解决方案**：
1. 删除现有的OAuth客户端
2. 重新创建OAuth同意屏幕（确保添加测试用户）
3. 重新创建OAuth客户端
4. 重新授权（确保看到权限确认页面）

### Q4: 出现 "insufficient permissions" 错误

**原因**：授予的API权限不足

**解决方案**：
1. 检查 `.env` 中的 `scopes` 是否包含所有必需的范围
2. 重新运行OAuth流程，确保授予所有权限
3. 在Google Cloud Console中检查API是否全部启用

### Q5: Token过期错误

**原因**：access_token过期，且自动刷新失败

**解决方案**：
- 项目会自动使用 `refresh_token` 刷新
- 如果自动刷新失败，检查 `refresh_token` 是否有效
- 必要时重新运行OAuth流程

---

## 📚 参考资料

- [Google OAuth 2.0文档](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth Playground](https://developers.google.com/oauthplayground/)
- [Gemini API文档](https://ai.google.dev/docs)

---

**文档版本**: 1.0  
**创建时间**: 2025-10-20  
**最后更新**: 2025-10-20

如有任何问题，请参考主项目的 [GitHub Issues](https://github.com/gzzhongqi/geminicli2api/issues)

