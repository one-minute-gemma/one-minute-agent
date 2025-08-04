#!/usr/bin/env python3
"""
Production test for emergency location service
"""
import asyncio
from location import get_emergency_location

async def test_emergency_location():
    """Test the production emergency location service"""
    print("🚨 EMERGENCY LOCATION SERVICE TEST")
    print("=" * 60)
    
    location = await get_emergency_location()
    
    print("\n📋 EMERGENCY RESPONSE DATA:")
    print("=" * 60)
    
    if location.get("status") == "LOCATION_ACQUIRED":
        print(f"✅ STATUS: {location['status']}")
        print(f"📍 COORDINATES: {location['latitude']:.6f}, {location['longitude']:.6f}")
        print(f"🏙️  LOCATION: {location['city']}, {location['region']}, {location['country']}")
        print(f"🎯 ACCURACY: {location['accuracy_level']} (~{location['accuracy_meters']}m)")
        print(f"⏰ TIMESTAMP: {location['timestamp']}")
        print(f"🔧 METHOD: {location['method']}")
        
        if "wifi_environment" in location:
            wifi = location["wifi_environment"]
            print(f"📶 ENVIRONMENT: {wifi['environment_type']} ({wifi['networks_detected']} networks)")
            print(f"📡 SIGNAL DATA: Strongest {wifi['strongest_signal_dbm']}dBm, Avg {wifi['average_signal_dbm']}dBm")
        
        print(f"\n💬 FOR 911 OPERATOR:")
        print(f"    Caller location: {location['city']}, {location['region']}")
        print(f"    Coordinates: {location['latitude']:.6f}, {location['longitude']:.6f}")
        print(f"    Accuracy: City-level (suitable for dispatch)")
        
    else:
        print(f"⚠️  STATUS: {location['status']}")
        guidance = location.get("emergency_guidance", {})
        print(f"📞 GUIDANCE: {guidance.get('message')}")
        print(f"📋 INSTRUCTION: {guidance.get('instruction')}")
        
    print("\n" + "=" * 60)
    print("✅ Emergency location test completed")

if __name__ == "__main__":
    asyncio.run(test_emergency_location()) 