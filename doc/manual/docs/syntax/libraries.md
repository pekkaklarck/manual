
<a id="test-libraries"></a>
# Using test libraries

Test libraries contain those lowest-level keywords, often called
*library keywords*, which actually interact with the system under
test. All test cases always use keywords from some library, often
through higher-level [user keywords](creating-user-keywords.md#user-keyword). This section explains how to
take test libraries into use and how to use the keywords they
provide. [Creating test libraries](../extending/creating-test-libraries.md#creating-test-libraries) is described in a separate
section.

## Importing libraries

Test libraries are typically imported using the `Library` setting,
but it is also possible to use the *Import Library* keyword.

### Using `Library` setting

Libraries are normally imported in the Settings section using the
`Library` setting with the library name or path as its value.
Unlike most of the other data, the library name or path
is both case- and space-sensitive. If a library is in a package,
the full name including the package name must be used.

In those cases where the library needs arguments, they are listed in
the columns after the library name. It is possible to use default
values, variable number of arguments, and named arguments in test
library imports similarly as with [arguments to keywords](creating-test-cases.md#using-arguments).  Both the
library name and arguments can be set using variables.

```robotframework
*** Settings ***
Library    OperatingSystem
Library    path/to/MyLibrary.py
Library    my.package.TestLibrary
Library    LibraryAcceptingArguments    arg1    arg2
Library    ${LIBRARY}
```
It is possible to import test libraries in [suite files](creating-test-suites.md#suite-files),
[resource files](resource-files.md#resource-files) and [suite initialization files](creating-test-suites.md#suite-initialization-files). In all these
cases, all the keywords in the imported library are available in that
file. With resource files, those keywords are also available in other
files using them.

### Using `Import Library` keyword

Another possibility to take a test library into use is using the
keyword *Import Library* from the [BuiltIn](#builtin) library. This keyword
takes the library name or path and possible arguments similarly as the
`Library` setting. Keywords from the imported library are
available in the test suite where the *Import Library* keyword was
used. This approach is useful in cases where the library is not
available when the test execution starts and only some other keywords
make it available.

```robotframework
*** Test Cases ***
Example
    Do Something
    Import Library    MyLibrary    arg1    arg2
    KW From MyLibrary
```
## Specifying library to import

Libraries to import can be specified either by using the library name
or the path to the library. These approaches work the same way regardless
if the library is imported using the `Library` setting or the
*Import Library* keyword.

### Using library name

The most common way to specify a test library to import is using its name.
In these cases Robot Framework tries to find the class or module
implementing the library from the [module search path](../executing-tests/configuring-execution.md#module-search-path). Libraries that
are installed somehow ought to be in the module search path automatically,
but with other libraries the search path may need to be configured separately.

```robotframework
*** Settings ***
Library    OperatingSystem
Library    CustomLibrary    possible    arguments
Library    librarymodule.LibraryClass
```
The biggest benefit of this approach is that when the module search
path has been configured, often using a custom [start-up script](../executing-tests/basic-usage.md#start-up-script),
normal users do not need to think where libraries actually are
installed. The drawback is that getting your own, possible
very simple, libraries into the search path may require some
additional configuration.

### Using physical path to library

Another mechanism for specifying the library to import is using a
path to it in the file system. This path is considered relative to the
directory where current test data file is situated similarly as paths
to [resource and variable files](variables.md#variable). The main benefit of this approach
is that there is no need to configure the module search path.

If the library is a file, the path to it must contain extension,
i.e. *.py*. If a library is implemented
as a directory, the path to it must have a trailing forward slash (`/`)
if the path is relative. With absolute paths the trailing slash is optional.
Following examples demonstrate these different usages.

```robotframework
*** Settings ***
Library    PythonLibrary.py
Library    relative/path/PythonDirLib/    possible    arguments
Library    ${RESOURCES}/Example.py
```
## Setting custom name to library

The library name is shown in test logs before keyword names, and if
multiple keywords have the same name, they must be used so that the
[keyword name is prefixed with the library name](advanced-features.md#handling-keywords-with-same-names). The library name
is got normally from the module or class name implementing it, but
there are some situations where changing it is desirable:

- There is a need to import the same library several times with
  different arguments. This is not possible otherwise.

- The library name is inconveniently long.

- You want to use variables to import different libraries in
  different environments, but refer to them with the same name.

- The library name is misleading or otherwise poor. In this case,
  changing the actual name is, of course, a better solution.

The basic syntax for specifying the new name is having the text
`AS` (case-sensitive) after the library name and then
having the new name after that. The specified name is shown in
logs and must be used in the test data when using keywords' full name
(*LibraryName.Keyword Name*).

```robotframework
*** Settings ***
Library    packagename.TestLib    AS    TestLib
Library    ${LIBRARY}    AS    MyName
```
Possible arguments to the library are placed between the
original library name and the `AS` marker. The following example
illustrates how the same library can be imported several times with
different arguments:

```robotframework
*** Settings ***
Library    SomeLibrary    localhost        1234    AS    LocalLib
Library    SomeLibrary    server.domain    8080    AS    RemoteLib

*** Test Cases ***
Example
    LocalLib.Some Keyword     some arg       second arg
    RemoteLib.Some Keyword    another arg    whatever
    LocalLib.Another Keyword
```
Setting a custom name to a test library works both when importing a
library in the Setting section and when using the *Import Library* keyword.

!!! note
    Prior to Robot Framework 6.0 the marker to use when giving a custom name
    to a library was `WITH NAME` instead of `AS`. The old syntax continues
    to work, but it is considered deprecated and will eventually be removed.

## Standard libraries

Some test libraries are distributed with Robot Framework and these
libraries are called *standard libraries*. The [BuiltIn](#builtin) library is special,
because it is taken into use automatically and thus its keywords are always
available. Other standard libraries need to be imported in the same way
as any other libraries, but there is no need to install them.

### Normal standard libraries

The available normal standard libraries are listed below with links to their
documentations:

  - [BuiltIn](#builtin)
  - [Collections](#collections)
  - [DateTime](#datetime)
  - [Dialogs](#dialogs)
  - [OperatingSystem](#operatingsystem)
  - [Process](#process)
  - [Screenshot](#screenshot)
  - [String](#string)
  - [Telnet](#telnet)
  - [XML](#xml)


<a id="xml"></a>
<a id="telnet"></a>
<a id="screenshot"></a>
<a id="string"></a>
<a id="process"></a>
<a id="operatingsystem"></a>
<a id="dialogs"></a>
<a id="datetime"></a>
<a id="collections"></a>
<a id="builtin"></a>
### Remote library

In addition to the normal standard libraries listed above, there is
also *Remote* library that is totally different than the other standard
libraries. It does not have any keywords of its own but it works as a
proxy between Robot Framework and actual test library implementations.
These libraries can be running on other machines than the core
framework and can even be implemented using languages not supported by
Robot Framework natively.

See separate [Remote library interface](../extending/remote-library.md#remote-library-interface) section for more information
about this concept.

## External libraries

Any test library that is not one of the standard libraries is, by
definition, *an external library*. The Robot Framework open source community
has implemented several generic libraries, such as [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary) and
[SwingLibrary](https://github.com/robotframework/SwingLibrary), which are not packaged with the core framework. A list of
publicly available libraries can be found from http://robotframework.org.

Generic and custom libraries can obviously also be implemented by teams using
Robot Framework. See [Creating test libraries](../extending/creating-test-libraries.md#creating-test-libraries) section for more information
about that topic.

Different external libraries can have a totally different mechanism
for installing them and taking them into use. Sometimes they may also require
some other dependencies to be installed separately. All libraries
should have clear installation and usage documentation and they should
preferably automate the installation process.
