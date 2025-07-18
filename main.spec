# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('mikubg.png', '.'), ('bg.jpg', '.')],  # Include your image files
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy unused modules to speed up build
        'tkinter', 'matplotlib', 'scipy', 'pandas', 'numpy.distutils',
        'numpy.f2py', 'numpy.testing', 'test', 'unittest', 'pydoc',
        'doctest', 'pdb', 'profile', 'cProfile', 'timeit', 'trace', 
        'py_compile', 'compileall', 'pickletools', 'turtle', 'webbrowser'
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HatsuneMikuAssistant_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mikubg.png'  # Set icon
)
