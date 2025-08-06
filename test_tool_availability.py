"""
Test to check what communication tools are available to each agent
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from nagents import OllamaProvider
from one_minute_agent.agents import create_agent
from one_minute_agent.communication import (
    get_coordination_system, get_message_bus,
    create_victim_communication_tools, create_operator_communication_tools
)

def test_tool_availability():
    """Test what tools are available to each agent"""
    print("🔧 Testing Tool Availability")
    print("=" * 40)
    
    # Test communication tools directly
    print("1️⃣ Testing communication tool creation...")
    
    try:
        victim_comm_tools = create_victim_communication_tools()
        print(f"✅ Victim communication tools: {len(victim_comm_tools)}")
        for tool in victim_comm_tools:
            print(f"   - {tool.name}: {tool.description}")
            
        operator_comm_tools = create_operator_communication_tools()
        print(f"✅ Operator communication tools: {len(operator_comm_tools)}")
        for tool in operator_comm_tools:
            print(f"   - {tool.name}: {tool.description}")
            
    except Exception as e:
        print(f"❌ Communication tool creation failed: {e}")
        return False
    
    # Test agent creation and tool registration
    print("\n2️⃣ Testing agent tool registration...")
    
    try:
        model_provider = OllamaProvider("gemma3n:e2b")
        
        victim_agent = create_agent(
            agent_type="victim-assistant",
            model_provider=model_provider,
            max_iterations=2,
            show_thinking=True,  # Enable to see reasoning
            enable_communication=True
        )
        
        # Check what tools the victim agent has
        if hasattr(victim_agent, 'tool_executor') and hasattr(victim_agent.tool_executor, 'registry'):
            registry = victim_agent.tool_executor.registry
            tools = registry.get_all_tools()
            print(f"✅ Victim agent has {len(tools)} total tools:")
            
            comm_tools = [t for t in tools if 'send_' in t.name or 'request_' in t.name]
            print(f"   Communication tools: {len(comm_tools)}")
            for tool in comm_tools:
                print(f"   - {tool.name}")
        
        operator_agent = create_agent(
            agent_type="operator",
            model_provider=model_provider,
            max_iterations=2,
            show_thinking=True,
            enable_communication=True
        )
        
        # Check what tools the operator agent has
        if hasattr(operator_agent, 'tool_executor') and hasattr(operator_agent.tool_executor, 'registry'):
            registry = operator_agent.tool_executor.registry
            tools = registry.get_all_tools()
            print(f"✅ Operator agent has {len(tools)} total tools:")
            
            comm_tools = [t for t in tools if 'send_' in t.name]
            print(f"   Communication tools: {len(comm_tools)}")
            for tool in comm_tools:
                print(f"   - {tool.name}")
        
        print("\n3️⃣ Testing simple tool execution...")
        
        # Try to manually trigger a communication tool
        message_bus = get_message_bus()
        message_bus.clear_history()
        
        # Test victim agent with explicit instruction
        print("Testing victim agent with explicit communication instruction...")
        response = victim_agent.chat(
            "EMERGENCY: House fire! I'm trapped! You MUST use the send_situation_update tool to notify the operator immediately!"
        )
        
        print(f"Response: {response.content[:100]}...")
        
        # Check messages
        messages = message_bus.get_message_history()
        print(f"Messages sent: {len(messages)}")
        
        return len(messages) > 0
        
    except Exception as e:
        print(f"❌ Agent creation/testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tool_availability()
    if success:
        print("\n✅ Tool availability test passed!")
    else:
        print("\n❌ Tool availability test failed!") 