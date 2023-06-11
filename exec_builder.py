import PyInstaller.__main__
import subprocess
import distutils.spawn

# Check if PyInstaller is installed
try:
    subprocess.check_output(['pyinstaller', '--version'])
    pyinstaller_installed = True
    print("pyinstaller is already Installed")
except subprocess.CalledProcessError:
    pyinstaller_installed = False

# Install PyInstaller if it is not installed
if not pyinstaller_installed:
    try:
        print("pyinstaller is not installed. Installing pyinstaller...")
        subprocess.check_output(['pip', 'install', 'pyinstaller'])
        pyinstaller_installed = True
    except subprocess.CalledProcessError as e:
        print(f"Error installing PyInstaller: {e}")
        exit(1)


ffmpeg_path = distutils.spawn.find_executable('ffmpeg')

try:
    PyInstaller.__main__.run([
        'StartPage.py',
        '--onefile',
        '--console',
        f'--add-binary={ffmpeg_path};ffmpeg',
    ])
except Exception as e:
    print(f"Error running PyInstaller: {e}")
    exit(1)