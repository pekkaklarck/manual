"""Generate installation instructions.

They are copied from `INSTALL.md` at the project root.
"""

from pathlib import Path

import mkdocs_gen_files


root = Path(__file__).parent.parent.parent
source = root / 'INSTALL.md'
target = Path('install/index.md')

with mkdocs_gen_files.open(target, 'w') as file:
    file.write(source.read_text(encoding='UTF-8'))

mkdocs_gen_files.set_edit_path(target, '..' / source.relative_to(root))
