import importlib.metadata as pkg_resources
import requests
import subprocess
import sys

def get_latest_version(pkg):
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data["info"]["version"]
    except:
        return
        
def check_outdated(logs=True):
    if logs: print("Checking for outdated packages...")
    outdated = []
    ok = []
    for dist in pkg_resources.distributions():
        name = dist.metadata["Name"]
        current_version = dist.version
        latest_version = get_latest_version(name)
        if latest_version and latest_version != current_version:
            outdated.append(name)
            if logs: print(f"{name} is outdated: {current_version} (should be {latest_version})")
        else:
            ok.append(name)
            if logs: print(f"{name} is up to date.")
    return outdated, ok
    
def update_all(packages=None, logs=False, checklogs=False):
    if packages is None:
        packages, _ = check_outdated(logs=checklogs)
    if isinstance(packages, str):
        packages = [packages]
    
    for pkg in packages:
        if logs: print(f"Updating package {pkg}...")             
        try:
            if logs:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg])
            else:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
                )    
        except Exception as e:
            if logs: print(f"Error: {e}")        
            