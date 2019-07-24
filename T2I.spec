# -*- mode: python -*-

block_cipher = None


a = Analysis(['T2I.py'],
             pathex=['C:\\Users\\rahul\\Documents\\Python\\Text2Image'],
             binaries=[],
             datas=[('tasakai_lig.ttf', 'font')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='T2I',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='a2.ico')
