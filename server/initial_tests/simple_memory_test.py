# simple_memory_test.py - Quick memory testing
import uuid
from memory import Memory, MessageType, ToolInvocation

def quick_test():
    print("Quick Memory Test\n")
    
    # Create memory instance
    test_uuid = str(uuid.uuid4())
    memory = Memory(test_uuid, "test_session", last_n=3)
    
    print(f"Created memory for session: {test_uuid[:8]}...")
    
    # Add some messages
    memory.add_message(MessageType.HUMAN, "What's the weather like?")
    memory.add_message(MessageType.AI, "I don't have access to weather data.")
    memory.add_message(MessageType.HUMAN, "Tell me about Princeton")
    
    # Test tool invocation
    tool = ToolInvocation("search", "Princeton University", "Princeton is a prestigious university in NJ")
    memory.add_message(MessageType.AI, "Princeton University is located in Princeton, New Jersey.", tool)
    
    # Get recent messages
    messages = memory.get_messages()
    print(f"\nRecent messages ({len(messages)}):")
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg}")
    
    # Get summary
    summary = memory.get_conversation_summary()
    print(f"\nSummary: {summary['message_count']} messages")
    
    print("\nQuick test completed!")

if __name__ == "__main__":
    quick_test() 