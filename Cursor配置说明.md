# Cursor配置说明

## 方案1: 使用本地服务（推荐用于测试）

**优点**: 速度快、无网络延迟、免费

**配置**:
```
Base URL: http://localhost:7860/v1
API Key: 123456
Model: gemini-2.5-flash
```

**注意**: 需要保持本地服务运行（`python app.py`）

---

## 方案2: 使用Hugging Face Space（推荐用于生产）

**优点**: 无需本地运行、随时可用、可分享给他人

**配置**:
```
Base URL: https://ch862747537-my-cloud-service.hf.space/v1
API Key: 123456
Model: gemini-2.5-flash
```

**注意**: 首次构建需要2-3分钟

---

## 可用的模型

### 基础模型
- `gemini-2.5-flash` - 最快的模型
- `gemini-2.5-pro` - 最强大的模型
- `gemini-1.5-flash` - 旧版快速模型
- `gemini-1.5-pro` - 旧版强大模型

### 搜索增强模型（带Google搜索）
- `gemini-2.5-flash-search`
- `gemini-2.5-pro-search`

### 思考模型（显示推理过程）
- `gemini-2.5-flash-thinking`
- `gemini-2.5-pro-thinking`

### 限制思考的模型
- `gemini-2.5-flash-nothinking` - 不显示思考过程
- `gemini-2.5-flash-maxthinking` - 最大化思考深度

---

## 在Cursor中配置

1. 打开Cursor设置
2. 找到"Models"或"Language Models"
3. 添加自定义模型：
   - Provider: OpenAI Compatible
   - Base URL: （见上方）
   - API Key: 123456
   - Model: gemini-2.5-flash

4. 测试连接
5. 开始使用！

---

## Function Calling支持

✅ 完全支持OpenAI的Function Calling API
✅ Cursor的所有工具都能正常工作
✅ 支持流式和非流式模式

**测试通过的功能**:
- ✅ 文件读写工具
- ✅ 命令执行工具
- ✅ 代码搜索工具
- ✅ 自定义函数调用

---

## 故障排查

### 问题1: "Connection refused"
**原因**: 本地服务未启动
**解决**: 运行 `python app.py` 或双击 `启动服务.bat`

### 问题2: "Invalid API key"
**原因**: API密钥错误
**解决**: 确保API Key设置为 `123456`

### 问题3: Hugging Face Space返回502
**原因**: Space正在构建或休眠
**解决**: 等待1-2分钟，或访问Space页面唤醒

### 问题4: 工具调用不工作
**原因**: 模型或配置问题
**解决**: 
1. 确保使用最新版本代码
2. 使用 `gemini-2.5-flash` 或 `gemini-2.5-pro`
3. 检查Cursor的Function Calling设置是否启用

---

## 性能对比

| 指标 | 本地服务 | Hugging Face Space |
|-----|---------|-------------------|
| 响应延迟 | 极低 (~50ms) | 较低 (~200ms) |
| 稳定性 | 需要保持运行 | 高（24/7可用） |
| 网络要求 | 无 | 需要稳定网络 |
| 推荐场景 | 开发测试 | 生产使用 |

---

**最后更新**: 2025-10-20 15:45

