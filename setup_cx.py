from cx_Freeze import setup, Executable
import sys

# Additional files
include_files = [('J:/Monitor/BH NPCs/Race Menu HELP V2/Data', 'Data')]

# Build options
build_options = {
    'packages': [],
    'excludes': [],
    'include_files': include_files
}

# Base for Windows (no console)
base = 'Win32GUI' if sys.platform == 'win32' else None

# Executable configuration
executable = Executable(
    script='020_Race_Menu_psc_creator.pyw',
    base=base,
    target_name="020_Race_Menu_psc_creator.exe"
)

setup(
    name='020_Race_Menu_psc_creator',
    version='1.0',
    description='',
    options={'build_exe': build_options},
    executables=[executable]
)
