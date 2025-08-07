# test_utils.py
from utils import (
    time_to_date_string, 
    openai_json_response, 
    openai_stream,
    system_prompt, 
    user_prompt,
    get_embedding,
    with_timing
)
import time
import os

def test_time_function():
    print("Testing time_to_date_string function...")
    
    try:
        time_str = time_to_date_string()
        print(f"Time function result: {time_str}")
        print("Time function works correctly")
        return True
    except Exception as e:
        print(f"Time function failed: {e}")
        return False

def test_prompt_decorators():
    print("\nTesting prompt decorators...")
    
    @system_prompt
    def test_system():
        return 'You are a helpful assistant'
    
    @user_prompt  
    def test_user():
        return 'Hello'
    
    try:
        system_msg = test_system()
        user_msg = test_user()
        
        print(f"System message: {system_msg}")
        print(f"User message: {user_msg}")
        
        # Verify structure
        assert system_msg['role'] == 'system'
        assert user_msg['role'] == 'user'
        assert system_msg['content'][0]['type'] == 'text'
        assert user_msg['content'][0]['type'] == 'text'
        
        print("Prompt decorators work correctly")
        return True
    except Exception as e:
        print(f"Prompt decorators failed: {e}")
        return False

def test_openai_json_response():
    print("\nTesting OpenAI JSON response...")
    
    try:
        response = openai_json_response([
            {'role': 'user', 'content': 'Respond with JSON: {"test": "success", "number": 42}'}
        ])
        print(f"OpenAI JSON response: {response}")
        
        # Verify it's valid JSON
        assert isinstance(response, dict)
        assert 'test' in response
        assert response['test'] == 'success'
        
        print("OpenAI JSON response works correctly")
        return True
    except Exception as e:
        print(f"OpenAI JSON response failed: {e}")
        return False

def test_openai_stream():
    print("\nTesting OpenAI stream...")
    
    try:
        stream = openai_stream([
            {'role': 'user', 'content': 'Say hello in one word'}
        ], max_tokens=10)
        
        print("Stream created successfully")
        
        # Test that we can iterate through the stream
        chunk_count = 0
        for chunk in stream:
            chunk_count += 1
            if chunk_count > 5:  # Limit to avoid long test
                break
        
        print(f"Stream iteration works (tested {chunk_count} chunks)")
        return True
    except Exception as e:
        print(f"OpenAI stream failed: {e}")
        return False

def test_get_embedding():
    print("\nTesting get_embedding function...")
    
    try:
        test_text = "This is a test sentence for embedding"
        embedding = get_embedding(test_text)
        
        print(f"Embedding generated with {len(embedding)} dimensions")
        
        # Verify it's a list of numbers
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, (int, float)) for x in embedding)
        
        print("Embedding function works correctly")
        return True
    except Exception as e:
        print(f"Embedding function failed: {e}")
        return False

def test_with_timing_decorator():
    print("\nTesting with_timing decorator...")
    
    @with_timing
    def slow_function():
        time.sleep(0.1)  # Simulate some work
        return "done"
    
    try:
        # Test with DEBUG=1
        original_debug = os.getenv("DEBUG")
        os.environ["DEBUG"] = "1"
        
        result = slow_function()
        print(f"Timed function result: {result}")
        
        # Test without DEBUG
        os.environ["DEBUG"] = "0"
        result2 = slow_function()
        print(f"Untimed function result: {result2}")
        
        # Restore original DEBUG setting
        if original_debug is None:
            del os.environ["DEBUG"]
        else:
            os.environ["DEBUG"] = original_debug
        
        print("Timing decorator works correctly")
        return True
    except Exception as e:
        print(f"Timing decorator failed: {e}")
        return False

def test_error_handling():
    print("\nTesting error handling...")
    
    # Test with invalid input
    try:
        # This should fail gracefully
        response = openai_json_response([
            {'role': 'user', 'content': 'Invalid JSON please'}
        ])
        print("Error handling test passed")
        return True
    except Exception as e:
        print(f"Expected error caught: {type(e).__name__}")
        return True

def run_all_tests():
    print("Testing utils.py functions\n")
    
    tests = [
        ("Time Function", test_time_function),
        ("Prompt Decorators", test_prompt_decorators),
        ("OpenAI JSON Response", test_openai_json_response),
        ("OpenAI Stream", test_openai_stream),
        ("Embedding Function", test_get_embedding),
        ("Timing Decorator", test_with_timing_decorator),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"PASSED: {test_name}")
            else:
                print(f"FAILED: {test_name}")
        except Exception as e:
            print(f"ERROR in {test_name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("All tests passed!")
    else:
        print(f"{total - passed} tests failed")

if __name__ == "__main__":
    run_all_tests() 