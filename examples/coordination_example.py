"""
Example demonstrating inter-agent communication in emergency response system.

This example shows how the Victim Assistant and Operator agents communicate
through the message bus system during an emergency scenario.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path so we can import nagents and one_minute_agent
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import asyncio
import time
from datetime import datetime
from typing import Dict, Any

from nagents import OllamaProvider
from one_minute_agent.agents import create_agent
from one_minute_agent.communication import (
    get_coordination_system, get_message_bus, get_event_logger,
    MessageType, Priority, AgentRole
)


class CommunicationDemo:
    """Demo class to showcase inter-agent communication"""
    
    def __init__(self):
        self.coordination_system = get_coordination_system()
        self.message_bus = get_message_bus()
        self.event_logger = get_event_logger()
        
        # Initialize agents
        model_provider = OllamaProvider("gemma3n:e2b")
        
        self.victim_agent = create_agent(
            agent_type="victim-assistant",
            model_provider=model_provider,
            max_iterations=2,
            show_thinking=False,
            enable_communication=True
        )
        
        self.operator_agent = create_agent(
            agent_type="operator", 
            model_provider=model_provider,
            max_iterations=2,
            show_thinking=False,
            enable_communication=True
        )
        
        print("✅ Agents initialized and registered with coordination system")
        
    def simulate_emergency_scenario(self):
        """Simulate a complete emergency response scenario"""
        print("\n🚨 EMERGENCY SCENARIO: House Fire")
        print("=" * 50)
        
        # Step 1: Victim reports emergency
        print("\n1️⃣ Victim reports emergency...")
        victim_response = self.victim_agent.chat(
            "There's a fire in my house! I'm trapped on the second floor and there's smoke everywhere. "
            "The front door is blocked by flames. I can see fire trucks outside but I can't get out!"
        )
        print(f"🗣️ Victim Agent Response: {victim_response.content}")
        
        # Give a moment for message processing
        time.sleep(1)
        
        # Step 2: Operator responds to situation
        print("\n2️⃣ Operator responds to emergency...")
        operator_response = self.operator_agent.chat(
            "I have a victim trapped on second floor of house fire at 1247 Oak Street. "
            "Front exit blocked, victim reports smoke inhalation risk. Fire department on scene. "
            "Need to coordinate rescue and provide victim guidance."
        )
        print(f"🎧 Operator Response: {operator_response.content}")
        
        # Step 3: Show communication log
        print("\n3️⃣ Inter-Agent Communication Log:")
        print("-" * 40)
        self.display_communication_log()
        
        # Step 4: Continue scenario with follow-up
        print("\n4️⃣ Follow-up communication...")
        victim_followup = self.victim_agent.chat(
            "I found a back window! I can see the fire ladder outside. Should I try to get to it?"
        )
        print(f"🗣️ Victim Follow-up: {victim_followup.content}")
        
        time.sleep(1)
        
        operator_followup = self.operator_agent.chat(
            "Victim has located back window exit with fire ladder visible. "
            "Coordinating with fire team for safe evacuation."
        )
        print(f"🎧 Operator Follow-up: {operator_followup.content}")
        
        # Final communication log
        print("\n5️⃣ Final Communication Log:")
        print("-" * 40)
        self.display_communication_log()
        
    def display_communication_log(self):
        """Display the inter-agent communication log"""
        messages = self.message_bus.get_message_history()
        
        if not messages:
            print("No inter-agent messages logged.")
            return
        
        for message in messages:
            timestamp = message.timestamp.strftime("%H:%M:%S")
            sender = message.sender.value.upper()
            recipient = message.recipient.value.upper()
            msg_type = message.message_type.value.upper().replace('_', ' ')
            priority = message.priority.name
            
            print(f"{timestamp} [{priority}] {sender} → {recipient}: {msg_type}")
            
            # Show message content summary
            if message.message_type == MessageType.SITUATION_UPDATE:
                situation = message.content.get('situation_description', 'N/A')
                print(f"    📋 Situation: {situation[:60]}...")
                
            elif message.message_type == MessageType.DISPATCH_UPDATE:
                status = message.content.get('dispatch_status', 'N/A')
                eta = message.content.get('responder_eta', 'N/A')
                print(f"    🚒 Dispatch: {status}, ETA: {eta} min")
                
            elif message.message_type == MessageType.STATUS_UPDATE:
                status = message.content.get('status', 'N/A')
                print(f"    ℹ️ Status: {status}")
                
            print()
    
    def get_streamlit_log_format(self) -> list:
        """Get communication log in format suitable for Streamlit display"""
        messages = self.message_bus.get_message_history()
        log_entries = []
        
        for message in messages:
            timestamp = message.timestamp.strftime("%H:%M:%S %p")
            
            # Map message types to display categories
            if message.message_type == MessageType.SITUATION_UPDATE:
                log_type = "COMMUNICATION"
                content = f"Victim reports: \"{message.content.get('situation_description', 'Emergency situation')[:50]}...\""
                
            elif message.message_type == MessageType.DISPATCH_UPDATE:
                log_type = "DISPATCH" 
                status = message.content.get('dispatch_status', 'dispatched')
                eta = message.content.get('responder_eta', 'Unknown')
                content = f"Dispatch update: {status}, ETA {eta} minutes"
                
            elif message.message_type == MessageType.STATUS_UPDATE:
                log_type = "STATUS"
                content = f"Status: {message.content.get('status', 'Update')}"
                
            elif message.message_type == MessageType.EMERGENCY_ESCALATION:
                log_type = "CRITICAL"
                content = f"ESCALATION: {message.content.get('escalation_reason', 'Emergency escalation')}"
                
            else:
                log_type = "SYSTEM"
                content = f"{message.message_type.value}: {str(message.content)[:50]}..."
            
            log_entries.append({
                'time': timestamp,
                'type': log_type,
                'message': content
            })
        
        return log_entries


def main():
    """Run the communication demo"""
    print("🚨 Emergency Response Inter-Agent Communication Demo")
    print("=" * 60)
    
    try:
        demo = CommunicationDemo()
        demo.simulate_emergency_scenario()
        
        print("\n✅ Demo completed successfully!")
        print("\nThis demo shows how the two agents communicate through:")
        print("- Structured message types (SituationUpdate, DispatchUpdate)")
        print("- Priority-based message handling")
        print("- Event logging and coordination")
        print("- Real-time message bus communication")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 