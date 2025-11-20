"""
Conversation memory manager for the IT support agent.
Maintains chat history across turns.
"""


class ConversationMemory:
    """Manages conversation state and history."""
    
    def __init__(self):
        """Initialize empty conversation history."""
        self.messages = []
    
    def add_user_message(self, content: str):
        """Add a user message to history.
        
        Args:
            content: The user's message text
        """
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content: str):
        """Add an assistant message to history.
        
        Args:
            content: The assistant's message text
        """
        self.messages.append({
            "role": "assistant",
            "content": content
        })
    
    def add_system_message(self, content: str):
        """Add a system message to history.
        
        Args:
            content: The system message text
        """
        self.messages.append({
            "role": "system",
            "content": content
        })
    
    def get_history(self) -> list:
        """Get the full conversation history.
        
        Returns:
            List of message dictionaries
        """
        return self.messages.copy()
    
    def get_recent_history(self, n: int = 10) -> list:
        """Get the n most recent messages.
        
        Args:
            n: Number of recent messages to retrieve
            
        Returns:
            List of recent message dictionaries
        """
        return self.messages[-n:] if len(self.messages) > n else self.messages.copy()
    
    def clear(self):
        """Clear all conversation history."""
        self.messages = []
    
    def count_messages(self) -> int:
        """Get the total number of messages.
        
        Returns:
            Number of messages in history
        """
        return len(self.messages)
    
    def __repr__(self):
        return f"ConversationMemory(messages={self.count_messages()})"

