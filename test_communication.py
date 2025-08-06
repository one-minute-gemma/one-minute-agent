"""
Simple test script to verify inter-agent communication is working
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from one_minute_agent.communication import (
    get_coordination_system, get_message_bus, get_event_logger,
    create_situation_update, create_dispatch_update,
    MessageType, Priority, AgentRole
)

def test_communication_system():
    """Test the communication system components"""
    print("🧪 Testing Inter-Agent Communication System")
    print("=" * 50)
    
    # Get system components
    coordination_system = get_coordination_system()
    message_bus = get_message_bus()
    event_logger = get_event_logger()
    
    print("✅ Communication system components initialized")
    
    # Test 1: Create and send a situation update
    print("\n1️⃣ Testing Situation Update...")
    situation_msg = create_situation_update(
        situation="House fire with victim trapped on second floor",
        victim_status={"conscious": True, "mobile": True, "injuries": "smoke inhalation risk"},
        hazards=["fire", "smoke", "blocked exit"],
        needs=["evacuation guidance", "medical assessment"]
    )
    
    success = message_bus.publish(situation_msg)
    print(f"   Message sent: {success}")
    print(f"   Message ID: {situation_msg.id}")
    
    # Test 2: Create and send a dispatch update
    print("\n2️⃣ Testing Dispatch Update...")
    dispatch_msg = create_dispatch_update(
        eta=4,
        responder_types=["fire", "medical"],
        instructions="Move to back window, fire ladder will be positioned for rescue",
        status="en_route"
    )
    
    success = message_bus.publish(dispatch_msg)
    print(f"   Message sent: {success}")
    print(f"   Message ID: {dispatch_msg.id}")
    
    # Test 3: Check message history
    print("\n3️⃣ Testing Message History...")
    history = message_bus.get_message_history()
    print(f"   Total messages: {len(history)}")
    
    for i, msg in enumerate(history, 1):
        print(f"   {i}. {msg.sender.value} → {msg.recipient.value}: {msg.message_type.value}")
    
    # Test 4: Check event logging
    print("\n4️⃣ Testing Event Logger...")
    log_entries = event_logger.get_entries()
    print(f"   Total log entries: {len(log_entries)}")
    
    for entry in log_entries[-3:]:  # Show last 3 entries
        print(f"   {entry.format_for_display()}")
    
    print("\n✅ Communication system test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_communication_system()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc() 