# test_memory.py
import uuid
import time
from memory import Memory, MessageType, ToolInvocation
from clients import print_database_state

def test_memory_basic():
    print("Testing basic Memory functionality...")
    
    # Create a new memory instance
    test_uuid = str(uuid.uuid4())
    test_session = "test_session_123"
    memory = Memory(test_uuid, test_session, last_n=5)
    
    print(f"Memory created for UUID: {test_uuid[:8]}...")
    print(f"Session ID: {test_session}")
    
    return memory

def test_add_messages(memory):
    print("\nTesting message addition...")
    
    # Add human message
    memory.add_message(MessageType.HUMAN, "Hello, how are you?")
    print("Added human message")
    
    # Add AI message
    memory.add_message(MessageType.AI, "I'm doing well, thank you for asking!")
    print("Added AI message")
    
    # Add message with tool use
    tool_use = ToolInvocation("search", "Princeton University", "Princeton University is located in Princeton, NJ")
    memory.add_message(MessageType.AI, "I found information about Princeton University.", tool_use)
    print("Added AI message with tool use")
    
    # Add more messages to test the limit
    for i in range(3):
        memory.add_message(MessageType.HUMAN, f"Message {i+1}")
        memory.add_message(MessageType.AI, f"Response {i+1}")
    
    print("Added additional messages")

def test_get_messages(memory):
    print("\nTesting message retrieval...")
    
    # Get recent messages
    messages = memory.get_recent_messages()
    print(f"Retrieved {len(messages)} recent messages")
    
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {msg['type']}: {msg['content'][:50]}...")
    
    # Get formatted messages for context
    formatted_messages = memory.get_messages()
    print(f"\nRetrieved {len(formatted_messages)} formatted messages")
    
    for i, msg_str in enumerate(formatted_messages):
        print(f"  {i+1}. {msg_str}")
    
    return messages

def test_conversation_summary(memory):
    print("\nTesting conversation summary...")
    
    summary = memory.get_conversation_summary()
    print(f"Conversation summary:")
    print(f"  - Message count: {summary['message_count']}")
    print(f"  - Last updated: {summary['last_updated']}")
    print(f"  - Session ID: {summary['session_id']}")
    print(f"  - UUID: {summary['uuid'][:8]}...")

def test_cache_functionality(memory):
    print("\nTesting cache functionality...")
    
    # Test that cache works (should be faster on second call)
    start_time = time.time()
    messages1 = memory.get_recent_messages()
    time1 = time.time() - start_time
    
    start_time = time.time()
    messages2 = memory.get_recent_messages()
    time2 = time.time() - start_time
    
    print(f"First retrieval: {time1:.4f}s")
    print(f"Second retrieval: {time2:.4f}s")
    print(f"Cache working: {len(messages1) == len(messages2)}")
    
    # Test cache clearing
    memory.clear_cache()
    print("Cache cleared")
    
    # Show database state
    print_database_state()

def test_tool_invocation():
    print("\nTesting ToolInvocation class...")
    
    tool = ToolInvocation("database_query", "SELECT * FROM users", "Found 5 users")
    tool_dict = tool.to_dict()
    
    print(f"ToolInvocation created:")
    print(f"  - Tool: {tool_dict['tool']}")
    print(f"  - Input: {tool_dict['input']}")
    print(f"  - Output: {tool_dict['output']}")

if __name__ == "__main__":
    print("Testing Memory System\n")
    
    try:
        # Run all tests
        memory = test_memory_basic()
        test_add_messages(memory)
        test_get_messages(memory)
        test_conversation_summary(memory)
        test_cache_functionality(memory)
        test_tool_invocation()
        
        print("\nAll memory tests completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc() 