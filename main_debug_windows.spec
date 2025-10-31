# -*- mode: python ; coding: utf-8 -*-
import os

# Poetry 가상환경 경로 가져오기
venv_path = os.popen('poetry env info --path').read().strip()
site_packages = os.path.join(venv_path, 'Lib', 'site-packages')

block_cipher = None

# 데이터 파일들 - 존재하는 것만 포함
datas = []
if os.path.exists('static'):
    datas.append(('static', 'static'))
if os.path.exists('config'):
    datas.append(('config', 'config'))
if os.path.exists('core'):
    datas.append(('core', 'core'))
if os.path.exists('common'):
    datas.append(('common', 'common'))

a = Analysis(
    ['main_debug.py'],
    pathex=[site_packages],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'fastapi',
        'fastapi.applications',
        'fastapi.routing',
        'fastapi.responses',
        'fastapi.staticfiles',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'fastapi.dependencies',
        'fastapi.security',
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.responses',
        'starlette.staticfiles',
        'starlette.middleware',
        'starlette.middleware.cors',
        'pydantic',
        'pydantic.main',
        'pydantic.fields',
        'pydantic.types',
        'pydantic.validators',
        'pydantic_core',
        'uvicorn',
        'uvicorn.main',
        'uvicorn.server',
        'uvicorn.config',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.http.httptools_impl',
        'uvicorn.protocols.websockets.wsproto_impl',
        'uvicorn.loops.auto',
        'uvicorn.loops.asyncio',
        'uvicorn.logging',
        'httpx',
        'jinja2',
        'multipart',
        'python_multipart',
        # 로컬 모듈들
        'core',
        'core.services',
        'config',
        'config.schemas',
        'config.data_manager',
        'common',
    ],
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
    name='client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
