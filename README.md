# Robot Framework Manual

:construction: Under development!

Robot Framework Manual is planned to replace the current
[Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
and also current [API docs](https://robot-framework.readthedocs.org/)
will be migrated into it.

Robot Framework Manual pages in this repository are written in Markdown, and the website is built with
[ProperDocs](https://properdocs.org/), using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
for visual design.

See the generated pages at https://pekkaklarck.github.io/manual/.

## Contribution guidelines

Contributions are welcome, from typo fixes to corrections and additions.

To contribute, fork the repository, make your changes, and open a
[pull request](https://github.com/robotframework/robotframework/blob/master/CONTRIBUTING.rst#pull-requests).

## Setting up development environment

### Prerequisites

- **Python 3.13** or higher

### Installing dependencies

It’s recommended to create a Python virtual environment (with `venv`, `uv`, or another tool of your choice) and run the
commands below within it. Make sure your working directory is the repository root (the top-level directory containing
`requirements.txt`) before installation.

#### Install dependencies

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

#### Verify the ProPerdocs installation

    properdocs --version

### Previewing the Manual

#### Start the development server

    properdocs serve

Example output:

    INFO    -  Building documentation...
    INFO    -  Cleaning site directory
    API doc generation takes some time. It can be disabled by setting the 'DO_NOT_GENERATE_API_DOCS' environment variable to a non-empty value.
    INFO    -  Documentation built in 11.84 seconds
    INFO    -  [22:03:18] Watching paths for changes: 'doc/manual/docs', 'properdocs.yml', 'INSTALL.md', 'src/robot',
            'doc/manual/overrides'
    INFO    -  [22:03:18] Serving on http://127.0.0.1:8000/manual/

Open http://127.0.0.1:8000/manual/ in your browser. The changes will be reflected as you modify the contents of the pages.

#### Optional: speed up builds

To speed up builds, disable API document generation:

Linux (Bash)

    DO_NOT_GENERATE_API_DOCS=True properdocs serve

Windows (Command Prompt)

    set "DO_NOT_GENERATE_API_DOCS=True" && properdocs serve

### Stopping the preview server

To stop the development server, use the key combination:

    Ctrl + C

## Getting help

If you need guidance or help with getting started with contributing (or have a suggestion or would like to discuss
the manual), reach out in the [#manual](https://robotframework.slack.com/archives/C063Y9GEMUP) channel on Slack.
