"""
Run the Emergency Response Dashboard
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Run the Streamlit dashboard"""
    dashboard_path = Path(__file__).parent / "streamlit_dashboard.py"
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running dashboard: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
        return 0
    
    return 0

if __name__ == "__main__":
    exit(main())