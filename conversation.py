class ConversationManager:
    def __init__(self, max_length=20):
        self.max_length = max_length
        self.context = []  # 格式：[{"role": "user/assistant", "content": "内容"}]

    def add_message(self, role, content):
        """添加消息到上下文，超过最大长度则删除最早的"""
        self.context.append({"role": role, "content": content})
        if len(self.context) > self.max_length:
            self.context.pop(0)

    def get_context(self):
        """获取完整上下文"""
        return self.context

    def clear_context(self):
        """清空上下文"""
        self.context = []

    def get_context_str(self):
        """将上下文转为字符串（备用）"""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.context])