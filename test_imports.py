"""
Test script to verify all imports are working correctly
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing Import Paths")
    print("=" * 30)
    
    try:
        print("1️⃣ Testing nagents import...")
        from nagents import OllamaProvider
        print("   ✅ nagents imported successfully")
    except Exception as e:
        print(f"   ❌ nagents import failed: {e}")
        return False
    
    try:
        print("2️⃣ Testing one_minute_agent.agents import...")
        from one_minute_agent.agents import create_agent
        print("   ✅ agents imported successfully")
    except Exception as e:
        print(f"   ❌ agents import failed: {e}")
        return False
        
    try:
        print("3️⃣ Testing one_minute_agent.communication import...")
        from one_minute_agent.communication import (
            get_coordination_system, get_message_bus, get_event_logger,
            MessageType, Priority, AgentRole
        )
        print("   ✅ communication imported successfully")
    except Exception as e:
        print(f"   ❌ communication import failed: {e}")
        return False
    
    try:
        print("4️⃣ Testing communication tools...")
        from one_minute_agent.communication.communication_tools import (
            create_victim_communication_tools,
            create_operator_communication_tools
        )
        
        # Test creating the tools
        victim_tools = create_victim_communication_tools()
        operator_tools = create_operator_communication_tools()
        
        print(f"   ✅ Victim communication tools: {len(victim_tools)} tools")
        print(f"   ✅ Operator communication tools: {len(operator_tools)} tools")
        
    except Exception as e:
        print(f"   ❌ communication tools failed: {e}")
        return False
        
    print("\n✅ All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 Ready to run coordination example!")
    else:
        print("\n❌ Fix import issues before running examples") 