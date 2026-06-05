
<a id="general-parsing-rules"></a>
# Test data syntax

This section covers Robot Framework's overall test data syntax. The following
sections will explain how to actually create test cases, test suites and so on.
Although this section mostly uses term *test*, the same rules apply also
when [creating tasks](creating-tasks.md#creating-tasks).

## Files and directories

The hierarchical structure for arranging test cases is built as follows:

- Test cases are created in [suite files](creating-test-suites.md#suite-files).
- A test case file automatically creates a [test suite](creating-test-suites.md#test-suite) containing
  the test cases in that file.
- A directory containing test case files forms a higher-level test
  suite. Such a [suite directory](creating-test-suites.md#suite-directory) has suites created from test
  case files as its child test suites.
- A test suite directory can also contain other test suite directories,
  and this hierarchical structure can be as deeply nested as needed.
- Test suite directories can have a special [initialization file](creating-test-suites.md#initialization-file)
  configuring the created test suite.

In addition to this, there are:

- [Test libraries](using-test-libraries.md#test-libraries) containing the lowest-level keywords.
- [Resource files](resource-files.md#resource-files) with [variables](variables.md#variables) and higher-level [user keywords](creating-user-keywords.md#user-keyword).
- [Variable files](variable-files.md#variable-files) to provide more flexible ways to create variables
  than resource files.

Test case files, test suite initialization files and resource files are
all created using Robot Framework test data syntax. Test libraries and
variable files are created using "real" programming languages, most
often Python.

<a id="test-data-tables"></a>

<a id="section-headers"></a>
## Test data sections

Robot Framework data is defined in different sections, often also
called tables, listed below:

| Section | Used for |
| --- | --- |
| Settings | 1) Importing [test libraries](using-test-libraries.md#test-libraries), [resource files](resource-files.md#resource-files) and [variable files](variable-files.md#variable-files). 2) Defining metadata for [test suites](creating-test-suites.md#test-suite) and [test cases](creating-test-cases.md#test-case). |
| Variables | Defining [variables](variables.md#variables) that can be used elsewhere in the test data. |
| Test Cases | [Creating test cases](creating-test-cases.md#creating-test-cases) from available keywords. |
| Tasks | [Creating tasks](creating-tasks.md#creating-tasks) using available keywords. Single file can only contain either tests or tasks. |
| Keywords | [Creating user keywords](creating-user-keywords.md#creating-user-keywords) from existing lower-level keywords |
| Comments | Additional comments or data. Ignored by Robot Framework. |

Different sections are recognized by their header row. The recommended
header format is `*** Settings ***`, but the header is case-insensitive,
surrounding spaces are optional, and the number of asterisk characters can
vary as long as there is at least one asterisk in the beginning. For example,
also `*settings` would be recognized as a section header.

Robot Framework supports also singular headers like `*** Setting ***,` but that
support was deprecated in Robot Framework 6.0. There is a visible deprecation
warning starting from Robot Framework 7.0 and singular headers will eventually
not be supported at all.

The header row can contain also other data than the actual section header.
The extra data must be separated from the section header using the data
format dependent separator, typically two or more spaces. These extra headers
are ignored at parsing time, but they can be used for documenting
purposes. This is especially useful when creating test cases using the
[data-driven style](creating-test-cases.md#data-driven-style).

Possible data before the first section is ignored.

!!! note
    Section headers can be [localized](#localized). See the [Translations](../appendices/translations.md#translations) appendix for
    supported translations.

## Supported file formats

The most common approach to create Robot Framework data is using the
[space separated format](#space-separated-format) where pieces of the data, such as keywords
and their arguments, are separated from each others with two or more spaces.
An alternative is using the [pipe separated format](#pipe-separated-format) where the separator is
the pipe character surrounded with spaces (`\ |\ `).

Suite files typically use the *.robot* extension, but what files are
parsed [can be configured](https://issues.robotframework.org). [Resource files](resource-files.md#resource-files) can use the *.robot*
extension as well, but using the dedicated *.resource* extension is
recommended and may be mandated in the future. Files containing non-ASCII
characters must be saved using the UTF-8 encoding.

Robot Framework supports also [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) files so that normal
Robot Framework data is [embedded into code blocks](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json). Only files with
the *.robot.rst* extension are parsed by default. If you would
rather use just *.rst* or *.rest* extension, that needs to be
configured separately.

Robot Framework supports also [Markdown](https://en.wikipedia.org/wiki/Markdown) files so that normal Robot Framework
data is [embedded into code blocks](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_dict). Only files with the *.robot.md*
extension are parsed by default. If you would rather use just *.md* or
*.markdown* extension, that needs to be configured separately.

Robot Framework data can also be created in the [JSON format](control-structures.md#for) that is targeted
more for tool developers than normal Robot Framework users. Only JSON files
with the custom *.rbt* extension are parsed by default.

Earlier Robot Framework versions supported data also in HTML and TSV formats.
The TSV format still works if the data is compatible with the [space separated
format](#space-separated-format), but the support for the HTML format has been removed altogether.
If you encounter such data files, you need to convert them to the plain text
format to be able to use them with Robot Framework 3.2 or newer. The easiest
way to do that is using the [Tidy](../supporting-tools/tidy.md#tidy) tool, but you must use the version included
with Robot Framework 3.1 because newer versions do not understand the HTML
format at all.

<a id="space-separated-plain-text-format"></a>
<a id="plain-text-format"></a>
### Space separated format

When Robot Framework parses data, it first splits the data to lines and then
lines to tokens such as keywords and arguments. When using the space
separated format, the separator between tokens is two or more spaces or
alternatively one or more tab characters. In addition to the normal ASCII
space, any Unicode character considered to be a space (e.g. no-break space)
works as a separator. The number of spaces used as separator can vary, as
long as there are at least two, making it possible to align the data nicely
in settings and elsewhere when it makes the data easier to understand.

```robotframework
*** Settings ***
Documentation     Example using the space separated format.
Library           OperatingSystem

*** Variables ***
${MESSAGE}        Hello, world!

*** Test Cases ***
My Test
    [Documentation]    Example test.
    Log    ${MESSAGE}
    My Keyword    ${CURDIR}

Another Test
    Should Be Equal    ${MESSAGE}    Hello, world!

*** Keywords ***
My Keyword
    [Arguments]    ${path}
    Directory Should Exist    ${path}
```
Because tabs and consecutive spaces are considered separators, they must
be escaped if they are needed in keyword arguments or elsewhere
in the actual data. It is possible to use special escape syntax like
`\t` for tab and `\xA0` for no-break space as well as [built-in variables](variables.md#built-in-variables)
`${SPACE}` and `${EMPTY}`. See the [Escaping](#escaping) section for details.

!!! tip
    Although using two spaces as a separator is enough, it is recommended
    to use four spaces to make the separator easier to recognize.

!!! note
    Prior to Robot Framework 3.2, non-ASCII spaces used in the data
    were converted to ASCII spaces during parsing. Nowadays all data
    is preserved as-is.

### Pipe separated format

The biggest problem of the space delimited format is that visually
separating keywords from arguments can be tricky. This is a problem
especially if keywords take a lot of arguments and/or arguments
contain spaces. In such cases the pipe delimited variant can
work better because it makes the separator more visible.

One file can contain both space separated and pipe separated lines.
Pipe separated lines are recognized by the mandatory leading pipe character,
but the pipe at the end of the line is optional. There must always be at
least one space or tab on both sides of the pipe except at the beginning and
at the end of the line. There is no need to align the pipes, but that often
makes the data easier to read.

```robotframework
| *** Settings ***   |
| Documentation      | Example using the pipe separated format.
| Library            | OperatingSystem

| *** Variables ***  |
| ${MESSAGE}         | Hello, world!

| *** Test Cases *** |                 |               |
| My Test            | [Documentation] | Example test. |
|                    | Log             | ${MESSAGE}    |
|                    | My Keyword      | ${CURDIR}     |
| Another Test       | Should Be Equal | ${MESSAGE}    | Hello, world!

| *** Keywords ***   |                        |         |
| My Keyword         | [Arguments]            | ${path} |
|                    | Directory Should Exist | ${path} |
```
When using the pipe separated format, consecutive spaces or tabs inside
arguments do not need to be escaped. Similarly empty columns do not need
to be escaped except [if they are at the end](https://issues.robotframework.org). Possible pipes surrounded by
spaces in the actual test data must be escaped with a backslash, though:

```robotframework
| *** Test Cases *** |                 |                 |                      |
| Escaping Pipe      | ${file count} = | Execute Command | ls -1 *.txt \| wc -l |
|                    | Should Be Equal | ${file count}   | 42                   |
```

!!! note
    Preserving consecutive spaces and tabs in arguments is new
    in Robot Framework 3.2. Prior to it non-ASCII spaces used in
    the data were also converted to ASCII spaces.

### reStructuredText format

[reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (reST) is an easy-to-read plain text markup syntax that
is commonly used for documentation of Python projects, including Python itself
as well as this User Guide. reST documents are most often compiled to HTML,
but also other output formats are supported. Using reST with Robot Framework
allows you to mix richly formatted documents and test data in a concise text
format that is easy to work with using simple text editors, diff tools, and
source control systems.

!!! note
    Using [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) files with Robot Framework requires the
    Python [docutils](https://pypi.python.org/pypi/docutils) module to be installed.

When using Robot Framework with reStructuredText files, normal Robot Framework
data is embedded to so called code blocks. In standard reST code blocks are
marked using the `code` directive, but Robot Framework supports also
`code-block` or `sourcecode` directives used by the [Sphinx](http://sphinx-doc.org/) tool.

```rst
reStructuredText example
------------------------

This text is outside code blocks and thus ignored.

.. code:: robotframework

   *** Settings ***
   Documentation    Example using the reStructuredText format.
   Library          OperatingSystem

   *** Variables ***
   ${MESSAGE}       Hello, world!

   *** Test Cases ***
   My Test
       [Documentation]    Example test.
       Log    ${MESSAGE}
       My Keyword    ${CURDIR}

   Another Test
       Should Be Equal    ${MESSAGE}    Hello, world!

Also this text is outside code blocks and ignored. Code blocks not
containing Robot Framework data are ignored as well.

.. code:: robotframework

   # Both space and pipe separated formats are supported.

   | *** Keywords ***  |                        |         |
   | My Keyword        | [Arguments]            | ${path} |
   |                   | Directory Should Exist | ${path} |

.. code:: python

   # This code block is ignored.
   def example():
       print('Hello, world!')
```
Robot Framework supports reStructuredText files using *.robot.rst*,
*.rst* and *.rest* extensions. To avoid parsing unrelated
reStructuredText files, only files with the *.robot.rst* extension
are parsed by default when executing a directory. Parsing files with
other extensions [can be enabled](https://issues.robotframework.org) by using either `--parseinclude`
or `--extension` option.

When Robot Framework parses reStructuredText files, errors below level
`SEVERE` are ignored to avoid noise about possible non-standard directives
and other such markup. This may hide also real errors, but they can be seen
when processing files using reStructuredText tooling normally.

!!! note
    Parsing *.robot.rst* files automatically is new in
    Robot Framework 6.1.

### Markdown format

[Markdown](https://en.wikipedia.org/wiki/Markdown) is a lightweight plain text markup syntax that is widely used for
documentation, README files, and technical content across the software
development industry. Because of its natural fit for narrative documentation,
using Markdown with Robot Framework allows you to create test data in a format
that is easy to read, write and preview using standard editors and tools.

When Robot Framework parses Markdown files, it searches for code blocks
starting with fences of at least three backticks `\`\`\`` or tildes
`~~~` and the `robotframework` or `robot` language tag.
All content outside such blocks is ignored. The parser follows the [CommonMark](https://spec.commonmark.org)
specification for fenced code blocks, which means that the opening and closing
fences must match and the closing fence must be at least as long as the
opening one. If a code block is not closed properly, the rest of the file
will be considered as part of the code block itself.

```markdown
# Markdown example

This text is outside code blocks and thus ignored.

```robotframework
*** Settings ***
Documentation    Example using the Markdown format.
Library          OperatingSystem

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
My Test
    [Documentation]    Example test.
    Log    ${MESSAGE}
    My Keyword    ${CURDIR}

*** Keywords ***
My Keyword
    [Arguments]    ${path}
    Directory Should Exist    ${path}
```

More free text here. There could be additional code blocks with more
Robot Framework data as well.

```python
# This code block is ignored.
def example():
    print('Hello, world!')
```
```
Robot Framework supports Markdown files using *.robot.md*,
*.md* and *.markdown* extensions. To avoid parsing unrelated
Markdown files, only files with the *.robot.md* extension
are parsed by default when executing a directory. Parsing files with
the *.md* or *.markdown* extension [can be enabled](../executing-tests/configuring-execution.md#selecting-files-to-parse) by using
either `--parseinclude` or `--extension` option.

!!! note
    Using Markdown_ files with Robot Framework does not require any
    external Python module to be installed.

!!! note
    Markdown support is new in Robot Framework 7.5.
```

### JSON format

Robot Framework supports data also in the JSON_ format. This format is designed
more for tool developers than for regular Robot Framework users and it is not
meant to be edited manually. Its most important use cases are:

- Transferring data between processes and machines. A suite can be converted
  to JSON in one machine and recreated somewhere else.
- Saving a suite, possibly a nested suite, constructed from normal Robot Framework
  data into a single JSON file that is faster to parse.
- Alternative data format for external tools generating tests or tasks.

!!! note
    The JSON data support is new in Robot Framework 6.1 and it can be
    enhanced in future Robot Framework versions. If you have an enhancement
    idea or believe you have encountered a bug, please submit an issue__
    or start a discussion thread on the `#devel` channel on our Slack_.

#### Converting suite to JSON

A suite structure can be serialized into JSON by using the [TestSuite.to_json](https://robot-framework.readthedocs.io/en/master/autodoc/robot.result.html#robot.result.model.TestSuite.to_json)
method. When used without arguments, it returns JSON data as a string, but
it also accepts a path or an open file where to write JSON data along with
configuration options related to JSON formatting:

```python
from robot.running import TestSuite

# Create suite based on data on the file system.
suite = TestSuite.from_file_system('/path/to/data')

# Get JSON data as a string.
data = suite.to_json()

# Save JSON data to a file with custom indentation.
suite.to_json('data.rbt', indent=2)
```
If you would rather work with Python data and then convert that to JSON
or some other format yourself, you can use [TestSuite.to_dict](https://issues.robotframework.org) instead.

#### Creating suite from JSON

A suite can be constructed from JSON data using the [TestSuite.from_json](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json)
method. It works both with JSON strings and paths to JSON files:

```python
from robot.running import TestSuite

# Create suite from JSON data in a file.
suite = TestSuite.from_json('data.rbt')

# Create suite from a JSON string.
suite = TestSuite.from_json('{"name": "Suite", "tests": [{"name": "Test"}]}')

# Execute suite. Notice that log and report needs to be created separately.
suite.run(output='example.xml')
```
If you have data as a Python dictionary, you can use [TestSuite.from_dict](https://issues.robotframework.org)
instead. Regardless of how a suite is recreated, it exists only in memory and
original data files on the file system are not recreated.

As the above example demonstrates, the created suite can be executed using
the [TestSuite.run](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json) method. It may, however, be easier to execute a JSON file
directly as explained in the following section.

#### Executing JSON files

When executing tests or tasks using the `robot` command, JSON files with
the custom *.rbt* extension are parsed automatically. This includes
running individual JSON files like `robot tests.rbt` and running directories
containing *.rbt* files. If you would rather use the standard
*.json* extension, you need to [configure which files are parsed](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_dict).

#### Adjusting suite source

Suite source in the data got from `TestSuite.to_json` and `TestSuite.to_dict`
is in absolute format. If a suite is recreated later on a different machine,
the source may thus not match the directory structure on that machine. To
avoid that, it is possible to use the [TestSuite.adjust_source](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_json) method to
make the suite source relative before getting the data and add a correct root
directory after the suite is recreated:

```python
from robot.running import TestSuite

# Create a suite, adjust source and convert to JSON.
suite = TestSuite.from_file_system('/path/to/data')
suite.adjust_source(relative_to='/path/to')
suite.to_json('data.rbt')

# Recreate suite elsewhere and adjust source accordingly.
suite = TestSuite.from_json('data.rbt')
suite.adjust_source(root='/new/path/to')
```

#### JSON structure

Imports, variables and keywords created in suite files are included in the
generated JSON along with tests and tasks. The exact JSON structure is documented
in the *running.json* [schema file](https://github.com/robotframework/robotframework/tree/master/doc/schema#readme).

## Rules for parsing the data

<a id="comment"></a>
### Ignored data

When Robot Framework parses the test data files, it ignores:

- All data before the first [test data section](https://issues.robotframework.org).
- Data in the [Comments](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json) section.
- All empty rows.
- All empty cells at the end of rows when using the [pipe separated format](#pipe-separated-format).
- All single backslashes (`\\`) when not used for [escaping](#escaping).
- All characters following the hash character (`#`), when it is the first
  character of a cell. This means that hash marks can be used to enter
  comments in the test data.

When Robot Framework ignores some data, this data is not available in
any resulting reports and, additionally, most tools used with Robot
Framework also ignore them. To add information that is visible in
Robot Framework outputs, place it to the documentation or other metadata of
test cases or suites, or log it with the [BuiltIn](using-test-libraries.md#builtin) keywords *Log* or
*Comment*.

### Escaping

The escape character in Robot Framework test data is the backslash
(`\\`) and additionally [built-in variables](variables.md#built-in-variables) `${EMPTY}` and `${SPACE}`
can often be used for escaping. Different escaping mechanisms are
discussed in the sections below.

#### Escaping special characters

The backslash character can be used to escape special characters
so that their literal values are used.

   | Character | Meaning | Examples |
   | --- | --- | --- |
   | `\$` | Dollar sign, never starts a [scalar variable](variables.md#scalar-variable). | `\${notvar}` |
   | `\@` | At sign, never starts a [list variable](variables.md#list-variable). | `\@{notvar}` |
   | `\&` | Ampersand, never starts a [dictionary variable](variables.md#dictionary-variable). | `\&{notvar}` |
   | `\%` | Percent sign, never starts an [environment variable](variables.md#environment-variable). | `\%{notvar}` |
   | `\#` | Hash sign, never starts a [comment](#comment). | `\# not comment` |
   | `\=` | Equal sign, never part of [named argument syntax](creating-test-cases.md#named-argument-syntax). | `not\=named` |
   | `\|` | Pipe character, not a separator in the [pipe separated format](#pipe-separated-format). | `ls -1 *.txt \| wc -l` |
   | `\\` | Backslash character, never escapes anything. | `c:\\temp, \\${var}` |

<a id="escape-sequence"></a>
<a id="escape-sequences"></a>
#### Forming escape sequences

The backslash character also allows creating special escape sequences that are
recognized as characters that would otherwise be hard or impossible to create
in the test data.

   | Sequence | Meaning | Examples |
   | --- | --- | --- |
   | `\n` | Newline character. | `first line\n2nd line` |
   | `\r` | Carriage return character | `text\rmore text` |
   | `\t` | Tab character. | `text\tmore text` |
   | `\xhh` | Character with hex value `hh`. | `null byte: \x00, ä: \xE4` |
   | `\uhhhh` | Character with hex value `hhhh`. | `snowman: \u2603` |
   | `\Uhhhhhhhh` | Character with hex value `hhhhhhhh`. | `love hotel: \U0001f3e9` |

!!! note
    All strings created in the test data, including characters like
    `\x02`, are Unicode and must be explicitly converted to
    byte strings if needed. This can be done, for example, using
    *Convert To Bytes* or *Encode String To Bytes* keywords
    in [BuiltIn](using-test-libraries.md#builtin) and [String](using-test-libraries.md#string) libraries, respectively, or with
    something like `value.encode('UTF-8')` in Python code.

!!! note
    If invalid hexadecimal values are used with `\x`, `\u`
    or `\U` escapes, the end result is the original value without
    the backslash character. For example, `\xAX` (not hex) and
    `\U00110000` (too large value) result with `xAX`
    and `U00110000`, respectively. This behavior may change in
    the future, though.

!!! note
    [Built-in variable](variables.md#built-in-variable) `${\n}` can be used if operating system
    dependent line terminator is needed (`\r\n` on Windows and
    `\n` elsewhere).

#### Handling empty values

When using the [space separated format](#space-separated-format), the number of spaces used as
a separator can vary and thus empty values cannot be recognized unless they
are escaped. Empty cells can be escaped either with the backslash character
or with [built-in variable](variables.md#built-in-variable) `${EMPTY}`. The latter is typically recommended
as it is easier to understand.

```robotframework
*** Test Cases ***
Using backslash
    Do Something    first arg    \
    Do Something    \            second arg

Using ${EMPTY}
    Do Something    first arg    ${EMPTY}
    Do Something    ${EMPTY}     second arg
```
When using the [pipe separated format](#pipe-separated-format), empty values need to be escaped
only when they are at the end of the row:

```robotframework
| *** Test Cases *** |              |           |            |
| Using backslash    | Do Something | first arg | \          |
|                    | Do Something |           | second arg |
|                    |              |           |            |
| Using ${EMPTY}     | Do Something | first arg | ${EMPTY}   |
|                    | Do Something |           | second arg |
```
#### Handling spaces

Spaces, especially consecutive spaces, as part of arguments for keywords or
needed otherwise are problematic for two reasons:

- Two or more consecutive spaces is considered a separator when using the
  [space separated format](#space-separated-format).
- Leading and trailing spaces are ignored when using the
  [pipe separated format](#pipe-separated-format).

In these cases spaces need to be escaped. Similarly as when escaping empty
values, it is possible to do that either by using the backslash character or
by using the [built-in variable](variables.md#built-in-variable) `${SPACE}`.

   | Escaping with backslash | Escaping with `${SPACE}` | Notes |
   | --- | --- | --- |
   | `\\ leading space`          `${SPA | }leading space` |  |
   | `trailing space \\`         `trail | g space${SPACE}`            Backsl | h must be after the space. |
   | `\\ \\`                     `${SPA | }`                          Backsl | h needed on both sides. |
   | `consecutive \\ \\ spaces`  `conse | tive${SPACE * 3}spaces[Using | xtended variable syntax](variables.md#variable). |

As the above examples show, using the `${SPACE}` variable often makes the
test data easier to understand. It is especially handy in combination with
the [extended variable syntax](variables.md#extended-variable-syntax) when more than one space is needed.

### Dividing data to several rows

If there is more data than readily fits a row, it is possible to split it
and start continuing rows with ellipsis (`...`). Ellipses can be indented
to match the indentation of the starting row and they must always be followed
by the normal test data separator.

In most places split lines have exact same semantics as lines that are not
split. Exceptions to this rule are [suite](https://issues.robotframework.org), [test](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json) and [keyword](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_dict) documentation
as well [suite metadata](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_json). With them split values are automatically
[joined together with the newline character](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_dict) to ease creating multiline
values.

The `...` syntax allows also splitting variables in the [Variable section](variables.md#variable-section).
When long scalar variables (e.g. `${STRING}`) are split to multiple rows,
the final value is got by concatenating the rows together. The separator is
a space by default, but that can be changed by starting the value with
`SEPARATOR=<sep>`.

Splitting lines is illustrated in the following two examples containing
exactly same data without and with splitting.

```robotframework
*** Settings ***
Documentation      Here we have documentation for this suite.\nDocumentation is often quite long.\n\nIt can also contain multiple paragraphs.
Test Tags          test tag 1    test tag 2    test tag 3    test tag 4    test tag 5

*** Variables ***
${STRING}          This is a long string. It has multiple sentences. It does not have newlines.
${MULTILINE}       This is a long multiline string.\nThis is the second line.\nThis is the third and the last line.
@{LIST}            this     list     is    quite    long     and    items in it can also be long
&{DICT}            first=This value is pretty long.    second=This value is even longer. It has two sentences.

*** Test Cases ***
Example
    [Tags]    you    probably    do    not    have    this    many    tags    in    real    life
    Do X    first argument    second argument    third argument    fourth argument    fifth argument    sixth argument
    ${var} =    Get X    first argument passed to this keyword is pretty long    second argument passed to this keyword is long too
```
```robotframework
*** Settings ***
Documentation      Here we have documentation for this suite.
...                Documentation is often quite long.
...
...                It can also contain multiple paragraphs.
Test Tags          test tag 1    test tag 2    test tag 3
...                test tag 4    test tag 5

*** Variables ***
${STRING}          This is a long string.
...                It has multiple sentences.
...                It does not have newlines.
${MULTILINE}       SEPARATOR=\n
...                This is a long multiline string.
...                This is the second line.
...                This is the third and the last line.
@{LIST}            this     list     is      quite    long     and
...                items in it can also be long
&{DICT}            first=This value is pretty long.
...                second=This value is even longer. It has two sentences.

*** Test Cases ***
Example
    [Tags]    you    probably    do    not    have    this    many
    ...       tags    in    real    life
    Do X    first argument    second argument    third argument
    ...    fourth argument    fifth argument    sixth argument
    ${var} =    Get X
    ...    first argument passed to this keyword is pretty long
    ...    second argument passed to this keyword is long too
```

<a id="localized"></a>
## Localization

Robot Framework localization efforts were started in Robot Framework 6.0
that allowed translation of [section headers](../appendices/translations.md#section-headers), [settings](../appendices/translations.md#settings),
[Given/When/Then prefixes](https://issues.robotframework.org) used in Behavior Driven Development (BDD), and
[true and false strings](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json) used in automatic Boolean argument conversion.
The plan is to extend localization support in the future, for example,
to log and report and possibly also to control structures.

This section explains how to [activate languages](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_dict), what [built-in languages](#built-in-languages)
are supported, how to create [custom language files](#custom-language-files) and how new translations
can be [contributed](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_json).

### Enabling languages

#### Using command line option

The main mechanism to activate languages is specifying them from the command line
using the `--language` option. When enabling [built-in languages](#built-in-languages),
it is possible to use either the language name like `Finnish` or the language
code like `fi`. Both names and codes are case and space insensitive and also
the hyphen (`-`) is ignored. To enable multiple languages, the
`--language` option needs to be used multiple times:

```
robot --language Finnish testit.robot
robot --language pt --language ptbr testes.robot
```

The same `--language` option is also used when activating
[custom language files](#custom-language-files). With them the value can be either a path to the file or,
if the file is in the [module search path](../executing-tests/configuring-execution.md#module-search-path), the module name:

```
robot --language Custom.py tests.robot
robot --language MyLang tests.robot
```

For backwards compatibility reasons, and to support partial translations,
English is always activated automatically. Future versions may allow disabling
it.

#### Pre-file configuration

It is also possible to enable languages directly in data files by having
a line `Language: <value>` (case-insensitive) before any of the section
headers. The value after the colon is interpreted the same way as with
the `--language` option:

```
Language: Finnish
```

    *** Asetukset ***
    Dokumentaatio        Example using Finnish.

If there is a need to enable multiple languages, the `Language:` line
can be repeated. These configuration lines cannot be in comments so something like
`# Language: Finnish` has no effect.

Due to technical limitations, the per-file language configuration affects also
parsing subsequent files as well as the whole execution. This
behavior is likely to change in the future and *should not* be relied upon.
If you use per-file configuration, use it with all files or enable languages
globally with the `--language` option.

### Built-in languages

The following languages are supported out-of-the-box. Click the language name
to see the actual translations:

<!-- START GENERATED CONTENT -->


- [Arabic (ar)](../appendices/translations.md#arabic-ar)
- [Bulgarian (bg)](../appendices/translations.md#bulgarian-bg)
- [Bosnian (bs)](../appendices/translations.md#bosnian-bs)
- [Czech (cs)](../appendices/translations.md#czech-cs)
- [German (de)](../appendices/translations.md#german-de)
- [Spanish (es)](../appendices/translations.md#spanish-es)
- [Finnish (fi)](../appendices/translations.md#finnish-fi)
- [French (fr)](../appendices/translations.md#french-fr)
- [Hindi (hi)](../appendices/translations.md#hindi-hi)
- [Italian (it)](../appendices/translations.md#italian-it)
- [Japanese (ja)](../appendices/translations.md#japanese-ja)
- [Korean (ko)](../appendices/translations.md#korean-ko)
- [Dutch (nl)](../appendices/translations.md#dutch-nl)
- [Polish (pl)](../appendices/translations.md#polish-pl)
- [Portuguese (pt)](../appendices/translations.md#portuguese-pt)
- [Brazilian Portuguese (pt-BR)](../appendices/translations.md#brazilian-portuguese-pt-br)
- [Romanian (ro)](../appendices/translations.md#romanian-ro)
- [Russian (ru)](../appendices/translations.md#russian-ru)
- [Swedish (sv)](../appendices/translations.md#swedish-sv)
- [Thai (th)](../appendices/translations.md#thai-th)
- [Turkish (tr)](../appendices/translations.md#turkish-tr)
- [Ukrainian (uk)](../appendices/translations.md#ukrainian-uk)
- [Vietnamese (vi)](../appendices/translations.md#vietnamese-vi)
- [Chinese Simplified (zh-CN)](../appendices/translations.md#chinese-simplified-zh-cn)
- [Chinese Traditional (zh-TW)](../appendices/translations.md#chinese-traditional-zh-tw)

<!-- END GENERATED CONTENT -->
All these translations have been provided by the awesome Robot Framework
community. If a language you are interested in is not included, you can
consider [contributing](https://issues.robotframework.org) it!

### Custom language files

If a language you would need is not available as a built-in language, or you
want to create a totally custom language for some specific need, you can easily
create a custom language file. Language files are Python files that contain
one or more language definitions that are all loaded when the language file
is taken into use. Language definitions are created by extending the
`robot.api.Language` base class and overriding class attributes as needed:

```python
from robot.api import Language

class Example(Language):
    test_cases_header = 'Validations'
    tags_setting = 'Labels'
    given_prefixes = ['Assuming']
    true_strings = ['OK', '\N{THUMBS UP SIGN}']
```
Assuming the above code would be in file *example.py*, a path to that
file or just the module name `example` could be used when the language file
is [activated](https://issues.robotframework.org).

The above example adds only some of the possible translations. That is fine
because English is automatically enabled anyway. Most values must be specified
as strings, but BDD prefixes and true/false strings allow more than one value
and must be given as lists. For more examples, see Robot Framework's internal
[languages](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_json) module that contains the `Language` class as well as all built-in
language definitions.

### Contributing translations

If you want to add translation for a new language or enhance existing, head
to [Crowdin](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.to_dict) that we use for collaboration. For more details, see the
separate [Localization](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_json) project, and for questions and free discussion join
the `#localization` channel on our [Slack](http://slack.robotframework.org).

## Style

Robot Framework syntax creates a simple programming language, and similarly as with
other languages, it is important to think about the coding style. Robot Framework
syntax is pretty flexible on purpose, but there are some generally recommended
conventions:

- Four space indentation.
- Four space separation between keywords and arguments, settings and their values, etc...
  In some cases it makes sense to use more than four spaces.
  For example when aligning values in the Settings or Variables section or
  in [data-driven style](creating-test-cases.md#data-driven-style).
- Global [variables](variables.md#variables) using capital letters like `${EXAMPLE}` and local variables
  using lower-case letters like `${example}`.
- Consistency within a single file and preferably within the whole project.

One case where there currently is no strong convention is keyword capitalization.
Robot Framework itself typically uses title case like *Example Keyword* in
documentation and elsewhere, and this style is often used in Robot Framework data
as well. It does not work too well with longer, sentence-like keywords such as
*Log into system as an admin*, though.

Teams and organizations using Robot Framework should have their own coding standards.
The community developed [Robot Framework Style Guide](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.from_dict) is an excellent
starting point that can be amended as needed. It is also possible to enforce these
conventions by using the [Robocop](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.TestSuite.run) linter and the [Robotidy](https://robot-framework.readthedocs.io/en/master/autodoc/robot.model.html#robot.model.testsuite.TestSuite.adjust_source) code formatter.

