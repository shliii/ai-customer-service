import requests
from config import ZHIPU_API_KEY, ZHIPU_API_URL, DEFAULT_MODEL, TEMPERATURE

def detect_intent(user_input):
    """调用智谱API识别用户意图"""
    # 意图识别提示词（简洁、明确）
    prompt = f"""你是智能客服的意图识别助手，仅需从以下关键词中选择最匹配的一个回复：查订单、退款、物流、售后。若都不匹配，回复：我暂时无法帮助您，请联系人工客服（400-123-4567）"。用户输入：{user_input}"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_API_KEY}"
    }
    
    data = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE
    }

    try:
        response = requests.post(ZHIPU_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        intent = response.json()["choices"][0]["message"]["content"].strip()
        return intent
    except Exception as e:
        print(f"意图识别出错：{str(e)}")
        return "其他"