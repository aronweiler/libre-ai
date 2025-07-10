import tiktoken

class ConversationManager:
    def __init__(self, max_tokens=100000, summarizer=None):
        self.max_tokens = max_tokens
        self.summarizer = summarizer  # Should be a callable that summarizes conversation
        self.history = []  # List of dicts: {"role": "user"|"ai", "content": str}
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self._enforce_token_limit()

    def get_history(self):
        return self.history

    def _count_tokens(self, text):
        return len(self.tokenizer.encode(text))

    def _total_tokens(self):
        return sum(self._count_tokens(m["content"]) for m in self.history)

    def _enforce_token_limit(self):
        total = self._total_tokens()
        if total > self.max_tokens:
            self._summarize_conversation()

    def _summarize_conversation(self):
        if not self.summarizer:
            # Remove oldest messages until under limit
            while self._total_tokens() > self.max_tokens and len(self.history) > 1:
                self.history.pop(0)
            return
        # Use summarizer to compact conversation
        summary = self.summarizer(self.history)
        self.history = [{"role": "system", "content": summary}]

    def notify_user_of_summarization(self, notify_func):
        notify_func("Conversation was summarized to stay within token limit.")
