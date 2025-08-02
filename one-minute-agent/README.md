# OneMinute Emergency Agent

A specialized AI agent designed to assist during emergency situations by serving as an intelligent monitoring system that communicates with 911 operators. Built on the `nagents` framework.

## What It Does

The OneMinute agent acts as an AI monitoring system that:

- **Monitors a person in emergency situations** using various sensors and tools
- **Communicates with 911 operators** on behalf of the person experiencing the emergency
- **Provides real-time information** about the person's condition, location, and situation
- **Uses third-person perspective** - always refers to "the person" or "the patient", never "I" or "me"

## Key Features

### Emergency Response Capabilities
- **Health Monitoring**: Check vital signs, symptoms, and medical conditions
- **Location Tracking**: Provide precise location information for emergency responders
- **Audio/Video Analysis**: Assess situations through environmental monitoring
- **Crisis Detection**: Automatically identify life-threatening situations
- **Fast Decision Making**: Optimized for quick, decisive responses in emergency scenarios

### Communication Style
- Uses clinical, third-person language appropriate for 911 operators
- Prioritizes life-threatening information first
- Provides clear, actionable information
- Avoids ambiguity in emergency situations

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

When you run the agent, it will start a command-line interface simulating a 911 operator interaction:

```
🚨 Creating Emergency Agent...
911 Operator: What's your emergency?
OneMinute Agent: [Agent analyzes situation and responds with emergency information]
```

### Example Interaction
```
911 Operator: What's your emergency?
OneMinute Agent: The person is experiencing severe chest pain. Heart rate is elevated at 120 BPM. They are conscious but in distress. Location is 123 Main Street, Apartment 4B.

911 Operator: How long has this been happening?
OneMinute Agent: The chest pain started approximately 15 minutes ago according to audio analysis. The person has a history of heart conditions.
```

## Architecture

```
one-minute-agent/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point (python -m one-minute-agent)
├── app.py               # Main application and agent factory
├── agent.py             # OneMinuteAgent class (extends BaseAgent)
├── tools.py             # Emergency-specific tools
├── config/              # Configuration management
│   ├── config.py        # Configuration loader
│   └── config.json      # Settings and parameters
├── prompts/             # Agent prompts
│   └── prompt.md        # Emergency response prompt template
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

The agent has access to specialized emergency tools:

- **`get_health_status()`** - Monitor vital signs and health metrics
- **`get_current_location()`** - Provide precise location information
- **`analyze_audio_for_emergency()`** - Analyze ambient audio for emergency indicators
- **`capture_and_analyze_image()`** - Visual assessment of the situation
- **`call_emergency_contact()`** - Contact predefined emergency contacts
- **`get_emergency_medical_history()`** - Access relevant medical history

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

- **`OneMinuteAgent`**: Main agent class that extends `BaseAgent`
- **`EmergencyToolsProvider`**: Provides emergency-specific tools
- **`Config`**: Configuration management

### Extending the Agent

To add new emergency tools:

1. Define the tool function in `tools.py`
2. Register it with the `EmergencyToolsProvider`
3. Update the tool registry in `app.py`

### Testing

The agent includes sample data in the `stuff/` directory for testing various emergency scenarios with audio and visual inputs.

## Important Notes

- **Third-Person Perspective**: The agent always speaks about "the person" experiencing the emergency, never using first-person pronouns
- **Clinical Language**: Uses appropriate medical and emergency response terminology
- **Decisive Communication**: Optimized for quick, clear responses in time-critical situations
- **Local Processing**: All processing happens locally through Ollama - no external API calls required

## See Also

- [nagents framework documentation](../nagents/README.md)
- [Main project README](../README.md) 