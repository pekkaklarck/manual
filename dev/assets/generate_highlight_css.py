#!/usr/bin/env python

"""Generate syntax highlighting CSS files for light and dark modes.

Usage: {name} <mode> <style>

Parameters:
  mode:   Either 'dark' or 'light'.
  style:  Any style name recognized by Pygments. Run 'pygmentize -L styles'
          to see available styles.
"""

import sys
from pathlib import Path

from pygments.formatters import HtmlFormatter


try:
    mode, style_name = sys.argv[1:]
    if mode not in ["dark", "light"]:
        raise ValueError
except ValueError:
    sys.exit(__doc__.format(name=sys.argv[0]))

scheme = "default" if mode == "light" else "slate"
path = Path(__file__).parent / f"highlight-{mode}.css"
styles = HtmlFormatter(style=style_name).get_style_defs(".highlight")

with open(path, "w") as file:
    file.write(f"""\
/* Syntax highlighting for the {mode} mode using Pygments style '{style_name}'.

   Generated using 'generate_highlight_css' script. DO NOT EDIT MANUALLY!
*/
[data-md-color-scheme="{scheme}"] {{
""")
    for line in styles.splitlines():
        if line.startswith(".highlight"):
            file.write(f"  {line}\n")
    file.write("}\n")

print(path)
