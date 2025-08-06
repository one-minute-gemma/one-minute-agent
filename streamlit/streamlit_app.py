"""
Emergency Response Dashboard - Streamlit Implementation (FIXED VERSION)
Fixes: Chat scrolling, missing send buttons, swapped sides, cleaner log messages
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import os
import threading
import subprocess
import sys
from pathlib import Path

# Add the project path
sys.path.append(str(Path(__file__).parent.parent))

from nagents import OllamaProvider
from one_minute_agent.agents import create_agent
from one_minute_agent.communication import (
    get_coordination_system, get_message_bus, get_event_logger,
    MessageType, Priority, AgentRole
)

# Ollama initialization flag
OLLAMA_INITIALIZED = False
OLLAMA_AVAILABLE = False

def initialize_ollama_if_needed():
    """Initialize Ollama on first run"""
    global OLLAMA_INITIALIZED, OLLAMA_AVAILABLE
    
    if OLLAMA_INITIALIZED:
        return OLLAMA_AVAILABLE
    
    try:
        from .ollama_setup import initialize_ollama
        
        # Check if we're in a container environment (HF Spaces)
        if os.path.exists("/.dockerenv") or os.environ.get("SPACE_ID"):
            print("🐳 Detected container environment, initializing Ollama...")
            OLLAMA_AVAILABLE = initialize_ollama("gemma3n:e2b")
        else:
            print("💻 Local environment detected, assuming Ollama is already set up")
            OLLAMA_AVAILABLE = True
            
        OLLAMA_INITIALIZED = True
        return OLLAMA_AVAILABLE
        
    except Exception as e:
        print(f"❌ Ollama initialization failed: {e}")
        OLLAMA_INITIALIZED = True
        OLLAMA_AVAILABLE = False
        return False

def initialize_agents():
    """Initialize the emergency response agents with communication system"""
    if not st.session_state.agents_initialized:
        try:
            # Initialize Ollama if needed
            if initialize_ollama_if_needed():
                try:
                    model_provider = OllamaProvider("gemma3n:e2b")
                    st.session_state.provider_type = "Ollama (gemma3n:e2b)"
                    st.success("🎉 Using Ollama local model")
                except Exception as e:
                    print(f"⚠️ Ollama provider failed: {e}")
                    raise e
            else:
                # Fallback to mock provider
                from nagents.providers.mock_provider import MockProvider
                model_provider = MockProvider()
                st.session_state.provider_type = "Mock (Demo Mode)"
                st.info("🎭 Using demo mode - Ollama initialization failed")
            
            # Initialize communication system
            coordination_system = get_coordination_system()
            message_bus = get_message_bus()
            event_logger = get_event_logger()
            
            # Clear previous messages
            message_bus.clear_history()
            
            st.session_state.communication_system = {
                'coordination': coordination_system,
                'message_bus': message_bus,
                'event_logger': event_logger
            }
            
            # Create agents with communication enabled
            st.session_state.operator_agent = create_agent(
                agent_type="operator",
                model_provider=model_provider,
                max_iterations=3,
                show_thinking=False,
                enable_communication=True
            )
            
            st.session_state.victim_agent = create_agent(
                agent_type="victim-assistant", 
                model_provider=model_provider,
                max_iterations=3,
                show_thinking=False,
                enable_communication=True
            )
            
            st.session_state.agents_initialized = True
            
            # Add initial messages
            if not st.session_state.victim_messages:
                st.session_state.victim_messages.append({
                    'role': 'assistant',
                    'content': "Emergency services have been notified. Can you tell me about your situation?",
                    'timestamp': datetime.now().strftime("%H:%M %p")
                })
            
            if not st.session_state.operator_messages:
                st.session_state.operator_messages.append({
                    'role': 'assistant',
                    'content': 'Unit 23 dispatched to 1247 Oak Street. ETA 4 minutes.',
                    'timestamp': datetime.now().strftime("%H:%M %p")
                })
            
            # FIXED: Initialize with cleaner system log entries
            add_system_log("SYSTEM", f'Emergency call initiated - ID: {st.session_state.emergency_status["emergency_id"]}')
                
        except Exception as e:
            st.error(f"Failed to initialize agents: {str(e)}")
            st.session_state.agents_initialized = False

def add_system_log(message_type: str, content: str, source: str = "SYSTEM"):
    """Add entry to inter-agent communication log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.inter_agent_log.append({
        'time': timestamp,
        'type': message_type,
        'source': source,
        'message': content
    })

