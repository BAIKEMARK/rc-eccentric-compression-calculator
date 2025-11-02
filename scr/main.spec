# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['compression_desgin.py', 'getConstant.py', 'rc_check.py', 'symmetrical_rc_compression.py', 'asymmetrical_rc_eccentric_compression.py'],
    binaries=[],
    datas=[('a1b1.csv','.'),('concrete.csv','.'),('epsilon_b.csv','.'),('fai.csv','.'),('steelbar.csv','.'),('icon.png','.'),('icon.ico','.'),('compression_design.ui','.')],
    hiddenimports=['compression_desgin.py', 'getConstant.py', 'rc_check.py', 'symmetrical_rc_compression.py', 'asymmetrical_rc_eccentric_compression.py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./icon.ico'],
)
