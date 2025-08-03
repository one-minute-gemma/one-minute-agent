"""
Emergency location tools using multiple geolocation methods.
Optimized for 911/emergency response situations with offline fallback.
"""
import subprocess
import json
import requests
import logging
import socket
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_emergency_location() -> Dict[str, Any]:
    """
    🚨 EMERGENCY LOCATION SERVICE
    
    Provides location data suitable for emergency dispatch.
    Handles both online and offline scenarios.
    
    Returns:
        dict: Emergency location data with coordinates, city, accuracy info, or offline context
    """
    print("🚨 EMERGENCY LOCATION REQUEST")
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "service": "emergency_location_v1.0"
    }
    
    # Check internet connectivity first
    internet_available = _check_internet_connectivity()
    
    if internet_available:
        # Primary Method: IP-based geolocation (when online)
        try:
            print("📡 Acquiring emergency location via IP geolocation...")
            
            response = requests.get(
                "http://ip-api.com/json/", 
                timeout=10,
                headers={"User-Agent": "Emergency-Location-Service/1.0"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result.update({
                        "status": "LOCATION_ACQUIRED",
                        "connectivity": "ONLINE",
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon"),
                        "accuracy_meters": 5000,
                        "accuracy_level": "CITY_LEVEL",
                        "city": data.get("city"),
                        "region": data.get("regionName"), 
                        "country": data.get("country"),
                        "timezone": data.get("timezone"),
                        "method": "IP_GEOLOCATION",
                        "confidence": "HIGH",
                        "emergency_note": "Location suitable for emergency dispatch"
                    })
                    
                    print(f"✅ LOCATION ACQUIRED")
                    print(f"📍 {data.get('city')}, {data.get('regionName')}")
                    print(f"🎯 Coordinates: {data.get('lat'):.6f}, {data.get('lon'):.6f}")
                    print(f"📏 Accuracy: ~5km radius (city-level)")
                    
                    # Add Wi-Fi context if available
                    wifi_context = _get_wifi_environment_context()
                    if wifi_context:
                        result["wifi_environment"] = wifi_context
                    
                    return result
                    
        except requests.RequestException as e:
            print(f"⚠️  IP geolocation failed: {e}")
            result["ip_geolocation_error"] = str(e)
        except Exception as e:
            print(f"⚠️  Unexpected error in IP geolocation: {e}")
            result["ip_geolocation_error"] = str(e)
    
    else:
        print("📵 No internet connection detected - using offline mode")
    
    # OFFLINE FALLBACK: Get what we can without internet
    print("🔍 Gathering offline location context...")
    
    wifi_context = _get_wifi_environment_context()
    offline_location_data = _get_offline_location_context(wifi_context)
    
    result.update({
        "status": "OFFLINE_MODE",
        "connectivity": "OFFLINE",
        "method": "OFFLINE_CONTEXT",
        "wifi_environment": wifi_context,
        "location_context": offline_location_data,
        "emergency_guidance": {
            "for_ai": "User is offline but emergency services can still locate them via:",
            "location_methods": [
                "Cell tower triangulation (if phone available)",
                "Enhanced 911 (E911) automatic location",
                "ISP registration address lookup",
                "Last known IP geolocation"
            ],
            "ai_instruction": "Inform 911 operator that caller is offline but location services are still available",
            "user_instruction": "Stay on the line - emergency services have multiple ways to find you even offline"
        }
    })
    
    if wifi_context and wifi_context.get("networks_detected", 0) > 0:
        result["location_hint"] = f"Located in {wifi_context['environment_type'].lower().replace('_', ' ')} area with {wifi_context['networks_detected']} Wi-Fi networks detected"
        print(f"📶 CONTEXT: {result['location_hint']}")
    else:
        result["location_hint"] = "Remote area with limited Wi-Fi networks"
        print("📶 CONTEXT: Remote or rural area detected")
    
    print("✅ OFFLINE CONTEXT GATHERED")
    return result

def _check_internet_connectivity() -> bool:
    """Check if internet connection is available"""
    try:
        # Try to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        try:
            # Fallback: try Cloudflare DNS
            socket.create_connection(("1.1.1.1", 53), timeout=3)
            return True
        except OSError:
            return False

def _get_offline_location_context(wifi_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate location context for offline scenarios"""
    if not wifi_context:
        return {
            "area_estimate": "REMOTE_RURAL",
            "description": "Very remote area - no Wi-Fi networks detected",
            "confidence": "LOW",
            "emergency_note": "Cell tower location will be primary method"
        }
    
    network_count = wifi_context.get("networks_detected", 0)
    environment = wifi_context.get("environment_type", "UNKNOWN")
    
    context_map = {
        "DENSE_URBAN": {
            "description": "Dense urban area - downtown or city center",
            "typical_response_time": "5-10 minutes",
            "confidence": "MEDIUM"
        },
        "URBAN": {
            "description": "Urban area - city or large town",
            "typical_response_time": "8-15 minutes", 
            "confidence": "MEDIUM"
        },
        "SUBURBAN": {
            "description": "Suburban area - residential neighborhood",
            "typical_response_time": "10-20 minutes",
            "confidence": "LOW"
        },
        "RURAL": {
            "description": "Rural area - countryside or small town",
            "typical_response_time": "15-30 minutes",
            "confidence": "LOW"
        }
    }
    
    area_info = context_map.get(environment, {
        "description": "Area type unknown",
        "typical_response_time": "Variable",
        "confidence": "VERY_LOW"
    })
    
    return {
        "area_estimate": environment,
        "description": area_info["description"],
        "network_density": f"{network_count} networks",
        "estimated_response_time": area_info["typical_response_time"],
        "confidence": area_info["confidence"],
        "emergency_note": f"Wi-Fi density suggests {area_info['description'].lower()}"
    }

def _get_wifi_environment_context() -> Optional[Dict[str, Any]]:
    """
    Get Wi-Fi environment context to supplement location data.
    Works offline - only scans nearby networks.
    """
    try:
        import objc
        
        bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
        objc.loadBundle('CoreWLAN', bundle_path=bundle_path, module_globals=globals())
        
        CWInterface = globals().get('CWInterface')
        if not CWInterface:
            return None
            
        interface = CWInterface.interface()
        if not interface or not interface.powerOn():
            return {
                "networks_detected": 0,
                "environment_type": "WIFI_DISABLED",
                "note": "Wi-Fi hardware disabled or unavailable"
            }
        
        scan_result, error = interface.scanForNetworksWithName_includeHidden_error_(None, True, None)
        if error or not scan_result:
            return {
                "networks_detected": 0,
                "environment_type": "SCAN_FAILED",
                "note": "Wi-Fi scan failed - may be hardware issue"
            }
        
        # Analyze Wi-Fi environment
        signal_strengths = []
        security_types = []
        
        for network in scan_result:
            try:
                rssi = network.rssiValue()
                if rssi:
                    signal_strengths.append(int(rssi))
                
                # Extract security info from string representation
                network_str = str(network)
                if "WPA2" in network_str:
                    security_types.append("WPA2")
                elif "WPA" in network_str:
                    security_types.append("WPA")
                elif "WEP" in network_str:
                    security_types.append("WEP")
                else:
                    security_types.append("Open")
            except:
                continue
        
        if signal_strengths:
            # Determine environment type
            network_count = len(signal_strengths)
            avg_signal = sum(signal_strengths) // len(signal_strengths)
            strongest_signal = max(signal_strengths)
            
            if network_count > 20 and strongest_signal > -40:
                environment = "DENSE_URBAN"
            elif network_count > 10:
                environment = "URBAN"
            elif network_count > 3:
                environment = "SUBURBAN"
            else:
                environment = "RURAL"
            
            return {
                "networks_detected": network_count,
                "environment_type": environment,
                "strongest_signal_dbm": strongest_signal,
                "average_signal_dbm": avg_signal,
                "security_mix": list(set(security_types)),
                "location_confidence_note": f"{environment.lower().replace('_', ' ')} area with {network_count} networks",
                "scan_timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "networks_detected": len(scan_result) if scan_result else 0,
                "environment_type": "NO_SIGNAL_DATA",
                "note": "Networks detected but no signal strength data available"
            }
            
    except Exception as e:
        logger.debug(f"Wi-Fi context scan failed: {e}")
        return {
            "networks_detected": 0,
            "environment_type": "SCAN_ERROR",
            "error": str(e),
            "note": "Wi-Fi scanning unavailable"
        }

# Legacy function for backward compatibility
async def estimate_location_from_wifi() -> Dict[str, Any]:
    """Legacy function - redirects to emergency location service"""
    return await get_emergency_location()

# Export main functions
__all__ = ['get_emergency_location', 'estimate_location_from_wifi']
