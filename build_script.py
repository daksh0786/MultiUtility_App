import os
import subprocess
import sys
import shutil
from pathlib import Path
import textwrap


def clean_previous_builds():
    """Clean up previous build artifacts"""
    for path in ['dist', 'build']:
        if os.path.exists(path):
            shutil.rmtree(path)
    for file in Path('.').glob('*.spec'):
        file.unlink()


def build_app():
    try:
        # Clean previous builds
        clean_previous_builds()

        # Get paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, 'Model')
        resources_dir = os.path.join(base_dir, 'resources')
        components_dir = os.path.join(base_dir, 'Components')
        venv_path = os.path.dirname(sys.executable)

        # Platform-specific separator
        separator = ';' if sys.platform.startswith('win') else ':'

        # PyInstaller command
        cmd = [
            sys.executable,
            '-m', 'PyInstaller',
            '--name=AppSuite',
            '--onefile',
            f'--add-data={model_dir}{separator}Model',  # Bundle Model folder
            f'--add-data={resources_dir}{separator}resources',  # Bundle resources folder
            f'--add-data={components_dir}{separator}Components',  # Bundle Components folder
            '--hidden-import=keras',
            '--hidden-import=keras.models',
            '--hidden-import=keras.layers',
            '--hidden-import=keras.preprocessing',
            '--hidden-import=keras.callbacks',
            '--hidden-import=keras.optimizers',
            '--hidden-import=keras.applications',
            '--clean',
            'app.py'  # Adjust if your main script is different
        ]

        # Run PyInstaller
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == '__main__':
    build_app()
