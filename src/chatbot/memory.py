class Memory:
    def __init__(self):
        self.conversation_history = []

    def add_message(self, user_message, bot_response):
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_response
        })

    def get_history(self):
        return self.conversation_history

    def clear_memory(self):
        self.conversation_history = []