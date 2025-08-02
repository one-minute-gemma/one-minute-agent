"""
Example usage of the OneMinuteAgent API.
Shows how easy it is to integrate with frontends.
"""
import logging
from ollama_agent import create_emergency_agent

# Set up logging to see the thinking process
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
        print(f"OneMinute Agent: {result['response']}")
        
        if result['tools_executed']:
            print(f"Tools used: {len(result['tools_executed'])}")

if __name__ == "__main__":
    main() 