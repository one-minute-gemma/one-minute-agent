"""
OneMinute Emergency Agent - Simple Implementation

A simple demonstration of the nagents framework for emergency scenarios.
Uses the new agent factory system with proper tool organization.
"""
import sys
import logging
from pathlib import Path
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and visual separators"""
    
    # Color mapping for different log levels
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    
    # Special colors for different components
    COMPONENT_COLORS = {
        'OneMinuteAgent': Fore.BLUE + Style.BRIGHT,
        'OllamaProvider': Fore.MAGENTA,
        'ToolRegistry': Fore.CYAN,
        'EmergencyAgent': Fore.BLUE + Style.BRIGHT
    }
    
    def format(self, record):
        # Add visual delimiter at start
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        component_color = self.COMPONENT_COLORS.get(record.name, Fore.WHITE)
        
        # Special handling for OneMinuteAgent - show as REASONING instead of INFO
        level_display = record.levelname
        if record.name == 'OneMinuteAgent' and record.levelname == 'INFO':
            level_display = 'REASONING'
            log_color = Fore.YELLOW + Style.BRIGHT  # Make reasoning more prominent
        
        # Format with colors and borders
        formatted = (
            f"{Fore.BLACK + Back.WHITE}[LOG]{Style.RESET_ALL} "
            f"{Fore.CYAN}{self.formatTime(record, '%H:%M:%S')}{Style.RESET_ALL} "
            f"│ {component_color}{record.name}{Style.RESET_ALL} "
            f"│ {log_color}{level_display}{Style.RESET_ALL} "
            f"│ {record.getMessage()}"
        )
        
        return formatted

# Configure logging with custom colored formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove default handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add console handler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter())
logger.addHandler(console_handler)

sys.path.append(str(Path(__file__).parent))

from .config.config import config
from nagents import OllamaProvider
from .agents import create_agent, create_operator_agent, create_victim_assistant_agent, AgentType

def create_emergency_agent(
        agent_type: AgentType = "operator",
        model_name: str = "gemma3n:e2b", 
        show_thinking: bool = True, 
        max_iterations: int = 2,
        always_use_reasoning: bool = True
        ):
    """
    Create a ready-to-use emergency agent.
    
    Args:
        agent_type: Type of agent ("operator" or "victim-assistant")
        model_name: Ollama model to use (default: gemma3n:e2b)
        show_thinking: Whether to show the agent's reasoning process
        max_iterations: Maximum reasoning iterations
        
    Returns:
        Configured emergency agent with appropriate tools
    """
    
    model_provider = OllamaProvider(model_name)
    
    agent = create_agent(
        agent_type=agent_type,
        model_provider=model_provider,
        max_iterations=max_iterations,
        show_thinking=show_thinking,
        always_use_reasoning=always_use_reasoning
    )
    
    return agent

# Convenience function for operator agent
def create_operator_emergency_agent(model_name: str = "gemma3n:e2b", show_thinking: bool = False, max_iterations: int = 2):
    """Create a 911 operator communication agent."""
    model_provider = OllamaProvider(model_name)
    return create_operator_agent(model_provider, max_iterations, show_thinking)

def main():
    """Interactive demo with agent type selection"""
    
    print("🚨 OneMinute Emergency Response System")
    print("=====================================")
    print("1. Operator Agent - Communicates with 911 dispatchers")
    print("2. Victim Assistant Agent - Provides direct help to victims")
    print()
    
    choice = input("Select agent type (1 for Operator, 2 for Victim Assistant): ").strip()
    
    if choice == "1":
        agent_type = "operator"
        agent_name = "911 Operator Agent"
        prompt_prefix = "911 Operator: "
        max_iter = 2
    elif choice == "2":
        agent_type = "victim-assistant" 
        agent_name = "Victim Assistant Agent"
        prompt_prefix = "Emergency Victim: "
        max_iter = 3
    else:
        print("Invalid choice, defaulting to Operator Agent")
        agent_type = "operator"
        agent_name = "911 Operator Agent" 
        prompt_prefix = "911 Operator: "
        max_iter = 2
    
    print(f"\n🚨 Creating {agent_name}...")
    agent = create_emergency_agent(
        agent_type=agent_type,
        show_thinking=True,
        max_iterations=max_iter
    )
    
    print(f"✅ {agent_name} ready!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
    
    while True:
        user_input = input(prompt_prefix)
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        # Visual separator before processing
        print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔄 Processing your request...{Style.RESET_ALL}")
        
        result = agent.chat(user_input)
        
        # Visual separator after processing
        print(f"{Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN + Style.BRIGHT}{agent_name}:{Style.RESET_ALL} {result.content}")
        
        if result.tools_executed:
            print(f"{Fore.CYAN}🔧 Tools used: {len(result.tools_executed)}{Style.RESET_ALL}")
        if result.metadata:
            print(f"{Fore.BLUE}📊 Metadata: {result.metadata}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{'═' * 60}{Style.RESET_ALL}")
        print()  # Extra space for readability

if __name__ == "__main__":
    main() 