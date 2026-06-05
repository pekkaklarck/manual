
<a id="test-suite"></a>
# Creating test suites

Robot Framework [test cases](creating-test-cases.md#creating-test-cases) are created in test case files, which can
be organized into directories. These files and directories create a
hierarchical test suite structure. Same concepts apply also when
[creating tasks](creating-tasks.md#creating-tasks), but the terminology differs.

<a id="suite-file"></a>
## Suite files

Robot Framework test cases [are created](creating-test-cases.md#creating-test-cases) using test case sections in
suite files, also known as test case files. Such a file automatically creates
a test suite from
all the test cases it contains. There is no upper limit for how many
test cases there can be, but it is recommended to have less than ten,
unless the [data-driven approach](creating-test-cases.md#data-driven-approach) is used, where one test case consists of
only one high-level keyword.

The following settings in the Setting section can be used to customize the suite:

`Name`
: Used for setting a custom [suite name](#suite-name). The default name is created based
   on the file or directory name.
`Documentation`
   Used for specifying a [suite documentation](#suite-documentation).
`Metadata`
   Used for setting [free suite metadata](#free-suite-metadata) as name-value pairs.
`Suite Setup`, `Suite Teardown`
   Specify [suite setup and teardown](#suite-setup-and-teardown).

!!! note
    Setting names are case-insensitive, but the format used above is recommended.

<a id="suite-directory"></a>
## Suite directories

Test case files can be organized into directories, and these
directories create higher-level test suites. A test suite created from
a directory cannot have any test cases directly, but it contains
other test suites with test cases, instead. These directories can then be
placed into other directories creating an even higher-level suite. There
are no limits for the structure, so test cases can be organized
as needed.

When a test directory is executed, the files and directories it
contains are processed recursively as follows:

- Files and directories with names starting with a dot (*.*) or an
  underscore (*_*) are ignored.
- Directories with the name *CVS* are ignored (case-sensitive).
- Files in [supported file formats](test-data-syntax.md#supported-file-formats) are processed.
- Other files are ignored.

If a file or directory that is processed does not contain any test
cases, it is silently ignored (a message is written to the [syslog](../executing-tests/result-files.md#syslog))
and the processing continues.

<a id="initialization-file"></a>

<a id="suite-initialization-file"></a>
### Suite initialization files

A test suite created from a directory can have similar settings as a suite
created from a test case file. Because a directory alone cannot have that
kind of information, it must be placed into a special suite initialization
file. An initialization file name must always be of the format
*[__init](../extending/parser-interface.md#parse-init-method).ext*, where the extension must be one of the [supported
file formats](test-data-syntax.md#supported-file-formats) (typically *[__init](../extending/parser-interface.md#parse-init-method).robot*).
The name format is borrowed from Python, where files named in this manner
denote that a directory is a module.

Starting from Robot Framework 6.1, it is also possible to define a suite
initialization file for automatically created suite when starting the test
execution by giving multiple [paths](#paths).

Initialization files have the same structure and syntax as test case files,
except that they cannot have test case sections and not all settings are
supported. Variables and keywords created or imported in initialization files
*are not* available in the lower level suites. If you need to share
variables or keywords, you can put them into [resource files](resource-files.md#resource-files) that can be
imported both by initialization and test case files.

The main usage for initialization files is specifying suite related
settings similarly as in [suite files](#suite-files), but setting some [test case
related settings](../executing-tests/configuring-execution.md#by-suite-names) is also possible. How to use different settings in the
initialization files is explained below.

`Name`, `Documentation`, `Metadata`, `Suite Setup`, `Suite Teardown`
: These suite specific settings work the same way in suite initialization files
   as in suite files.
`Test Tags`
   Specified tags are unconditionally set to all tests in all suite files
   this directory contains, recursively. New in Robot Framework 6.1. The
   deprecated `Force Tags` needs to be used with older versions.
`Test Setup`, `Test Teardown`, `Test Timeout`
   Set the default value for test setup/teardown or test timeout to all test
   cases this directory contains. Can be overridden on lower level.
   Notice that keywords used as setups and teardowns must be available in
   test case files where tests using them are. Defining keywords in the
   initialization file itself is not enough.
`Task Setup`, `Task Teardown`, `Task Tags`, `Task Timeout`
   Aliases for `Test Setup`, `Test Teardown`, `Test Tags`
   and `Test Timeout`, respectively, that can be used when
   [creating tasks](creating-tasks.md#creating-tasks), not tests.
`Test Template`, `Default Tags`
   Not supported in initialization files.

```robotframework
*** Settings ***
Documentation    Example suite
Suite Setup      Do Something    ${MESSAGE}
Test Tags        example
Library          SomeLibrary

*** Variables ***
${MESSAGE}       Hello, world!

*** Keywords ***
Do Something
    [Arguments]    ${args}
    Some Keyword    ${arg}
    Another Keyword
```

!!! note
    When you run a suite file or directory, possible suite initialization
    files in higher level directories are not taken into account. If that
    is not desired, run the appropriate higher level suite directory and use
    the [--suite](../executing-tests/configuring-execution.md#setting-suite-name) option to select which child suite inside it is executed.

## Suite name

The test suite name is constructed from the file or directory name by default.
The name is created so that the extension is ignored, possible underscores are
replaced with spaces, and names fully in lower case are title cased. For
example, *some_tests.robot* becomes *Some Tests* and
*My_test_directory* becomes *My test directory*.

The file or directory name can contain a prefix to control the [execution
order](../executing-tests/test-execution.md#execution-order) of the suites. The prefix is separated from the base name by two
underscores and, when constructing the actual test suite name, both
the prefix and underscores are removed. For example files
*01__some_tests.robot* and *02__more_tests.robot* create test
suites *Some Tests* and *More Tests*, respectively, and
the former is executed before the latter.

Starting from Robot Framework 6.1, it is also possible to give a custom name
to a suite by using the `Name` setting in the Setting section:

```robotframework
*** Settings ***
Name            Custom suite name
```
The name of the top-level suite [can be overridden](../executing-tests/configuring-execution.md#setting-suite-documentation) from the command line with
the `--name` option.

## Suite documentation

The documentation for a test suite is set using the `Documentation`
setting in the Settings section. It can be used both in [suite files](#suite-files)
and in [suite initialization files](#suite-initialization-files). Suite documentation has exactly
the same characteristics regarding to where it is shown and how it can
be created as [test case documentation](creating-test-cases.md#test-case-documentation). For details about the syntax
see the [Documentation formatting](../appendices/documentation-formatting.md#documentation-formatting) appendix.

```robotframework
*** Settings ***
Documentation    An example suite documentation with *some* _formatting_.
...              Long documentation can be split into multiple lines.
```
The documentation of the top-level suite [can be overridden](test-data-syntax.md#dividing-data-to-several-rows) from
the command line with the `--doc` option.

## Free suite metadata

In addition to documentation, suites can also have free metadata. This metadata
is defined as name-value pairs in the Settings section using the `Metadata`
setting. It is shown in reports and logs similarly as documentation.

Name of the metadata is the first argument given to the `Metadata` setting
and the remaining arguments specify its value. The value is handled similarly as
documentation, which means that it supports [HTML formatting](../appendices/documentation-formatting.md#html-formatting) and [variables](variables.md#variables), and
that longer values can be [split into multiple rows](../executing-tests/configuring-execution.md#setting-free-suite-metadata).

```robotframework
*** Settings ***
Metadata        Version            2.0
Metadata        Robot Framework    http://robotframework.org
Metadata        Platform           ${PLATFORM}
Metadata        Longer Value
...             Longer metadata values can be split into multiple
...             rows. Also *simple* _formatting_ is supported.
```
The free metadata of the top-level suite [can be set](creating-test-cases.md#test-setup-and-teardown) from
the command line with the `--metadata` option.

<a id="suite-setup"></a>

<a id="suite-teardown"></a>
## Suite setup and teardown

Not only [test cases](creating-test-cases.md#test-case) but also test suites can have a setup and
a teardown. A suite setup is executed before running any of the suite's
test cases or child test suites, and a suite teardown is executed after
them. All test suites can have a setup and a teardown; with suites created
from a directory they must be specified in a [suite initialization file](#suite-initialization-file).

Similarly as with test cases, a suite setup and teardown are keywords
that may take arguments. They are defined in the Setting section with
`Suite Setup` and `Suite Teardown` settings,
respectively. Keyword names and possible arguments are located in
the columns after the setting name.

If a suite setup fails, all test cases in it and its child test suites
are immediately assigned a fail status and they are not actually
executed. This makes suite setups ideal for checking preconditions
that must be met before running test cases is possible.

A suite teardown is normally used for cleaning up after all the test
cases have been executed. It is executed even if the setup of the same
suite fails. If the suite teardown fails, all test cases in the
suite are marked failed, regardless of their original execution status.
Note that all the keywords in suite teardowns are executed even if one
of them fails.

The name of the keyword to be executed as a setup or a teardown can be
a variable. This facilitates having different setups or teardowns
in different environments by giving the keyword name as a variable
from the command line.
