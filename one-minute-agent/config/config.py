"""
Configuration management for the OneMinuteAgent system.
Centralized configuration loading and access.
"""
import json
import os
from typing import Dict, Any
from pathlib import Path

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Get config path relative to this file
            config_dir = Path(__file__).parent
            config_path = config_dir / "config.json"
        
        self._config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
    
    @property
    def default_model_name(self) -> str:
        """Get the default model name"""
        return self._config.get("model", {}).get("default_name", "gemma3n:latest")
    
    @property
    def model_provider(self) -> str:
        """Get the model provider"""
        return self._config.get("model", {}).get("provider", "ollama")
    
    @property
    def max_iterations(self) -> int:
        """Get the maximum iterations for agent reasoning"""
        return self._config.get("agent", {}).get("max_iterations", 2)
    
    @property
    def default_show_thinking(self) -> bool:
        """Get the default show_thinking setting"""
        return self._config.get("agent", {}).get("show_thinking", False)
    
    @property
    def max_tools_per_conversation(self) -> int:
        """Get the maximum tools per conversation"""
        return self._config.get("tools", {}).get("max_tools_per_conversation", 2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'model.default_name')"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

# Global configuration instance
config = Config() 