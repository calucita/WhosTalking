# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['Run.py'],
             binaries=[],
             datas=[('./Success.html', '.'), ('./Failed.html', '.'), ('./boticon.ico', '.'),
             ('../../../AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/customtkinter','customtkinter'), 
             ('./img/main-moon.png', './img/.'), ('./img/main-lightbulb.png', './img/.'), 
             ('./img/main-stop.png', './img/.'), ('./img/main-play.png', './img/.'), 
             ('./img/main-dice.png', './img/.'), ('./img/main-lupa-plus.png', './img/.'), 
             ('./img/main-lupa-minus.png', './img/.'), ('./img/main-trash-can.png', './img/.'), 
             ('./img/main-ellipsis.png', './img/.'), ('./img/main-filter.png', './img/.'),
             ('./img/main-gear.png', './img/.'), ('./img/main-reply.png', './img/.'),
             ('./img/set-minus.png', './img/.'), ('./img/set-plus.png', './img/.'), ('./img/set-refresh.png', './img/.'),
             ('./img/set-text-height.png', './img/.'), ('./img/set-text-height-dark.png', './img/.')],
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
