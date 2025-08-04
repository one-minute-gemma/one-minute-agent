# OneMinute Emergency Response System

A dual-agent AI system designed to provide comprehensive emergency assistance through two specialized agents. Built on the `nagents` framework.

## What It Does

The OneMinute system provides emergency assistance through two complementary agents:

### 1. Operator Agent
- **Communicates with 911 dispatchers** on behalf of the person experiencing the emergency
- **Monitors emergency situations** using various sensors and tools
- **Provides real-time information** about the person's condition, location, and situation
- **Uses third-person perspective** - always refers to "the person" or "the patient", never "I" or "me"

### 2. Victim Assistant Agent  
- **Provides direct help to victims** during emergency situations
- **Offers first aid guidance** using traditional and RAG-powered medical advice
- **Gives immediate assistance** while emergency responders are en route
- **Uses medical knowledge base** to provide relevant emergency care instructions

## Key Features

### Operator Agent Capabilities
- **Health Monitoring**: Check vital signs, symptoms, and medical conditions
- **Location Tracking**: Provide precise location information for emergency responders
- **Audio/Video Analysis**: Assess situations through environmental monitoring
- **Crisis Management**: Call emergency contacts, activate alarms, log incidents
- **Clinical Communication**: Uses third-person language appropriate for 911 operators

### Victim Assistant Agent Capabilities
- **First Aid Guidance**: Provides step-by-step emergency care instructions
- **Medical Knowledge**: RAG-powered medical advice system
- **Location Services**: Emergency location reporting
- **Direct Support**: Immediate assistance while help is en route
- **Compassionate Communication**: Direct, supportive interaction with victims

## Installation & Setup

### Prerequisites
- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running
- Model: `gemma3n:e2b`

### Install Required Model
```bash
ollama pull gemma3n:e2b
```

### Run the Agent
```bash
# From the project root
python -m one-minute-agent
```

## Usage

When you run the system, you'll be prompted to select which agent to use:

```
🚨 OneMinute Emergency Response System
=====================================
1. Operator Agent - Communicates with 911 dispatchers
2. Victim Assistant Agent - Provides direct help to victims

Select agent type (1 for Operator, 2 for Victim Assistant): 
```

### Example Interactions

#### Operator Agent (911 Communication)
```
911 Operator: What's your emergency?
Operator Agent: The person is experiencing severe chest pain. Heart rate is elevated at 120 BPM. They are conscious but in distress. Location is 123 Main Street, Apartment 4B.

911 Operator: How long has this been happening?
Operator Agent: The chest pain started approximately 15 minutes ago according to audio analysis. The person has a history of heart conditions.
```

#### Victim Assistant Agent (Direct Help)
```
You: I'm having chest pain and shortness of breath
Victim Assistant: I'm here to help you through this emergency. Based on your symptoms, this could be serious. First, try to stay calm and sit down. Are you able to take an aspirin right now if you're not allergic? I'm also getting your location to help emergency services find you.
```

## Architecture

```
one-minute-agent/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point (python -m one-minute-agent)
├── app.py               # Main application and agent factory
├── agents/              # Agent implementations
│   ├── __init__.py      # Agent factory and selection logic
│   ├── operator/        # 911 Operator Agent
│   │   ├── agent.py     # OneMinuteAgent class
│   │   ├── tools.py     # Operator-specific tools
│   │   └── prompts/     # Operator prompts
│   └── victim_assistant/ # Victim Assistant Agent
│       ├── agent.py     # VictimAssistantAgent class
│       ├── tools.py     # Victim assistance tools
│       └── prompts/     # Victim assistance prompts
├── config/              # Configuration management
│   ├── config.py        # Configuration loader
│   └── config.json      # Settings and parameters
└── stuff/               # Sample data and assets
    ├── sample_audio/    # Audio samples for testing
    └── sample_images/   # Image samples for testing
```

## Configuration

The agent's behavior can be customized through `config/config.json`:

```json
{
  "model_name": "gemma3n:e2b",
  "max_iterations": 2,
  "show_thinking": true,
  "emergency_contacts": [...]
}
```

## Available Emergency Tools

### Operator Agent Tools
- **`get_health_metrics()`** - Monitor vital signs and health metrics
- **`get_user_location()`** - Provide precise location information
- **`get_audio_input()`** - Analyze audio for emergency indicators
- **`get_video_input()`** - Visual assessment of the situation
- **`get_user_details()`** - Access medical history and personal information
- **`call_emergency_contact()`** - Contact predefined emergency contacts
- **`activate_alarm()`** - Trigger alerts to notify nearby people
- **`log_incident()`** - Record emergency incident details

### Victim Assistant Agent Tools
- **`get_emergency_location()`** - Provide location information for emergency services
- **`get_first_aid_advice()`** - Traditional first aid guidance system
- **`get_rag_medical_advice()`** - RAG-powered medical knowledge system

## Reasoning Process

The agent uses a structured reasoning approach:

1. **Assessment Phase**: Gather information using available tools
2. **Analysis Phase**: Evaluate the severity and type of emergency
3. **Communication Phase**: Provide clear, actionable information to operators

### Example Reasoning
```json
{
  "thought": "I need to assess the person's current health status to provide accurate information to the 911 operator",
  "action": "get_health_status",
  "actionInput": {}
}
```

## Emergency Response Priorities

1. **Life-threatening conditions** (breathing, consciousness, severe bleeding)
2. **Location information** for emergency responder dispatch
3. **Patient details** and relevant medical history
4. **Environmental hazards** or access issues

## Development

### Key Classes

- **`OneMinuteAgent`**: Operator agent for 911 communication
- **`VictimAssistantAgent`**: Direct victim assistance agent
- **`EmergencyToolsProvider`**: Provides operator-specific tools
- **`VictimAssistantToolsProvider`**: Provides victim assistance tools
- **`Config`**: Configuration management

### Extending the Agents

To add new tools to either agent:

1. Define the tool function in the appropriate `agents/{agent_type}/tools.py`
2. Add it to the `tools` array in that file
3. The tool will be automatically registered through the provider system

### Testing

The agent includes sample data in the `stuff/` directory for testing various emergency scenarios with audio and visual inputs.

## Important Notes

### Operator Agent
- **Third-Person Perspective**: Always speaks about "the person" experiencing the emergency, never using first-person pronouns
- **Clinical Language**: Uses appropriate medical and emergency response terminology
- **Decisive Communication**: Optimized for quick, clear responses to 911 dispatchers

### Victim Assistant Agent
- **Direct Communication**: Speaks directly to the victim using second-person ("you")
- **Compassionate Tone**: Provides reassuring, supportive guidance
- **Action-Oriented**: Focuses on immediate steps the victim can take

### Both Agents
- **Local Processing**: All processing happens locally through Ollama - no external API calls required
- **Time-Critical**: Optimized for emergency response scenarios

## See Also

- [nagents framework documentation](../nagents/README.md)
- [Main project README](../README.md) 