#!/bin/bash

# Create a temporary build directory in the Linux filesystem
BUILD_DIR="/tmp/pi-trader-build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy project files to build directory
cp -r . "$BUILD_DIR/"

# Change to build directory
cd "$BUILD_DIR"

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyInstaller first
pip install pyinstaller==6.12.0

# Install other requirements
pip install -r requirements.txt

# Run the build script with detailed output
python build.py

# Show the contents of the dist directory
echo "Contents of dist directory:"
ls -la dist/

# Create dist directory in original location if it doesn't exist
mkdir -p "/mnt/c/Users/Disph/OneDrive/Desktop/CursorSandbox/pi-trader/dist"

# Copy the built executable back to the Windows filesystem with verbose output
if [ -f "dist/pi-trader" ]; then
    cp -v dist/pi-trader "/mnt/c/Users/Disph/OneDrive/Desktop/CursorSandbox/pi-trader/dist/"
    echo "Build complete. The executable can be found in the dist directory."
else
    echo "Build failed. No executable was created."
    exit 1
fi

# Deactivate virtual environment
deactivate

# Cleanup
cd ..
rm -rf "$BUILD_DIR" 