def update_communication_log():
    """Update the communication log with messages from the message bus"""
    if not st.session_state.communication_system:
        return
        
    message_bus = st.session_state.communication_system['message_bus']
    messages = message_bus.get_message_history()
    
    # Only process new messages
    new_message_count = len(messages)
    if new_message_count > st.session_state.last_message_count:
        new_messages = messages[st.session_state.last_message_count:]
        
        for message in new_messages:
            timestamp = message.timestamp.strftime("%H:%M:%S")
            
            # FIXED: Cleaner message formatting - only show relevant inter-agent communication
            if message.message_type == MessageType.SITUATION_UPDATE:
                log_type = "COMMUNICATION"
                source = "VICTIM→OPERATOR"
                situation = message.content.get('situation_description', 'Emergency situation')
                content = f"Situation: {situation[:60]}..."
                
            elif message.message_type == MessageType.DISPATCH_UPDATE:
                log_type = "DISPATCH"
                source = "OPERATOR→VICTIM"
                status = message.content.get('dispatch_status', 'dispatched')
                eta = message.content.get('responder_eta', 'Unknown')
                content = f"Responders {status}, ETA {eta} min"
                
            elif message.message_type == MessageType.STATUS_UPDATE:
                log_type = "STATUS"
                source = "SYSTEM"
                status = message.content.get('status', 'Update')
                content = status[:60]
                
            else:
                # Skip other message types to reduce clutter
                continue
            
            # Add to log
            st.session_state.inter_agent_log.append({
                'time': timestamp,
                'type': log_type,
                'source': source,
                'message': content
            })
        
        st.session_state.last_message_count = new_message_count

