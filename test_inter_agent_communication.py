"""
Focused test to verify inter-agent communication is working properly
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import time
from nagents import OllamaProvider
from one_minute_agent.agents import create_agent
from one_minute_agent.communication import (
    get_coordination_system, get_message_bus, get_event_logger,
    MessageType, Priority, AgentRole
)

def test_communication_flow():
    """Test the complete communication flow between agents"""
    print("🧪 Testing Inter-Agent Communication Flow")
    print("=" * 50)
    
    # Initialize communication system
    coordination_system = get_coordination_system()
    message_bus = get_message_bus()
    event_logger = get_event_logger()
    
    # Clear any previous messages
    message_bus.clear_history()
    
    # Initialize agents
    model_provider = OllamaProvider("gemma3n:e2b")
    
    victim_agent = create_agent(
        agent_type="victim-assistant",
        model_provider=model_provider,
        max_iterations=4,  # More iterations for communication
        show_thinking=False,
        enable_communication=True
    )
    
    operator_agent = create_agent(
        agent_type="operator", 
        model_provider=model_provider,
        max_iterations=4,  # More iterations for communication
        show_thinking=False,
        enable_communication=True
    )
    
    print("✅ Agents initialized with communication enabled")
    
    # Test 1: Victim Assistant should send situation update
    print("\n1️⃣ Testing Victim Assistant Communication...")
    print("Input: 'Help! There's a fire in my kitchen and I can't get out the front door!'")
    
    victim_response = victim_agent.chat(
        "Help! There's a fire in my kitchen and I can't get out the front door! "
        "The smoke is getting thick and I'm having trouble breathing!"
    )
    
    print(f"Response: {victim_response.content[:100]}...")
    
    # Check for messages
    time.sleep(1)
    messages = message_bus.get_message_history()
    print(f"📨 Messages sent by Victim Assistant: {len(messages)}")
    
    for msg in messages:
        print(f"   - {msg.message_type.value} (Priority: {msg.priority.name})")
    
    # Test 2: Operator should respond with dispatch info
    print("\n2️⃣ Testing Operator Communication...")
    print("Input: 'What's your emergency? I need location and victim status for dispatch.'")
    
    operator_response = operator_agent.chat(
        "What's your emergency? I need the victim's exact location, current condition, "
        "and situation details so I can dispatch the appropriate emergency services."
    )
    
    print(f"Response: {operator_response.content[:100]}...")
    
    # Check for new messages
    time.sleep(1)
    new_messages = message_bus.get_message_history()
    operator_messages = [m for m in new_messages if m.sender == AgentRole.OPERATOR]
    print(f"📨 Messages sent by Operator: {len(operator_messages)}")
    
    for msg in operator_messages:
        print(f"   - {msg.message_type.value} (Priority: {msg.priority.name})")
    
    # Show all messages
    print("\n3️⃣ Complete Communication Log:")
    print("-" * 40)
    
    all_messages = message_bus.get_message_history()
    if not all_messages:
        print("❌ No inter-agent messages found!")
        return False
    
    for i, msg in enumerate(all_messages, 1):
        timestamp = msg.timestamp.strftime("%H:%M:%S")
        sender = msg.sender.value.upper()
        recipient = msg.recipient.value.upper()
        msg_type = msg.message_type.value.upper().replace('_', ' ')
        priority = msg.priority.name
        
        print(f"{i}. {timestamp} [{priority}] {sender} → {recipient}: {msg_type}")
        
        # Show content preview
        if msg.message_type == MessageType.SITUATION_UPDATE:
            situation = msg.content.get('situation_description', 'N/A')
            print(f"   Content: {situation[:60]}...")
        elif msg.message_type == MessageType.DISPATCH_UPDATE:
            status = msg.content.get('dispatch_status', 'N/A')
            eta = msg.content.get('responder_eta', 'N/A')
            print(f"   Content: Status={status}, ETA={eta}min")
        elif msg.message_type == MessageType.EMERGENCY_ESCALATION:
            reason = msg.content.get('escalation_reason', 'N/A')
            print(f"   Content: {reason[:60]}...")
        
        print()
    
    # Analysis
    situation_updates = [m for m in all_messages if m.message_type == MessageType.SITUATION_UPDATE]
    dispatch_updates = [m for m in all_messages if m.message_type == MessageType.DISPATCH_UPDATE]
    escalations = [m for m in all_messages if m.message_type == MessageType.EMERGENCY_ESCALATION]
    
    print("📊 Message Analysis:")
    print(f"   - Situation Updates: {len(situation_updates)}")
    print(f"   - Dispatch Updates: {len(dispatch_updates)}")
    print(f"   - Emergency Escalations: {len(escalations)}")
    
    # Success criteria
    success = len(all_messages) > 0 and (len(situation_updates) > 0 or len(escalations) > 0)
    
    if success:
        print("\n✅ Inter-agent communication is working!")
        if len(dispatch_updates) == 0:
            print("⚠️ Note: Operator didn't send dispatch updates - may need more explicit prompting")
    else:
        print("\n❌ Inter-agent communication is not working properly")
    
    return success

if __name__ == "__main__":
    try:
        success = test_communication_flow()
        if success:
            print("\n🎉 Communication test passed!")
        else:
            print("\n💥 Communication test failed!")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
