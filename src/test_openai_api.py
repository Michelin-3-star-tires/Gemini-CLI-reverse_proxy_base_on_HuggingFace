#%%
"""
OpenAI兼容接口测试脚本

此脚本用于测试 geminicli2api 的 OpenAI 兼容接口
"""
import os

# 强制设置终端编码为UTF-8
os.system('chcp 65001 > nul')

#%%
import logging
from openai import OpenAI

# --- 标准化路径管理 ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_dir)

LOGS_DIR = os.path.join(project_root, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# --- 配置日志 ---
log_file = os.path.join(LOGS_DIR, 'test_openai_api.log')
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
BASE_URL = "http://localhost:8888/v1"
API_KEY = "your_password"  # 替换为你的密码
TEST_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-pro-maxthinking",
]

# 记录测试参数
logging.info("=" * 60)
logging.info("OpenAI API 测试开始")
logging.info(f"API Base URL: {BASE_URL}")
logging.info(f"测试模型: {TEST_MODELS}")
logging.info("=" * 60)

#%%
def test_list_models():
    """测试列出可用模型"""
    logging.info("\n【测试1】列出可用模型")
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        models = client.models.list()
        
        logging.info(f"✓ 成功获取模型列表，共 {len(models.data)} 个模型")
        
        # 列出前5个模型
        for i, model in enumerate(models.data[:5], 1):
            logging.info(f"  {i}. {model.id}")
        
        if len(models.data) > 5:
            logging.info(f"  ... 还有 {len(models.data) - 5} 个模型")
        
        return True
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        return False

#%%
def test_chat_completion(model, stream=False):
    """测试聊天补全"""
    mode_text = "流式" if stream else "非流式"
    logging.info(f"\n【测试2】{mode_text}聊天补全 - 模型: {model}")
    
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        
        messages = [
            {"role": "user", "content": "用一句话解释什么是量子纠缠"}
        ]
        
        logging.info(f"发送消息: {messages[0]['content']}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            max_tokens=100
        )
        
        if stream:
            logging.info("接收响应（流式）:")
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
            
            logging.info(f"完整响应: {full_response}")
        else:
            content = response.choices[0].message.content
            logging.info(f"响应内容: {content}")
        
        logging.info(f"✓ {mode_text}测试成功")
        return True
        
    except Exception as e:
        logging.error(f"✗ 测试失败: {str(e)}")
        return False

#%%
def test_thinking_model():
    """测试带思维过程的模型"""
    logging.info(f"\n【测试3】思维过程测试 - 模型: gemini-2.5-pro-maxthinking")
    
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        
        messages = [
            {"role": "user", "content": "计算：23 × 47 = ?"}
        ]
        
        logging.info(f"发送消息: {messages[0]['content']}")
        
        response = client.chat.completions.create(
            model="gemini-2.5-pro-maxthinking",
            messages=messages,
            stream=True
        )
        
        logging.info("接收响应:")
        has_reasoning = False
        reasoning_parts = []
        content_parts = []
        
        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                has_reasoning = True
                reasoning_parts.append(chunk.choices[0].delta.reasoning_content)
            
            if chunk.choices[0].delta.content:
                content_parts.append(chunk.choices[0].delta.content)
        
        if has_reasoning:
            logging.info(f"[推理过程]: {''.join(reasoning_parts)}")
        
        logging.info(f"[最终答案]: {''.join(content_parts)}")
        
        if has_reasoning:
            logging.info("✓ 思维过程测试成功（包含推理过程）")
        else:
            logging.info("✓ 测试成功（但未检测到推理过程）")
        
        return True
        
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
    
    # 测试2：非流式聊天（使用Flash模型速度快）
    results['non_stream'] = test_chat_completion("gemini-2.5-flash", stream=False)
    
    # 测试3：流式聊天
    results['stream'] = test_chat_completion("gemini-2.5-flash", stream=True)
    
    # 测试4：思维过程
    results['thinking'] = test_thinking_model()
    
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

