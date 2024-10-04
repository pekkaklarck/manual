"""Generate standard library documentation."""

import os
import sys
import tempfile
from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent.parent

# Make sure `robot` is imported from right place and contains latest changes.
sys.path.insert(0, str(root / 'src'))
for name in sorted(sys.modules):
    if name == 'robot' or name.startswith('robot.'):
        sys.modules.pop(name)

from robot.libdoc import libdoc


html_temp = tempfile.mkstemp(suffix='.html')[1]
json_temp = tempfile.mkstemp(suffix='.json')[1]


def generate(name):
    html_target = Path(f'libraries/{name}.html')
    json_target = Path(f'libraries/{name}.json')
    libdoc(name, html_temp, quiet=True)
    libdoc(name, json_temp, specdocformat='RAW', quiet=True)
    with mkdocs_gen_files.open(html_target, 'w') as file:
        file.write(Path(html_temp).read_text(encoding='UTF-8'))
    with mkdocs_gen_files.open(json_target, 'w') as file:
        file.write(Path(json_temp).read_text(encoding='UTF-8'))


for name in ['BuiltIn', 'Collections', 'DateTime', 'Dialogs', 'OperatingSystem',
             'Process', 'Screenshot', 'String', 'Telnet', 'XML']:
    generate(name)


os.unlink(html_temp)
os.unlink(json_temp)