def render_chat_message(message: Dict[str, Any], agent_type: str = "assistant"):
    """Render a chat message with proper styling"""
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', '')
    
    css_class = f"chat-{role}" if role in ['user', 'assistant'] else f"chat-{agent_type}"
    
    if agent_type == "operator":
        agent_label = "🎧 911 Operator" if role == 'assistant' else "👤 Human Operator"
    else:
        agent_label = "🆘 Assistant" if role == 'assistant' else "👤 Victim"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div style="font-size: 11px; opacity: 0.7; margin-bottom: 4px;">
            {agent_label} {timestamp}
        </div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_inter_agent_log():
    """Render the inter-agent communication log"""
    st.markdown('<div class="column-header log">📡 Inter-Agent Log<br><small>Real-time system communications</small></div>', unsafe_allow_html=True)
    
    # Update log with latest messages
    update_communication_log()
    
    # FIXED: Use proper container with fixed height
    st.markdown('<div class="log-container">', unsafe_allow_html=True)
    
    # Show recent entries (last 30 to avoid clutter)
    recent_entries = st.session_state.inter_agent_log[-30:]
    
    for entry in recent_entries:
        log_class = f"log-{entry['type'].lower()}"
        
        st.markdown(f"""
        <div class="log-entry {log_class}">
            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="color: #9ca3af; font-weight: bold;">{entry['time']}</span>
                <span style="color: #6b7280; font-size: 10px;">{entry.get('source', '')}</span>
            </div>
            <div style="color: #d1d5db;">{entry['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_victim_view():
    """Render the simplified victim view"""
    # Status bar
    st.markdown(f"""
    <div class="status-bar">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 18px;">✅ {st.session_state.emergency_status['message']}</span><br>
                <small>Emergency services have been notified</small>
            </div>
            <div style="font-size: 24px; font-weight: bold;">
                🕒 ETA: {st.session_state.emergency_status['eta']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    st.markdown('<div class="column-header victim">🆘 Victim Assistant<br><small>Direct victim support</small></div>', unsafe_allow_html=True)
    
    # FIXED: Chat messages container with proper scrolling
    st.markdown('<div class="chat-container" id="victim-chat">', unsafe_allow_html=True)
    
    for message in st.session_state.victim_messages:
        render_chat_message(message, "assistant")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FIXED: Chat input with send button
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", key="victim_input", label_visibility="collapsed")
    with col2:
        send_button = st.button("📤 Send", key="victim_send", help="Send message", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if send_button and user_input:
        # Add user message
        st.session_state.victim_messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().strftime("%H:%M %p")
        })
        
        # Get agent response
        if st.session_state.agents_initialized:
            try:
                with st.spinner("Assistant is responding..."):
                    result = st.session_state.victim_agent.chat(user_input)
                    
                st.session_state.victim_messages.append({
                    'role': 'assistant',
                    'content': result.content,
                    'timestamp': datetime.now().strftime("%H:%M %p")
                })
                
                # Add communication log entry for victim interaction
                add_system_log("COMMUNICATION", f'Victim message received', "VICTIM→SYSTEM")
                
            except Exception as e:
                st.error(f"Agent error: {str(e)}")
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("### Quick emergency categories:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔥 Fire", key="quick_fire", help="Fire emergency"):
            quick_message = "There's a fire emergency! I need immediate help!"
            st.session_state.victim_messages.append({
                'role': 'user',
                'content': quick_message,
                'timestamp': datetime.now().strftime("%H:%M %p")
            })
            add_system_log("COMMUNICATION", "Quick action: Fire emergency", "VICTIM→SYSTEM")
            st.rerun()
    
    with col2:
        if st.button("🏥 Medical", key="quick_medical", help="Medical emergency"):
            quick_message = "I need medical help! Someone is injured!"
            st.session_state.victim_messages.append({
                'role': 'user',
                'content': quick_message,
                'timestamp': datetime.now().strftime("%H:%M %p")
            })
            add_system_log("COMMUNICATION", "Quick action: Medical emergency", "VICTIM→SYSTEM")
            st.rerun()
    
    with col3:
        if st.button("🚗 Accident", key="quick_accident", help="Accident emergency"):
            quick_message = "There's been an accident! People are hurt!"
            st.session_state.victim_messages.append({
                'role': 'user',
                'content': quick_message,
                'timestamp': datetime.now().strftime("%H:%M %p")
            })
            add_system_log("COMMUNICATION", "Quick action: Accident emergency", "VICTIM→SYSTEM")
            st.rerun()

def render_supervisor_view():
    """FIXED: Render the three-column supervisor dashboard with swapped sides"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # FIXED: Left column - Victim Assistant (swapped from operator)
    with col1:
        st.markdown('<div class="column-header victim">🆘 Victim Assistant<br><small>Direct victim support</small></div>', unsafe_allow_html=True)
        
        # FIXED: Victim chat container with proper height
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.victim_messages:
            render_chat_message(message, "assistant")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # FIXED: Victim input with send button
        col_input, col_send = st.columns([4, 1])
        with col_input:
            victim_input = st.text_input("Type your message...", key="victim_input_supervisor", label_visibility="collapsed")
        with col_send:
            victim_send_btn = st.button("📤", key="victim_send_supervisor", help="Send message", type="primary")
        
        if victim_send_btn and victim_input:
            st.session_state.victim_messages.append({
                'role': 'user',
                'content': victim_input,
                'timestamp': datetime.now().strftime("%H:%M %p")
            })
            
            # Get victim agent response  
            if st.session_state.agents_initialized:
                try:
                    with st.spinner("Assistant responding..."):
                        result = st.session_state.victim_agent.chat(victim_input)
                        
                    st.session_state.victim_messages.append({
                        'role': 'assistant',
                        'content': result.content,
                        'timestamp': datetime.now().strftime("%H:%M %p")
                    })
                    
                    # Add to communication log
                    add_system_log("COMMUNICATION", "Victim interaction", "VICTIM→SYSTEM")
                    
                except Exception as e:
                    st.error(f"Victim agent error: {str(e)}")
            
            st.rerun()
    
    # Center column - Inter-Agent Log
    with col2:
        render_inter_agent_log()
    
    # FIXED: Right column - 911 Operator (swapped from victim)
    with col3:
        st.markdown('<div class="column-header operator">🎧 911 Operator<br><small>Emergency dispatch coordination</small></div>', unsafe_allow_html=True)
        
        # FIXED: Operator chat container with proper height
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.operator_messages:
            render_chat_message(message, "operator")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # FIXED: Operator input with send button
        col_input, col_send = st.columns([4, 1])
        with col_input:
            operator_input = st.text_input("Type your message...", key="operator_input", label_visibility="collapsed")
        with col_send:
            operator_send_btn = st.button("📤", key="operator_send", help="Send message", type="primary")
        
        if operator_send_btn and operator_input:
            st.session_state.operator_messages.append({
                'role': 'user',
                'content': operator_input,
                'timestamp': datetime.now().strftime("%H:%M %p")
            })
            
            # Get operator agent response
            if st.session_state.agents_initialized:
                try:
                    with st.spinner("Operator processing..."):
                        result = st.session_state.operator_agent.chat(operator_input)
                        
                    st.session_state.operator_messages.append({
                        'role': 'assistant',
                        'content': result.content,
                        'timestamp': datetime.now().strftime("%H:%M %p")
                    })
                    
                    # Add to communication log
                    add_system_log("STATUS", "Operator response", "OPERATOR→SYSTEM")
                    
                except Exception as e:
                    st.error(f"Operator agent error: {str(e)}")
            
            st.rerun()

def main():
    """Main dashboard application"""
    
    # Initialize agents
    initialize_agents()
    
    # View toggle button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        current_view = "Supervisor View" if st.session_state.view_mode == "victim" else "Victim View"
        if st.button(f"📱 {current_view}", key="view_toggle"):
            st.session_state.view_mode = "supervisor" if st.session_state.view_mode == "victim" else "victim"
            st.rerun()
    
    # Communication status indicator
    if st.session_state.agents_initialized:
        message_count = len(st.session_state.communication_system['message_bus'].get_message_history()) if st.session_state.communication_system else 0
        st.markdown(f"""
        <div class="comm-status">
            🟢 Inter-Agent Communication System Active | Messages: {message_count}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("🟡 Initializing Communication System...")
    
    # Render appropriate view
    if st.session_state.view_mode == "victim":
        render_victim_view()
    else:
        render_supervisor_view()
    
    # FIXED: Simplified auto-refresh without aggressive reloading
    if st.session_state.agents_initialized:
        # Auto-scroll to bottom of chat containers
        st.markdown("""
        <script>
        function scrollToBottom() {
            const containers = document.querySelectorAll('.chat-container, .log-container');
            containers.forEach(container => {
                container.scrollTop = container.scrollHeight;
            });
        }
        setTimeout(scrollToBottom, 100);
        </script>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 