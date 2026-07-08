import subprocess
import os

def launchExecutable(app):
    result = subprocess.run(
    ["./launcher/launchingEngine.exe", app],
    capture_output=True,
    text=True
)
    if result.returncode == 0:
        return app

    return None





