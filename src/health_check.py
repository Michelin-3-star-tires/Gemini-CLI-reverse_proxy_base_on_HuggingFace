#%%
"""
服务健康检查脚本

此脚本用于检查 geminicli2api 服务是否正常运行
"""
import os

# 强制设置终端编码为UTF-8
os.system('chcp 65001 > nul')

#%%
import logging
import requests
import sys
import time

# --- 标准化路径管理 ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_dir)

LOGS_DIR = os.path.join(project_root, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# --- 配置日志 ---
log_file = os.path.join(LOGS_DIR, 'health_check.log')
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
# --- 配置参数 ---
BASE_URL = "http://localhost:8888"
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

logging.info("=" * 60)
logging.info("服务健康检查开始")
logging.info(f"目标URL: {BASE_URL}")
logging.info(f"最大重试次数: {MAX_RETRIES}")
logging.info("=" * 60)

#%%
def check_health():
    """检查健康端点"""
    logging.info("\n【检查1】健康端点检查")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"尝试 {attempt}/{MAX_RETRIES}...")
            url = f"{BASE_URL}/health"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'healthy':
                logging.info(f"✓ 服务健康: {data}")
                return True
            else:
                logging.warning(f"⚠️ 服务状态异常: {data}")
                return False
                
        except requests.exceptions.ConnectionError:
            logging.error(f"✗ 连接失败: 无法连接到 {url}")
            if attempt < MAX_RETRIES:
                logging.info(f"等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
        except requests.exceptions.Timeout:
            logging.error("✗ 请求超时")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            logging.error(f"✗ 检查失败: {str(e)}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    
    return False

#%%
def check_root_endpoint():
    """检查根端点"""
    logging.info("\n【检查2】根端点检查")
    
    try:
        url = f"{BASE_URL}/"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if 'name' in data and data['name'] == 'geminicli2api':
            logging.info(f"✓ 根端点正常")
            logging.info(f"  项目名称: {data.get('name')}")
            logging.info(f"  版本: {data.get('version')}")
            logging.info(f"  描述: {data.get('description', '')[:50]}...")
            return True
        else:
            logging.warning("⚠️ 根端点响应格式异常")
            return False
            
    except Exception as e:
        logging.error(f"✗ 根端点检查失败: {str(e)}")
        return False

#%%
def check_authentication(api_password="your_password"):
    """检查认证功能"""
    logging.info("\n【检查3】认证功能检查")
    
    try:
        url = f"{BASE_URL}/v1/models"
        
        # 测试无认证
        logging.info("  测试无认证访问...")
        response = requests.get(url, timeout=5)
        if response.status_code == 401:
            logging.info("  ✓ 正确拒绝未认证请求")
        else:
            logging.warning(f"  ⚠️ 未认证请求返回状态码: {response.status_code}")
        
        # 测试有认证
        logging.info("  测试认证访问...")
        headers = {"Authorization": f"Bearer {api_password}"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            model_count = len(data.get('data', []))
            logging.info(f"  ✓ 认证成功，获取到 {model_count} 个模型")
            return True
        else:
            logging.warning(f"  ⚠️ 认证请求返回状态码: {response.status_code}")
            return False
            
    except Exception as e:
        logging.error(f"✗ 认证检查失败: {str(e)}")
        return False

#%%
def check_docker_container():
    """检查Docker容器状态"""
    logging.info("\n【检查4】Docker容器检查")
    
    try:
        # 检查容器是否运行
        result = os.popen("docker ps --filter name=geminicli2api --format '{{.Status}}'").read().strip()
        
        if result:
            logging.info(f"✓ Docker容器正在运行")
            logging.info(f"  状态: {result}")
            return True
        else:
            logging.warning("⚠️ 未找到运行中的geminicli2api容器")
            
            # 检查是否有停止的容器
            stopped = os.popen("docker ps -a --filter name=geminicli2api --format '{{.Status}}'").read().strip()
            if stopped:
                logging.info(f"  发现已停止的容器: {stopped}")
            
            return False
            
    except Exception as e:
        logging.error(f"✗ Docker检查失败: {str(e)}")
        return False

#%%
def run_all_checks():
    """运行所有检查"""
    logging.info("\n" + "=" * 60)
    logging.info("开始运行所有检查")
    logging.info("=" * 60)
    
    results = {}
    
    # 检查1：健康端点
    results['health'] = check_health()
    
    # 检查2：根端点
    results['root'] = check_root_endpoint()
    
    # 检查3：认证
    # 注意：这需要修改为实际的密码
    # results['auth'] = check_authentication("your_actual_password")
    
    # 检查4：Docker容器
    results['docker'] = check_docker_container()
    
    # 总结
    logging.info("\n" + "=" * 60)
    logging.info("检查结果汇总")
    logging.info("=" * 60)
    
    for check_name, success in results.items():
        status = "✓ 正常" if success else "✗ 异常"
        logging.info(f"{check_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    logging.info(f"\n总计: {passed}/{total} 项检查通过")
    
    if passed == total:
        logging.info("🎉 所有检查通过！服务运行正常")
        return 0
    else:
        logging.error(f"⚠️ {total - passed} 项检查失败")
        logging.error("\n故障排查建议:")
        
        if not results.get('health'):
            logging.error("  1. 检查服务是否已启动: docker-compose ps")
            logging.error("  2. 查看服务日志: docker-compose logs")
            logging.error("  3. 确认端口未被占用: netstat -ano | findstr :8888")
        
        if not results.get('docker'):
            logging.error("  4. 启动服务: docker-compose up -d")
            logging.error("  5. 检查配置文件: 确认.env文件存在且配置正确")
        
        return 1
    
    logging.info("=" * 60)

#%%
if __name__ == "__main__":
    exit_code = run_all_checks()
    sys.exit(exit_code)

