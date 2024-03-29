# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'sado_info.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('images', 'images'),
        ('fonts', 'fonts'),
        ('sounds', 'sounds'),
        ('sado.json', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='rickTcal',
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
    icon=['images/static/rickTcal.icns'],
)


app = BUNDLE(exe,
         name='rickTcal.app',
         icon='images/static/rickTcal.icns',
         bundle_identifier='rickTcal_DayLife',
         info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
        },
    )
