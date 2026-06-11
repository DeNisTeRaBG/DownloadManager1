import os
import sys
import winreg
import ctypes

def is_admin():
    """Checks if the script is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def register_magnet_handler():
    """Registers this Python application to handle magnet:// links system-wide."""
    
    # 1. Force Administrator Privileges
    if not is_admin():
        print("Requesting Administrator privileges...")
        # This triggers the Windows UAC prompt
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
        return

    # 2. Get absolute paths
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    script_path = os.path.abspath("main.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Could not find {script_path}. Run this from the same folder as main.py.")
        input("Press Enter to exit...")
        return

    # 3. The exact command Windows needs to run
    command = f'"{python_exe}" "{script_path}" "%1"'

    try:
        # We use HKEY_CLASSES_ROOT to force it system-wide so Windows 11 Settings sees it
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"magnet")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:Magnet Protocol")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        
        cmd_key = winreg.CreateKey(key, r"shell\open\command")
        winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command)
        
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
        
        print("\nSUCCESS! The magnet protocol has been forcefully registered system-wide.")
        print(f"Command configured as: {command}\n")
        
    except Exception as e:
        print(f"\nFailed to set registry keys.\nError: {e}\n")
        
    input("Press Enter to close this window...")

if __name__ == "__main__":
    register_magnet_handler()