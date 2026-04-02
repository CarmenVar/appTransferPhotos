import os
import subprocess
import sys

def build():
    print("Starting build process using PyInstaller...")
    
    # We must include the icon/assets and ui files
    main_script = "main.py"
    build_args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=CloudPhotoTransfer",
        "--windowed",
        "--onedir",
        "--add-data=assets;assets",
        "--add-data=ui/style.qss;ui",
        "--hidden-import=PyQt6.sip",
        "--hidden-import=google.cloud.storage",
        "-y",
        main_script
    ]
    
    # Check if credentials exist before adding to build
    creds_path = "credentials.json"
    if os.path.exists(creds_path):
        print(f"Including {creds_path} in the build.")
        build_args.insert(10, f"--add-data={creds_path};.")
    else:
        print(f"WARNING: {creds_path} script not found. Build will proceed without embedded credentials.")
    
    try:
        result = subprocess.run(build_args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Build failed with error:\n{result.stderr}")
            sys.exit(1)
        print("Build completed successfully. Check the /dist directory.")
    except Exception as e:
        print(f"Build system error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
