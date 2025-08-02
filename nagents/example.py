"""
Example usage of the Nagents Agent Framework.
Shows how to use the emergency agent example.
"""
import logging
from nagents.examples.emergency import create_emergency_agent

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    """Simple example of emergency agent usage"""
    
    print("🚨 Creating Emergency Agent...")
    agent = create_emergency_agent(show_thinking=True)
    
    while True:
        user_input = input("911 Operator: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
            
        result = agent.chat(user_input)
        print(f"OneMinute Agent: {result.content}")
        
        if result.tools_executed:
            print(f"Tools used: {len(result.tools_executed)}")
        if result.metadata:
            print(f"Metadata: {result.metadata}")

if __name__ == "__main__":
    main() 