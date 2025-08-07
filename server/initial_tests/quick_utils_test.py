# quick_utils_test.py - Quick test for utils.py
from utils import time_to_date_string, openai_json_response, system_prompt, user_prompt, get_embedding

def quick_test():
    print("Quick utils.py test\n")
    
    # Test time function
    print("Time function:", time_to_date_string())
    
    # Test prompt decorators
    @system_prompt
    def test_system():
        return 'You are a helpful assistant'
    
    @user_prompt  
    def test_user():
        return 'Hello'
    
    system_msg = test_system()
    user_msg = test_user()
    print("Prompt decorators work:", system_msg['role'], user_msg['role'])
    
    # Test embedding function
    try:
        embedding = get_embedding("test sentence")
        print(f"Embedding works: {len(embedding)} dimensions")
    except Exception as e:
        print(f"Embedding failed: {e}")
    
    # Test OpenAI JSON response
    try:
        response = openai_json_response([
            {'role': 'user', 'content': 'Respond with JSON: {"test": "success"}'}
        ])
        print("OpenAI JSON response works:", response)
    except Exception as e:
        print(f"OpenAI JSON response failed: {e}")
    
    print("\nQuick test completed!")

if __name__ == "__main__":
    quick_test() 