

<a id="Resourcefiles"></a>
# Resource files

Resource files are typically created using the plain text format, but also
[reStructuredText format](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data) and [JSON format](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.to_json) are supported.

### Taking resource files into use

Resource files are imported using the `Resource` setting in the
Settings section so that the path to the resource file is given as an argument
to the setting. The recommended extension for resource files is *.resource*.
For backwards compatibility reasons also *.robot*, *.txt* and
*.tsv* work, but using *.resource* may be mandated in the future.

If the resource file path is absolute, it is used directly. Otherwise,
the resource file is first searched relatively to the directory
where the importing file is located. If the file is not found there,
it is then searched from the directories in Python's [module search path](../executing-tests/configuring-execution.md#module-search-path).
Searching resource files from the module search path makes it possible to
bundle them into Python packages as [package data](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.from_json) and importing
them like *package/example.resource*.

The resource file path can contain variables, and it is recommended to use
them to make paths system-independent (for example,
*${RESOURCES}/login.resource* or just *${RESOURCE_PATH}*).
Additionally, forward slashes (`/`) in the path
are automatically changed to backslashes (`\\`) on Windows.

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
    The *.resource* extension is new in Robot Framework 3.1.

### Resource file structure

The higher-level structure of resource files is the same as that of
suite files otherwise, but they cannot contain tests or tasks.
Additionally, the Setting section in resource files can contain only imports
(`Library`, `Resource`, `Variables`),
`Documentation` and `Keyword Tags`.
The Variable section and Keyword section are used exactly the same way
as in suite files.

If several resource files have a user keyword with the same name, they
must be used so that the [keyword name is prefixed with the resource
file name](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data) without the extension (for example, *myresources.Some
Keyword* and *common.Some Keyword*). Moreover, if several resource
files contain the same variable, the one that is imported first is
taken into use.

### Documenting resource files

Keywords created in a resource file can be [documented](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.to_json) using
`[Documentation]` setting. The resource file itself can have
`Documentation` in the Setting section similarly as [suites](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.from_json).

[Libdoc](../supporting-tools/libdoc.md#libdoc) and various editors use these documentations, and they
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
### Resource files using reStructured text format

The [reStructuredText format](test-data-syntax.md#restructuredtext-format) that can be used with [suite files](creating-test-suites.md#suite-files)  works
also with resource files. Such resource files can use either *.rst*
or *.rest* extension and they are otherwise imported exactly as
normal resource files:

```robotframework
*** Settings ***
Resource         example.rst
```
When parsing resource files using the reStructuredText format, Robot Framework
ignores all data outside code blocks containing Robot Framework data exactly
the same way as when parsing [reStructuredText suite files](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data).
For example, the following resource file imports *OperatingSystem* library,
defines `${MESSAGE}` variable and creates *My Keyword* keyword:

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

The [Markdown format](test-data-syntax.md#markdown-format) that can be used with [suite files](creating-test-suites.md#suite-files) works also with
resource files. Such resource files can use either *.md* or
*.markdown* extension and they are otherwise imported exactly as normal
resource files:

```robotframework
*** Settings ***
Resource         example.md
```
When parsing resource files using the Markdown format, Robot Framework
ignores all data outside fenced code blocks with the `robotframework` or `robot`
language tag exactly the same way as when parsing [Markdown suite files](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data).
For example, the following resource file imports *OperatingSystem* library,
defines `${MESSAGE}` variable and creates *My Keyword* keyword:

```markdown
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
```
```

### Resource files using JSON format

Resource files can be created using JSON_ the [same way as suite files](#same-way-as-suite-files).
Such JSON resource files must use either the standard *.json* extension
or the custom *.rsrc* extension. They are otherwise imported exactly as
normal resource files:

```robotframework
*** Settings ***
Resource         example.rsrc
```
Resource files can be converted to JSON using [ResourceFile.to_json](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data) and
recreated using [ResourceFile.from_json](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.to_json):

```python
from robot.running import ResourceFile

# Create resource file based on data on the file system.
resource = ResourceFile.from_file_system('example.resource')

# Save JSON data to a file.
resource.to_json('example.rsrc')

# Recreate resource from JSON data.
resource = ResourceFile.from_json('example.rsrc')
```
