#!/usr/bin/env python3
"""
Test offline emergency location functionality
"""
import asyncio
from location import get_emergency_location

async def test_offline_mode():
    """Test the offline emergency location detection"""
    print("🧪 Testing Emergency Location - Offline Detection")
    print("=" * 60)
    
    print("📝 This test will show both online and offline scenarios")
    print("   (Offline will be simulated if internet is available)")
    
    # Test current connectivity
    location = await get_emergency_location()
    
    print("\n📋 EMERGENCY LOCATION RESULT:")
    print("=" * 60)
    
    print(f"🔌 CONNECTIVITY: {location.get('connectivity', 'UNKNOWN')}")
    print(f"📊 STATUS: {location['status']}")
    
    if location.get("connectivity") == "ONLINE":
        print(f"📍 LOCATION: {location.get('city', 'N/A')}, {location.get('region', 'N/A')}")
        print(f"🎯 COORDINATES: {location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}")
    
    elif location.get("connectivity") == "OFFLINE":
        print(f"📶 CONTEXT: {location.get('location_hint', 'No context available')}")
        
        loc_context = location.get("location_context", {})
        if loc_context:
            print(f"🏘️  AREA: {loc_context.get('description', 'Unknown')}")
            print(f"⏱️  EST. RESPONSE: {loc_context.get('estimated_response_time', 'Unknown')}")
        
        # Show guidance for AI
        guidance = location.get("emergency_guidance", {})
        if guidance:
            print(f"\n🤖 FOR AI AGENT:")
            print(f"   {guidance.get('for_ai', 'No guidance')}")
            print(f"   Available methods: {', '.join(guidance.get('location_methods', []))}")
    
    # Show Wi-Fi environment if available
    wifi_env = location.get("wifi_environment")
    if wifi_env:
        print(f"\n📶 WI-FI ENVIRONMENT:")
        print(f"   Networks: {wifi_env.get('networks_detected', 0)}")
        print(f"   Type: {wifi_env.get('environment_type', 'Unknown')}")
        if wifi_env.get('strongest_signal_dbm'):
            print(f"   Signal: {wifi_env.get('strongest_signal_dbm')}dBm")
    
    print("\n" + "=" * 60)
    print("✅ Offline detection test completed")

if __name__ == "__main__":
    asyncio.run(test_offline_mode()) 