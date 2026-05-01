import os
import sys
import subprocess
import venv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, ".venv")
REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")

def in_venv():
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def get_venv_paths():
    if os.name == "nt":
        python_path = os.path.join(VENV_DIR, "Scripts", "python.exe")
        pip_path = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        python_path = os.path.join(VENV_DIR, "bin", "python")
        pip_path = os.path.join(VENV_DIR, "bin", "pip")
    return python_path, pip_path


def create_venv():
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)


def install_requirements(pip_path):
    if os.path.exists(REQUIREMENTS):
        print("Installing dependencies...")
        subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS])
    else:
        print("No requirements.txt found, skipping install.")


def relaunch_in_venv(python_path):
    print("Re-launching inside virtual environment...\n")

    script = os.path.abspath(__file__)

    cmd = [python_path, script, *sys.argv[1:]]
    print("DEBUG subprocess:", cmd)

    # Run and exit current process
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def main():
    
    if not in_venv():
        python_path, pip_path = get_venv_paths()

        if not os.path.exists(python_path):
            create_venv()

        install_requirements(pip_path)
        relaunch_in_venv(python_path)

    # ===== YOUR ACTUAL PROGRAM STARTS HERE =====
    print("Running inside virtual environment!")
    print(f"Python executable: {sys.executable}")




if __name__ == "__main__":
    main()