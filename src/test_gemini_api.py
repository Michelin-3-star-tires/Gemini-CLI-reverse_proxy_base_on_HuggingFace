#%%
"""
Gemini原生接口测试脚本

此脚本用于测试 geminicli2api 的 Gemini 原生接口
"""
import os

# 强制设置终端编码为UTF-8
os.system('chcp 65001 > nul')

#%%
import logging
import requests
import json

# --- 标准化路径管理 ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_dir)

LOGS_DIR = os.path.join(project_root, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# --- 配置日志 ---
log_file = os.path.join(LOGS_DIR, 'test_gemini_api.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logging.captureWarnings(True)

#%%
# --- 测试参数配置 ---
BASE_URL = "http://localhost:8888"
API_PASSWORD = "your_password"  # 替换为你的密码

# 记录测试参数
logging.info("=" * 60)
logging.info("Gemini API 测试开始")
logging.info(f"API Base URL: {BASE_URL}")
logging.info("=" * 60)

#%%
def get_headers():
    """获取请求头"""
    return {
        "Authorization": f"Bearer {API_PASSWORD}",
        "Content-Type": "application/json"
    }

#%%
def test_list_models():
    """测试列出模型"""
    logging.info("\n【测试1】列出 Gemini 模型")
    
    try:
        url = f"{BASE_URL}/v1beta/models"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        
        data = response.json()
        models = data.get('models', [])
        
        logging.info(f"✓ 成功获取模型列表，共 {len(models)} 个模型")
        
        # 列出前5个模型
        for i, model in enumerate(models[:5], 1):
            model_name = model.get('name', 'unknown')
            display_name = model.get('displayName', 'unknown')
            logging.info(f"  {i}. {model_name} ({display_name})")
        
        if len(models) > 5:
            logging.info(f"  ... 还有 {len(models) - 5} 个模型")
        
        return True
        
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        return False

#%%
def test_generate_content(model="gemini-2.5-flash"):
    """测试生成内容"""
    logging.info(f"\n【测试2】生成内容 - 模型: {model}")
    
    try:
        # 移除 models/ 前缀（如果有）
        model_name = model.replace("models/", "")
        
        url = f"{BASE_URL}/v1beta/models/{model_name}:generateContent"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "用一句话解释什么是人工智能"}]
                }
            ]
        }
        
        logging.info(f"发送请求到: {url}")
        logging.info(f"请求内容: {payload['contents'][0]['parts'][0]['text']}")
        
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # 提取响应文本
        if 'candidates' in data and len(data['candidates']) > 0:
            content = data['candidates'][0].get('content', {})
            parts = content.get('parts', [])
            if parts and 'text' in parts[0]:
                text = parts[0]['text']
                logging.info(f"响应内容: {text}")
                logging.info("✓ 生成内容测试成功")
                return True
        
        logging.warning("响应格式异常")
        logging.info(f"完整响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return False
        
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            logging.error(f"响应状态码: {e.response.status_code}")
            logging.error(f"响应内容: {e.response.text}")
        return False

#%%
def test_stream_generate_content(model="gemini-2.5-flash"):
    """测试流式生成内容"""
    logging.info(f"\n【测试3】流式生成内容 - 模型: {model}")
    
    try:
        # 移除 models/ 前缀（如果有）
        model_name = model.replace("models/", "")
        
        url = f"{BASE_URL}/v1beta/models/{model_name}:streamGenerateContent"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "列举三个编程语言"}]
                }
            ]
        }
        
        logging.info(f"发送请求到: {url}")
        logging.info(f"请求内容: {payload['contents'][0]['parts'][0]['text']}")
        
        response = requests.post(
            url, 
            headers=get_headers(), 
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        logging.info("接收流式响应:")
        full_text = ""
        
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith('data: '):
                    json_str = line_text[6:]  # 移除 'data: ' 前缀
                    try:
                        chunk_data = json.loads(json_str)
                        if 'candidates' in chunk_data and len(chunk_data['candidates']) > 0:
                            content = chunk_data['candidates'][0].get('content', {})
                            parts = content.get('parts', [])
                            if parts and 'text' in parts[0]:
                                text = parts[0]['text']
                                full_text += text
                    except json.JSONDecodeError:
                        continue
        
        logging.info(f"完整响应: {full_text}")
        logging.info("✓ 流式生成测试成功")
        return True
        
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            logging.error(f"响应状态码: {e.response.status_code}")
            logging.error(f"响应内容: {e.response.text}")
        return False

#%%
def test_search_model():
    """测试带搜索的模型"""
    logging.info(f"\n【测试4】搜索增强模型 - 模型: gemini-2.5-flash-search")
    
    try:
        url = f"{BASE_URL}/v1beta/models/gemini-2.5-flash-search:generateContent"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "2024年诺贝尔物理学奖获得者是谁？"}]
                }
            ]
        }
        
        logging.info(f"请求内容: {payload['contents'][0]['parts'][0]['text']}")
        
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if 'candidates' in data and len(data['candidates']) > 0:
            content = data['candidates'][0].get('content', {})
            parts = content.get('parts', [])
            if parts and 'text' in parts[0]:
                text = parts[0]['text']
                logging.info(f"响应内容: {text}")
                logging.info("✓ 搜索增强测试成功")
                return True
        
        logging.warning("响应格式异常")
        return False
        
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        return False

#%%
def run_all_tests():
    """运行所有测试"""
    logging.info("\n" + "=" * 60)
    logging.info("开始运行所有测试")
    logging.info("=" * 60)
    
    results = {}
    
    # 测试1：列出模型
    results['list_models'] = test_list_models()
    
    # 测试2：生成内容
    results['generate_content'] = test_generate_content()
    
    # 测试3：流式生成
    results['stream_generate'] = test_stream_generate_content()
    
    # 测试4：搜索增强
    results['search_model'] = test_search_model()
    
    # 总结
    logging.info("\n" + "=" * 60)
    logging.info("测试结果汇总")
    logging.info("=" * 60)
    
    for test_name, success in results.items():
        status = "✓ 通过" if success else "✗ 失败"
        logging.info(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    logging.info(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        logging.info("🎉 所有测试通过！")
    else:
        logging.warning(f"⚠️ {total - passed} 个测试失败")
    
    logging.info("=" * 60)

#%%
if __name__ == "__main__":
    run_all_tests()

