"""
Terminal interface for the one-minute emergency agent.
Uses the OMHandler with agentic reasoning and iterative tool execution.
"""
import logging
from pathlib import Path
    
from .one_min_handler import OMHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('one_minute_agent.log'),
        logging.StreamHandler()
    ]
)

def initialize_handler():
    """Initialize the OMHandler with error handling"""
    try:
        return OMHandler("gemma3n:e2b")
    except Exception as e:
        print(f"❌ Failed to initialize handler: {e}")
        print("Make sure Ollama is running and you have the model:")
        print("  ollama pull gemma3n:e2b")
        raise

def display_tool_results(tools_used):
    """Display the results of executed tools in a user-friendly format"""
    if not tools_used:
        return
        
    print(f"\n📊 Agent executed {len(tools_used)} tools during reasoning:")
    for i, tool in enumerate(tools_used, 1):
        tool_name = tool['tool']
        result = tool['result']
        
        if result.get('status') == 'success':
            print(f"  {i}. ✅ {tool_name}:")
            data = result.get('data', {})
            
            if tool_name == "get_health_metrics":
                print(f"     💓 Heart Rate: {data.get('heart_rate')} bpm")
                print(f"     🩸 Blood Pressure: {data.get('blood_pressure')} mmHg")  
                print(f"     🫁 Blood Oxygen: {data.get('blood_oxygen')}%")
                
            elif tool_name == "get_user_location":
                print(f"     📍 Location: {data.get('latitude')}, {data.get('longitude')}")
                
            elif tool_name == "get_audio_input":
                print(f"     🎙️ Audio: \"{data.get('audio')}\"")
                
            elif tool_name == "get_video_input":
                if 'error' in data:
                    print(f"     📹 Video Error: {data.get('error')}")
                else:
                    image_info = data.get('image', {})
                    print(f"     📹 Image Captured: {image_info.get('filename')}")
                    print(f"     📝 Description: {data.get('description')}")
                    
            elif tool_name == "get_user_details":
                print(f"     👤 Name: {data.get('name')}")
                print(f"     🎂 Age: {data.get('age')}")
                print(f"     🩸 Blood Type: {data.get('blood_type')}")
                print(f"     💊 Medications: {data.get('current_medications')}")
                print(f"     🚨 Allergies: {data.get('allergies')}")
        else:
            print(f"  {i}. ❌ {tool_name}: {result.get('message', 'Unknown error')}")

def display_agent_status():
    """Display information about the agentic capabilities"""
    print("\n🤖 **EMERGENCY-OPTIMIZED AGENTIC AI:**")
    print("  • ⚡ SPEED-FIRST: Maximum 2 iterations for rapid response")
    print("  • 🚫 NO REDUNDANCY: Prevents calling the same tool twice")
    print("  • 🎯 DECISIVE ACTION: Answers as soon as sufficient info is available")
    print("  • 🧠 Smart reasoning with thought → action → observation loops")
    print("  • 📞 Emergency response methodology optimized for 911 operators")
    print("  • ⏱️ Prioritizes life-saving speed over thoroughness")

def main():
    print("🚨 Emergency-Optimized Agent - Agentic AI Mode")
    print("=" * 70)
    
    try:
        handler = initialize_handler()
        print(f"✅ Agentic Emergency Agent initialized successfully!")
    except Exception:
        print("❌ Failed to start the agent. Exiting...")
        return
    
    display_agent_status()
    
    print("\nType 'quit', 'exit' or 'bye' to exit")
    print("Type 'clear' to clear conversation history")
    print("Type 'status' to see agentic capabilities")
    print("\nEmergency Simulation Prompts:")
    print("- 'What's your emergency?'")
    print("- 'Tell me what happened'")
    print("- 'Can you describe the situation?'")
    print("- 'I need a full assessment of the person'")
    print("=" * 70)
    print("\n911 Operator simulation ready...\n")
    
    while True:
        try:
            user_input = input("911 Operator: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Emergency session ended. Stay safe!")
                break
                
            if user_input.lower() == 'clear':
                handler.clear_history()
                print("🗑️ Conversation history cleared.")
                continue
                
            if user_input.lower() == 'status':
                display_agent_status()
                continue
                
            if not user_input:
                continue
            
            # Process the message with agentic reasoning
            response, tools_used = handler.handle_message(user_input)
            
            print(f"\n🎯 **Final Agent Response:**")
            print(f"Emergency Agent: {response}")
            
            # Display tool execution summary
            display_tool_results(tools_used)
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Emergency session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            logging.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    main()