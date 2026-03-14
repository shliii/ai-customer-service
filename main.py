import requests

from config import ZHIPU_API_KEY, ZHIPU_API_URL, DEFAULT_MODEL
from conversation import ConversationManager
from intent_recognizer import detect_intent
from knowledge_base import get_answer_by_intent

class CustomerServiceAgent:
    def __init__(self):
        self.conv_manager = ConversationManager()
        self.api_key = ZHIPU_API_KEY

    def generate_general_reply(self, context):
        """未匹配到知识库时，调用大模型生成通用回复"""
        prompt = """
        你是友好的电商智能客服，语气礼貌、专业，若无法解答用户问题，则根据用户提问回答，跟他聊天。
        """
        # 拼接上下文和提示词
        messages = context + [{"role": "user", "content": prompt}]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": DEFAULT_MODEL,
            "messages": messages,
            "temperature": 0.7  # 回复生成用稍高随机性，更自然
        }

        try:
            response = requests.post(ZHIPU_API_URL, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"抱歉，暂时无法解答您的问题，请联系人工客服：400-123-4567（错误：{str(e)}）"

    def get_reply(self, user_input):
        """核心方法：获取用户回复"""
        # 1. 记录用户输入到上下文
        self.conv_manager.add_message("user", user_input)
        
        # 2. 识别意图
        intent = detect_intent(user_input)
        
        # 3. 匹配知识库或生成通用回复
        answer = get_answer_by_intent(intent)
        if answer:
            reply = f"您好，{answer}"
        else:
            # 调用大模型生成回复
            context = self.conv_manager.get_context()
            reply = self.generate_general_reply(context)
        
        # 4. 记录回复到上下文
        self.conv_manager.add_message("assistant", reply)
        return reply

if __name__ == "__main__":
    # 检查API密钥
    if not ZHIPU_API_KEY:
        print("错误：请在.env文件中配置ZHIPU_API_KEY！")
        exit(1)
    
    # 初始化Agent
    agent = CustomerServiceAgent()
    print("===== 智能客服已启动 =====")
    print("输入“退出”结束对话，输入“清空”清空聊天记录\n")
    
    # 交互循环
    while True:
        user_input = input("你：")
        if user_input.strip() == "退出":
            print("客服：感谢您的咨询，祝您生活愉快！")
            break
        if user_input.strip() == "清空":
            agent.conv_manager.clear_context()
            print("客服：已清空您的聊天记录，您可以继续提问～")
            continue
        # 获取并输出回复
        reply = agent.get_reply(user_input)
        print(f"客服：{reply}\n")