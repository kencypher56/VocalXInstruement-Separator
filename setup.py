#!/usr/bin/env python3
"""
Enhanced setup script for VocalxInstrument Separator.
Handles both venv and conda environments. If conda is chosen but not installed,
the script can download and install Miniconda automatically (Linux/macOS).
"""

import os
import sys
import subprocess
import platform
import urllib.request
import tarfile
import tempfile
from pathlib import Path

VENV_DIR = Path.cwd() / ".venv"
REQUIREMENTS = Path(__file__).parent / "requirements.txt"

def check_conda():
    """Return path to conda executable if available, else None."""
    try:
        # Try 'conda' command
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'conda'
    except FileNotFoundError:
        pass

    # Also check common installation paths
    home = Path.home()
    candidates = [
        home / 'miniconda3' / 'bin' / 'conda',
        home / 'anaconda3' / 'bin' / 'conda',
        Path('/opt') / 'conda' / 'bin' / 'conda',
    ]
    for cand in candidates:
        if cand.exists():
            return str(cand)
    return None

def download_and_install_miniconda():
    """Download and install Miniconda (Linux/macOS). Returns path to conda binary."""
    system = platform.system()
    if system == "Linux":
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    elif system == "Darwin":
        # Check if Apple Silicon or Intel
        if platform.machine() == "arm64":
            url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
        else:
            url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    else:
        raise RuntimeError("Automatic Miniconda installation is only supported on Linux and macOS. Please install conda manually.")

    print("📥 Downloading Miniconda installer...")
    with tempfile.NamedTemporaryFile(suffix='.sh', delete=False) as tmp:
        installer_path = tmp.name
    urllib.request.urlretrieve(url, installer_path)
    os.chmod(installer_path, 0o755)

    # Install silently to ~/miniconda3
    install_dir = Path.home() / "miniconda3"
    print(f"📦 Installing Miniconda to {install_dir}...")
    subprocess.run([installer_path, '-b', '-p', str(install_dir)], check=True)

    # Clean up installer
    os.unlink(installer_path)

    conda_path = install_dir / "bin" / "conda"
    if not conda_path.exists():
        raise RuntimeError("Miniconda installation failed.")
    return str(conda_path)

def setup_conda(conda_path):
    """Create conda environment 'vocalx' and install dependencies."""
    print(f"🔧 Using conda at: {conda_path}")
    env_name = "vocalx"

    # Check if environment already exists
    result = subprocess.run([conda_path, 'env', 'list'], capture_output=True, text=True)
    if env_name in result.stdout:
        print(f"✅ Conda environment '{env_name}' already exists.")
    else:
        print(f"📦 Creating conda environment '{env_name}' with Python 3.9...")
        subprocess.run([conda_path, 'create', '-n', env_name, 'python=3.9', '-y'], check=True)

    # Get path to pip inside the environment
    env_prefix = subprocess.check_output([conda_path, 'env', 'list', '--json'], text=True)
    import json
    envs = json.loads(env_prefix)['envs']
    env_dir = next(e for e in envs if e.endswith(env_name))
    if platform.system() == "Windows":
        pip_path = Path(env_dir) / "Scripts" / "pip"
    else:
        pip_path = Path(env_dir) / "bin" / "pip"

    # Install dependencies
    print("📦 Installing Python packages (this may take a few minutes)...")
    subprocess.run([str(pip_path), 'install', '-r', str(REQUIREMENTS)], check=True)

    print(f"\n✅ Conda environment '{env_name}' is ready.")
    print("👉 Activate it with:")
    print(f"   conda activate {env_name}")
    print("   Then run the tool using python run.py or python cli.py")

def setup_venv():
    """Create a virtual environment and install dependencies."""
    print("🔧 Setting up with Python venv...")
    if not VENV_DIR.exists():
        print(f"📦 Creating virtual environment at {VENV_DIR}...")
        import venv
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("✅ Virtual environment already exists.")

    # Determine pip/python paths inside venv
    if sys.platform == "win32":
        pip_path = VENV_DIR / "Scripts" / "pip"
        python_path = VENV_DIR / "Scripts" / "python"
    else:
        pip_path = VENV_DIR / "bin" / "pip"
        python_path = VENV_DIR / "bin" / "python"

    # Upgrade pip
    print("📦 Upgrading pip...")
    subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Install requirements
    print("📦 Installing dependencies (this may take a few minutes)...")
    subprocess.run([str(pip_path), "install", "-r", str(REQUIREMENTS)], check=True)

    print("\n✅ Setup complete! Run the tool with:")
    print("   python run.py --help")
    print("   or")
    print("   python run.py (for interactive mode)")

def main():
    print("🔧 VocalxInstrument Separator Setup\n")

    # Ask user for preference
    print("Choose environment manager:")
    print("1) Python venv (local .venv folder)")
    print("2) Conda (creates 'vocalx' environment)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        # Check Python version
        if sys.version_info >= (3, 11):
            print("⚠️  Warning: Spleeter 2.4.0 requires Python < 3.11.")
            print("   Your current Python is", sys.version.split()[0])
            proceed = input("Proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Setup cancelled.")
                return
        setup_venv()
    elif choice == "2":
        conda_path = check_conda()
        if conda_path is None:
            print("❌ Conda is not installed.")
            auto_install = input("Would you like to download and install Miniconda automatically? (y/n): ").strip().lower()
            if auto_install == 'y':
                try:
                    conda_path = download_and_install_miniconda()
                except Exception as e:
                    print(f"❌ Automatic installation failed: {e}")
                    fallback = input("Fall back to venv? (y/n): ").strip().lower()
                    if fallback == 'y':
                        setup_venv()
                    return
            else:
                print("Please install conda manually and rerun setup.")
                return
        setup_conda(conda_path)
    else:
        print("❌ Invalid choice.")
        return

    # Check for ffmpeg (common requirement)
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ ffmpeg found.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ffmpeg not found. Please install ffmpeg manually for MP3 export and video conversion.")
        print("   - Linux: sudo apt install ffmpeg")
        print("   - macOS: brew install ffmpeg")
        print("   - Windows: download from https://ffmpeg.org/download.html")

if __name__ == "__main__":
    main()