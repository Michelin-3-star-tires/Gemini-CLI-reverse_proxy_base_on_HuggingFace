#%%
"""
测试Function Calling功能
"""
import os
import json
from openai import OpenAI

# 强制设置终端编码为UTF-8
os.system('chcp 65001 > nul')

#%%
# 配置客户端 - 使用Hugging Face部署的服务
client = OpenAI(
    api_key="123456",
    base_url="https://ch862747537-my-cloud-service.hf.space/v1"
)

#%%
# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如：2+2、10*5"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

#%%
print("=" * 60)
print("测试1: 基础Function Calling - 询问天气")
print("=" * 60)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "北京今天天气怎么样？"}
    ],
    tools=tools,
    tool_choice="auto"
)

print(f"\n模型响应:")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(f"Content: {response.choices[0].message.content}")

if response.choices[0].message.tool_calls:
    print(f"\n工具调用:")
    for tool_call in response.choices[0].message.tool_calls:
        print(f"  - 函数: {tool_call.function.name}")
        print(f"    参数: {tool_call.function.arguments}")

#%%
print("\n" + "=" * 60)
print("测试2: 流式Function Calling")
print("=" * 60)

stream = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "帮我算一下 123 * 456 等于多少"}
    ],
    tools=tools,
    tool_choice="auto",
    stream=True
)

print("\n流式输出:")
for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
        if delta.tool_calls:
            print(f"\n[工具调用: {delta.tool_calls}]")
        if chunk.choices[0].finish_reason:
            print(f"\n[Finish: {chunk.choices[0].finish_reason}]")

#%%
print("\n" + "=" * 60)
print("测试3: 完整的Function Calling循环")
print("=" * 60)

# 第一轮：模型决定调用工具
messages = [
    {"role": "user", "content": "上海现在的温度是多少摄氏度？"}
]

print("\n第一轮请求...")
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=messages,
    tools=tools
)

print(f"模型回复: {response.choices[0].message.content}")
print(f"Finish reason: {response.choices[0].finish_reason}")

if response.choices[0].message.tool_calls:
    # 添加assistant消息
    messages.append(response.choices[0].message)
    
    # 模拟执行工具并返回结果
    for tool_call in response.choices[0].message.tool_calls:
        print(f"\n调用工具: {tool_call.function.name}")
        print(f"参数: {tool_call.function.arguments}")
        
        # 模拟天气数据
        function_response = {
            "city": "上海",
            "temperature": 22,
            "unit": "celsius",
            "condition": "晴朗"
        }
        
        # 添加工具结果
        messages.append({
            "role": "tool",
            "name": tool_call.function.name,
            "tool_call_id": tool_call.id,
            "content": json.dumps(function_response, ensure_ascii=False)
        })
    
    # 第二轮：让模型基于工具结果生成最终答案
    print("\n第二轮请求...")
    final_response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages,
        tools=tools
    )
    
    print(f"\n最终回答:")
    print(final_response.choices[0].message.content)

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)

