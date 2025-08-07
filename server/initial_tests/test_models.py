# test_models.py
from models import Event, ChatQueryInput, Feedback
from pydantic import ValidationError
import uuid

def test_event_model():
    print("Testing Event model...")
    
    # Test valid Event
    try:
        event = Event(
            uuid=str(uuid.uuid4()),
            event="test_event",
            properties={"key": "value", "number": 42}
        )
        print(f"Valid Event created: {event.event}")
    except ValidationError as e:
        print(f"Event validation failed: {e}")
    
    # Test invalid Event (missing required fields)
    try:
        event = Event(event="test_event")  # Missing uuid and properties
        print(f"Invalid Event should have failed but didn't")
    except ValidationError as e:
        print(f"Invalid Event correctly rejected: {e}")

def test_chat_query_input_model():
    print("\nTesting ChatQueryInput model...")
    
    # Test valid ChatQueryInput
    try:
        chat_input = ChatQueryInput(
            text="Hello, how are you?",
            uuid=str(uuid.uuid4()),
            session_id="session_123"
        )
        print(f"Valid ChatQueryInput created: {chat_input.text[:20]}...")
    except ValidationError as e:
        print(f"ChatQueryInput validation failed: {e}")
    
    # Test invalid ChatQueryInput (missing required fields)
    try:
        chat_input = ChatQueryInput(text="Hello")  # Missing uuid and session_id
        print(f"Invalid ChatQueryInput should have failed but didn't")
    except ValidationError as e:
        print(f"Invalid ChatQueryInput correctly rejected: {e}")

def test_feedback_model():
    print("\nTesting Feedback model...")
    
    # Test valid Feedback with feedback
    try:
        feedback = Feedback(
            uuid=str(uuid.uuid4()),
            session_id="session_123",
            msg_index=1,
            feedback="This was helpful!"
        )
        print(f"Valid Feedback created with feedback: {feedback.feedback}")
    except ValidationError as e:
        print(f"Feedback validation failed: {e}")
    
    # Test valid Feedback without feedback (optional field)
    try:
        feedback = Feedback(
            uuid=str(uuid.uuid4()),
            session_id="session_123",
            msg_index=2
        )
        print(f"Valid Feedback created without feedback: {feedback.feedback}")
    except ValidationError as e:
        print(f"Feedback validation failed: {e}")
    
    # Test invalid Feedback (missing required fields)
    try:
        feedback = Feedback(uuid=str(uuid.uuid4()))  # Missing session_id and msg_index
        print(f"Invalid Feedback should have failed but didn't")
    except ValidationError as e:
        print(f"Invalid Feedback correctly rejected: {e}")

def test_model_serialization():
    print("\nTesting model serialization...")
    
    # Test Event serialization
    event = Event(
        uuid=str(uuid.uuid4()),
        event="test_event",
        properties={"key": "value"}
    )
    event_dict = event.dict()
    print(f"Event serialized to dict: {event_dict}")
    
    # Test ChatQueryInput serialization
    chat_input = ChatQueryInput(
        text="Test message",
        uuid=str(uuid.uuid4()),
        session_id="session_123"
    )
    chat_dict = chat_input.dict()
    print(f"ChatQueryInput serialized to dict: {chat_dict}")
    
    # Test Feedback serialization
    feedback = Feedback(
        uuid=str(uuid.uuid4()),
        session_id="session_123",
        msg_index=1,
        feedback="Great response!"
    )
    feedback_dict = feedback.dict()
    print(f"Feedback serialized to dict: {feedback_dict}")

if __name__ == "__main__":
    print("🧪 Testing Pydantic Models\n")
    test_event_model()
    test_chat_query_input_model()
    test_feedback_model()
    test_model_serialization()
    print("\nAll model tests completed!") 