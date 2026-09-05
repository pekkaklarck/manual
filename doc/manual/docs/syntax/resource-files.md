

<a id="Resourcefiles"></a>
# Resource files

Resource files are typically created using the plain text format, but also
[reStructuredText](#resource-files-using-restructuredtext-format), [Markdown](#resource-files-using-markdown-format) and [JSON](#resource-files-using-json-format) resource files are supported.

### Taking resource files into use

Resource files are imported using the *Resource*{.setting} setting in the
Settings section so that the path to the resource file is given as an argument
to the setting. The recommended extension for resource files is `.resource`{.file}.
For backwards compatibility reasons also `.robot`{.file}, `.txt`{.file} and
`.tsv`{.file} work, but using `.resource`{.file} may be mandated in the future.

If the resource file path is absolute, it is used directly. Otherwise,
the resource file is first searched relatively to the directory
where the importing file is located. If the file is not found there,
it is then searched from the directories in Python's [module search path](../execution/configuration.md#module-search-path).
Searching resource files from the module search path makes it possible to
bundle them into Python packages as [package data](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data) and importing
them like `package/example.resource`{.file}.

The resource file path can contain variables, and it is recommended to use
them to make paths system-independent (for example,
`${RESOURCES}/login.resource`{.file} or just `${RESOURCE_PATH}`{.file}).
Additionally, forward slashes (`/`) in the path
are automatically changed to backslashes (`\`{.codesc}) on Windows.

```robotframework
*** Settings ***
Resource    example.resource
Resource    ../resources/login.resource
Resource    package/example.resource
Resource    ${RESOURCES}/common.resource
```

The user keywords and variables defined in a resource file are
available in the file that takes that resource file into
use. Similarly available are also all keywords and variables from the
libraries, resource files and variable files imported by the said
resource file.

!!! note
    The `.resource`{.file} extension is new in Robot Framework 3.1.

### Resource file structure

The higher-level structure of resource files is the same as that of
suite files otherwise, but they cannot contain tests or tasks.
Additionally, the Setting section in resource files can contain only imports
(*Library*{.setting}, *Resource*{.setting}, *Variables*{.setting}),
*Documentation*{.setting} and *Keyword Tags*{.setting}.
The Variable section and Keyword section are used exactly the same way
as in suite files.

If several resource files have a user keyword with the same name, they
must be used so that the [keyword name is prefixed with the resource
file name](advanced.md#handling-keywords-with-same-names) without the extension (for example, *myresources.Some Keyword*{.name} and *common.Some Keyword*{.name}). Moreover, if several resource
files contain the same variable, the one that is imported first is
taken into use.

### Documenting resource files

Keywords created in a resource file can be [documented](user-keywords.md#user-keyword-name-and-documentation) using
*[Documentation]*{.setting} setting. The resource file itself can have
*Documentation*{.setting} in the Setting section similarly as [suites](suites.md#suite-name).

[Libdoc](../extend/libdoc.md#libdoc) and various editors use these documentations, and they
are naturally available for anyone opening resource files.  The
first logical line of the documentation of a keyword, until the first
empty line, is logged when the keyword is run, but otherwise resource
file documentation is ignored during the test execution.

### Example resource file

```robotframework
*** Settings ***
Documentation     An example resource file
Library           SeleniumLibrary
Resource          ${RESOURCES}/common.resource

*** Variables ***
${HOST}           localhost:7272
${LOGIN URL}      http://${HOST}/
${WELCOME URL}    http://${HOST}/welcome.html
${BROWSER}        Firefox

*** Keywords ***
Open Login Page
    [Documentation]    Opens browser to login page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Title Should Be    Login Page

Input Name
    [Arguments]    ${name}
    Input Text    username_field    ${name}

Input Password
    [Arguments]    ${password}
    Input Text    password_field    ${password}
```

### Resource files using reStructuredText format

The [reStructuredText data format](data.md#restructuredtext-data-format) that can be used with [suite files](suites.md#suite-files)  works
also with resource files. Such resource files can use either `.rst`{.file}
or `.rest`{.file} extension and they are otherwise imported exactly as
normal resource files:

```robotframework
*** Settings ***
Resource         example.rst
```

When parsing resource files using the reStructuredText format, Robot Framework
ignores all data outside code blocks containing Robot Framework data exactly
the same way as when parsing [reStructuredText suite files](data.md#restructuredtext-data-format).
For example, the following resource file imports *OperatingSystem*{.name} library,
defines `${MESSAGE}` variable and creates *My Keyword*{.name} keyword:

```rst
Resource file using reStructuredText
------------------------------------

This text is outside code blocks and thus ignored.

.. code:: robotframework

   *** Settings ***
   Library          OperatingSystem

   *** Variables ***
   ${MESSAGE}       Hello, world!

Also this text is outside code blocks and ignored. Code blocks not
containing Robot Framework data are ignored as well.

.. code:: robotframework

   # Both space and pipe separated formats are supported.

   | *** Keywords ***  |                        |         |
   | My Keyword        | [Arguments]            | ${path} |
   |                   | Directory Should Exist | ${path} |
```

### Resource files using Markdown format

The [Markdown data format](data.md#markdown-data-format) that can be used with [suite files](suites.md#suite-files) works also with
resource files. Such resource files can use either `.md`{.file} or
`.markdown`{.file} extension and they are otherwise imported exactly as normal
resource files:

```robotframework
*** Settings ***
Resource         example.md
```

When parsing resource files using the Markdown format, Robot Framework
ignores all data outside fenced code blocks with the `robotframework` or `robot`
language tag exactly the same way as when parsing [Markdown suite files](data.md#markdown-data-format).
For example, the following resource file imports *OperatingSystem*{.name} library,
defines `${MESSAGE}` variable and creates *My Keyword*{.name} keyword:

````markdown
# Resource file using Markdown

This text is outside code blocks and thus ignored.

```robotframework
*** Settings ***
Library          OperatingSystem

*** Variables ***
${MESSAGE}       Hello, world!
```

Also this text is outside code blocks and ignored. Code blocks not
containing Robot Framework data are ignored as well.

```robotframework
# Both space and pipe separated formats are supported.

| *** Keywords ***  |                        |         |
| My Keyword        | [Arguments]            | ${path} |
|                   | Directory Should Exist | ${path} |
```
````

### Resource files using JSON format

Resource files can be created using [JSON](#json) the [same way as suite files](data.md#json-data-format).
Such JSON resource files must use either the standard `.json`{.file} extension
or the custom `.rsrc`{.file} extension. They are otherwise imported exactly as
normal resource files:

```robotframework
*** Settings ***
Resource         example.rsrc
```

Resource files can be converted to JSON using [ResourceFile.to_json](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.to_json) and
recreated using [ResourceFile.from_json](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.from_json):

```python
from robot.running import ResourceFile

# Create resource file based on data on the file system.
resource = ResourceFile.from_file_system('example.resource')

# Save JSON data to a file.
resource.to_json('example.rsrc')

# Recreate resource from JSON data.
resource = ResourceFile.from_json('example.rsrc')
```
