import PyInstaller.__main__
import os
import sys

def build_application():
    # Get the absolute path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    src_dir = os.path.join(script_dir, 'src')
    main_path = os.path.join(src_dir, 'main.py')
    config_dir = os.path.join(script_dir, 'config')
    
    # PyInstaller arguments
    args = [
        main_path,
        '--onefile',
        '--name=pi-trader',
        f'--add-data={config_dir}{os.pathsep}config',
        '--clean',
        '--log-level=INFO',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=alpaca',
        '--hidden-import=openai',
        '--hidden-import=schedule',
        '--hidden-import=pytz',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_application() 