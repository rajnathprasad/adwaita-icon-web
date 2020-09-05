import asyncio
import shutil
import os
from pathlib import Path
from watchgod import awatch, Change

base_dir = Path(__file__).parent
shell = asyncio.create_subprocess_shell


def copy_to_dir(src: Path, dest_dir: Path, src_base_dir: Path = None):
    if src_base_dir:
        dest = src.relative_to(src_base_dir)
    else:
        dest = src.name
    dest = dest_dir.joinpath(dest)
    os.makedirs(dest.parent, exist_ok=True)
    shutil.copy(src, dest)
    print(f'copy {src} -> {dest}')


async def copy_adwaita_icon():
    adwaita_icon_path = base_dir.parent.joinpath('dist', 'adwaita.svg')
    dest_dir = base_dir.joinpath('static')
    copy_to_dir(adwaita_icon_path, dest_dir)
    async for changes in awatch(adwaita_icon_path):
        for change, path in changes:
            path = Path(path)
            if change == Change.modified:
                copy_to_dir(path, dest_dir)


async def ui():
    src_base_dir = base_dir.parent.joinpath('src', 'web-components')
    dest_dir = base_dir.joinpath('static', 'ui')
    
    for path in src_base_dir.glob('**/*.js'):
        copy_to_dir(path, dest_dir, src_base_dir)

    async for changes in awatch(src_base_dir):
        for change, path in changes:
            path = Path(path)
            if path.suffix != '.js':
                continue
            if not change == Change.deleted:
                copy_to_dir(path, dest_dir, src_base_dir)


async def main():
    await asyncio.gather(
        copy_adwaita_icon(),
        ui(),
    )

asyncio.run(main())