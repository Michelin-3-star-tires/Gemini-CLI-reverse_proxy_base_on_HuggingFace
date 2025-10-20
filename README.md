# geminicli2api 本地部署研究项目

## 项目简介

本项目旨在研究并部署 [geminicli2api](https://github.com/gzzhongqi/geminicli2api) ——一个基于FastAPI的Gemini API代理服务，可将Google Gemini CLI工具转换为OpenAI兼容的API接口和原生Gemini API接口。

## 项目价值

✅ **免费使用Gemini模型** - 利用Google的免费API配额  
✅ **OpenAI兼容接口** - 无缝迁移现有OpenAI代码  
✅ **双重API支持** - 同时提供OpenAI和Gemini两种格式  
✅ **流式输出** - 支持实时流式响应  
✅ **多模态支持** - 文本和图像输入  
✅ **思维控制** - 可调节推理过程（maxthinking/nothinking）

## 快速开始

### 前置要求

- Docker Desktop已安装
- Google账号（用于获取OAuth凭证）
- 基本的命令行操作知识

### 部署步骤

#### 1. 获取Google OAuth凭证

参考 `docs/Google_OAuth凭证获取教程.md`（需要先创建该文件）

#### 2. 配置环境变量

复制示例配置文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入必要信息：
```env
GEMINI_AUTH_PASSWORD=your_secure_password
PORT=8888
GEMINI_CREDENTIALS='{"client_id":"...","refresh_token":"..."}'
```

#### 3. 启动服务

使用Docker Compose（推荐）：
```bash
docker-compose up -d
```

或使用Docker命令：
```bash
docker build -t geminicli2api .
docker run -p 8888:8888 --env-file .env geminicli2api
```

#### 4. 验证服务

访问健康检查端点：
```bash
curl http://localhost:8888/health
```

预期响应：
```json
{"status":"healthy","service":"geminicli2api"}
```

## API使用示例

### OpenAI兼容接口

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="your_password"
)

response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {"role": "user", "content": "解释量子计算"}
    ]
)
print(response.choices[0].message.content)
```

### 原生Gemini接口

```python
import requests

url = "http://localhost:8888/v1beta/models/gemini-2.5-pro:generateContent"
headers = {
    "Authorization": "Bearer your_password",
    "Content-Type": "application/json"
}
data = {
    "contents": [{
        "role": "user",
        "parts": [{"text": "解释机器学习"}]
    }]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 可用模型

### 基础模型
- `gemini-2.5-pro` - 高级多模态模型
- `gemini-2.5-flash` - 快速高效模型
- `gemini-2.5-pro-preview-xxx` - Pro预览版本
- `gemini-2.5-flash-preview-xxx` - Flash预览版本

### 模型变体
- **搜索增强**: `-search` 后缀（如 `gemini-2.5-pro-search`）
- **最小推理**: `-nothinking` 后缀
- **最大推理**: `-maxthinking` 后缀

示例：
- `gemini-2.5-pro-maxthinking` - 深度思考模式
- `gemini-2.5-flash-search` - 快速+搜索增强

## 认证方式

支持多种认证方式：

1. **Bearer Token**
   ```bash
   Authorization: Bearer your_password
   ```

2. **Query Parameter**
   ```bash
   ?key=your_password
   ```

3. **Basic Auth**
   ```bash
   Authorization: Basic base64(username:password)
   ```

4. **Google Header**
   ```bash
   x-goog-api-key: your_password
   ```

## 项目结构

```
.
├── app.py                 # 主入口文件
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像
├── docker-compose.yml    # Docker Compose配置
├── docs/                 # 项目文档
│   ├── 项目规划.md        # 详细的项目规划
│   ├── 修改记录.md        # 开发变更记录
│   └── Google_OAuth凭证获取教程.md  # OAuth教程
├── src/                  # 源代码
│   ├── main.py           # FastAPI主应用
│   ├── config.py         # 配置文件
│   ├── auth.py           # 认证模块
│   ├── openai_routes.py  # OpenAI路由
│   └── gemini_routes.py  # Gemini路由
├── data/                 # 数据文件
├── output/              # 输出文件
└── logs/                # 日志文件
```

## 文档资源

- 📘 [详细项目规划](docs/项目规划.md) - 完整的技术分析和部署方案
- 📘 [修改记录](docs/修改记录.md) - 开发过程记录
- 📘 [OAuth教程](docs/Google_OAuth凭证获取教程.md) - 凭证获取步骤

## 常见问题

### Q: 如何获取Google OAuth凭证？
A: 参考 `docs/Google_OAuth凭证获取教程.md` 文档

### Q: 端口8888已被占用怎么办？
A: 修改 `.env` 文件中的 `PORT` 变量为其他端口

### Q: 支持哪些模型？
A: 支持Gemini 2.5 Pro/Flash系列所有模型及其变体

### Q: 是否支持流式响应？
A: 是的，完全支持流式响应

## 安全注意事项

⚠️ **重要**: 
- OAuth凭证包含敏感信息，切勿提交到公开仓库
- 使用强密码作为 `GEMINI_AUTH_PASSWORD`
- 生产环境建议使用HTTPS
- 定期检查和更新凭证

## 开发维护

### 查看日志
```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f <container_id>
```

### 停止服务
```bash
# Docker Compose
docker-compose down

# Docker
docker stop <container_id>
```

### 重启服务
```bash
docker-compose restart
```

## 许可证

MIT License - 继承自原项目 [gzzhongqi/geminicli2api](https://github.com/gzzhongqi/geminicli2api)

## 相关链接

- 🔗 [原项目GitHub](https://github.com/gzzhongqi/geminicli2api)
- 🔗 [Google Cloud Console](https://console.cloud.google.com/)
- 🔗 [Google OAuth Playground](https://developers.google.com/oauthplayground/)

---

**最后更新**: 2025-10-20  
**项目状态**: 研究和部署中
