#!/usr/bin/env python3
"""
Chatbot with Memory Example
===========================

Demonstrates how to add persistent memory to a chatbot.
"""

import sys
sys.path.insert(0, '..')

from connection_core import MemoryEngine, MemoryConfig
from memory_engine import ConversationMemory, SemanticMemory


def create_chatbot_with_memory():
    """Create a chatbot with persistent memory."""

    # Initialize memory engine
    config = MemoryConfig(
        storage_path="chatbot_memory.db",
        max_memories=5000,
    )
    engine = MemoryEngine(config)

    # Create conversation and semantic memory
    conversation = ConversationMemory(engine, max_turns=50)
    semantic = SemanticMemory(engine)

    return engine, conversation, semantic


def process_message(
    message: str,
    conversation: ConversationMemory,
    semantic: SemanticMemory
) -> str:
    """Process a user message and generate response."""

    # Add user message to conversation
    conversation.add_turn("user", message)

    # Check for user info updates
    if "my name is" in message.lower():
        name = message.split("my name is")[-1].strip().rstrip(".")
        semantic.add_concept("user.name", name, importance=0.9)

    if "i prefer" in message.lower() or "i like" in message.lower():
        pref = message.split("prefer" if "prefer" in message.lower() else "like")[-1].strip()
        semantic.add_concept("user.preferences.mentioned", pref, importance=0.8)

    # Recall relevant memories for context
    relevant = conversation.search(message, limit=3)

    # Generate response (in real app, this would use an LLM)
    response = generate_response(message, relevant, semantic)

    # Add assistant response to conversation
    conversation.add_turn("assistant", response)

    return response


def generate_response(message: str, relevant_memories, semantic: SemanticMemory) -> str:
    """Generate a response (placeholder - would use LLM in production)."""

    # Check if we know the user's name
    user_name = semantic.get_concept("user.name")

    # Simple pattern matching for demo
    message_lower = message.lower()

    if "hello" in message_lower or "hi" in message_lower:
        if user_name:
            return f"Hello {user_name}! How can I help you today?"
        return "Hello! What's your name?"

    if "my name is" in message_lower:
        name = message.split("my name is")[-1].strip().rstrip(".")
        return f"Nice to meet you, {name}! I'll remember that."

    if "what is my name" in message_lower or "do you know my name" in message_lower:
        if user_name:
            return f"Your name is {user_name}!"
        return "I don't think you've told me your name yet."

    if "remember" in message_lower:
        return "Got it! I've stored that in my memory."

    # Use relevant memories for context
    if relevant_memories:
        context = "\n".join([f"- {m.content}" for m in relevant_memories[:2]])
        return f"Based on our conversation:\n{context}\n\nHow can I help further?"

    return "I understand. Tell me more or ask me anything!"


def main():
    print("=" * 50)
    print("Chatbot with Memory Demo")
    print("=" * 50)
    print("Type 'quit' to exit, 'stats' for memory stats")
    print("Try: 'My name is Alice', 'What is my name?'")
    print()

    engine, conversation, semantic = create_chatbot_with_memory()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                break

            if user_input.lower() == "stats":
                stats = engine.get_stats()
                print(f"\nMemory Stats:")
                print(f"  Total memories: {stats['total_memories']}")
                print(f"  Database size: {stats['database_size_kb']}KB")
                print()
                continue

            if user_input.lower() == "history":
                print("\nRecent conversation:")
                print(conversation.get_formatted(5))
                print()
                continue

            response = process_message(user_input, conversation, semantic)
            print(f"Bot: {response}")
            print()

        except KeyboardInterrupt:
            break

    print("\nGoodbye!")
    engine.close()


if __name__ == "__main__":
    main()
