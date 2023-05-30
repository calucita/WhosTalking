# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['Run.py'],
             pathex=['F:\\Calu\\GitHub\\WhosTalking\\img'],
             binaries=[],
             datas=[('./Success.html', '.'), ('./Failed.html', '.'), ('./boticon.ico', '.'),('../../../AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/customtkinter','customtkinter')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
	  icon='boticon.ico')
