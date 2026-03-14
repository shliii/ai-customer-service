import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 大模型配置
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DEFAULT_MODEL = "glm-4"  # 免费可用的模型
TEMPERATURE = 0.1        # 意图识别用低随机性，回复生成用0.7