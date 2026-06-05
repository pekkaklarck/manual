
# Variable files

Variable files contain [variables](variables.md#variables) that can be used in the test
data. Variables can also be created using [Variable sections](variables.md#variable-sections) or [set from
the command line](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data), but variable files allow creating them dynamically
and also make it easy to create other variable values than strings.

Variable files are typically implemented as modules and there are
two different approaches for creating variables:

[Getting variables directly from a module](#getting-variables-directly-from-a-module)
: Variables are specified as module attributes. In simple cases, the
   syntax is so simple that no real programming is needed. For example,
   `MY_VAR = 'my value'` creates a variable `${MY_VAR}` with the specified
   text as its value. One limitation of this approach is that it does
   not allow using arguments.

[Getting variables from a special function](#getting-variables-from-a-special-function)
: Variable files can have a special `get_variables`
   (or `getVariables`) method that returns variables as a mapping.
   Because the method can take arguments this approach is very flexible.

Alternatively variable files can be implemented as [classes](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.to_json)
that the framework will instantiate. Also in this case it is possible to create
variables as attributes or get them dynamically from the `get_variables`
method. Variable files can also be created as [YAML](https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.ResourceFile.from_json) and [JSON](test-data-syntax.md#json-structure).

### Taking variable files into use

#### Setting section

All test data files can import variable files using the `Variables`
setting in the Setting section. Variable files are typically imported using
a path to the file same way as [resource files are imported](resource-files.md#resource-files) using
the `Resource` setting. Similarly to resource files, the path to
the imported variable file is considered relative to the directory where the
importing file is, and if not found, it is searched from directories
in the [module search path](../executing-tests/configuring-execution.md#module-search-path). The path can also contain variables,
and slashes are converted to backslashes on Windows.

Examples:

```robotframework
*** Settings ***
Variables    myvariables.py
Variables    ../data/variables.py
Variables    ${RESOURCES}/common.yaml
```
Starting from Robot Framework 5.0, variable files implemented using Python
can also be imported using the module name [similarly as libraries](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data).
When using this approach, the module needs to be in the [module search path](../executing-tests/configuring-execution.md#module-search-path).

Examples:

```robotframework
*** Settings ***
Variables    myvariables
Variables    rootmodule.Variables
```
If a [variable file accepts arguments](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data), they are specified after the path
or name of the variable file to import:

```robotframework
*** Settings ***
Variables    arguments.py    arg1    ${ARG2}
Variables    arguments    argument
```
All variables from a variable file are available in the test data file
that imports it. If several variable files are imported and they
contain a variable with the same name, the one in the earliest imported file is
taken into use. Additionally, variables created in Variable sections and
set from the command line override variables from variable files.

#### Command line

Another way to take variable files into use is using the command line option
`--variablefile`. Variable files are referenced using a path or
module name similarly as when importing them using the `Variables`
setting. Possible arguments are joined to the path with a colon (`:`):

```
--variablefile myvariables.py
--variablefile path/variables.py
--variablefile /absolute/path/common.py
--variablefile variablemodule
--variablefile arguments.py:arg1:arg2
--variablefile rootmodule.Variables:arg1:arg2
```

Variable files taken into use from the
command line are also searched from the [module search path](../executing-tests/configuring-execution.md#module-search-path) similarly as
variable files imported in the Setting section. Relative paths are considered
relative to the directory where execution is started from.

If a variable file is given as an absolute Windows path, the colon after the
drive letter is not considered a separator:

```
--variablefile C:\path\variables.py
```

It is also possible to use a semicolon
(`;`) as an argument separator. This is useful if variable file arguments
themselves contain colons, but requires surrounding the whole value with
quotes on UNIX-like operating systems:

```
--variablefile C:\path\variables.py;D:\data.xls
--variablefile "myvariables.py;argument:with:colons"
```

Variables in variable files taken use on the command line are globally
available in all test data files, similarly as [individual variables](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#package-data)
set with the `--variable` option. If both `--variablefile` and
`--variable` options are used and there are variables with same
names, those that are set individually with
`--variable` option take precedence.

### Getting variables directly from a module

#### Basic syntax

When variable files are taken into use, they are imported as Python
modules and all their module level attributes that do not start with
an underscore (`_`) are, by default, considered to be variables. Because
variable names are case-insensitive, both lower- and upper-case names are
possible, but in general, capital letters are recommended for global
variables and attributes.

```python
VARIABLE = "An example string"
ANOTHER_VARIABLE = "This is pretty easy!"
INTEGER = 42
STRINGS = ["one", "two", "kolme", "four"]
NUMBERS = [1, INTEGER, 3.14]
MAPPING = {"one": 1, "two": 2, "three": 3}
```
In the example above, variables `${VARIABLE}`, `${ANOTHER VARIABLE}`, and
so on, are created. The first two variables are strings, the third one is
an integer, then there are two lists, and the final value is a dictionary.
All these variables can be used as a [scalar variable](variables.md#scalar-variable), lists and the
dictionary also a [list variable](variables.md#list-variable) like `@{STRINGS}` (in the dictionary's case
that variable would only contain keys), and the dictionary also as a
[dictionary variable](variables.md#dictionary-variable) like `&{MAPPING}`.

To make creating a list variable or a dictionary variable more explicit,
it is possible to prefix the variable name with `LIST__` or `DICT__`,
respectively:

```python
from collections import OrderedDict

LIST__ANIMALS = ["cat", "dog"]
DICT__FINNISH = OrderedDict([("cat", "kissa"), ("dog", "koira")])
```
These prefixes will not be part of the final variable name, but they cause
Robot Framework to validate that the value actually is list-like or
dictionary-like. With dictionaries the actual stored value is also turned
into a special dictionary that is used also when [creating dictionaries](variables.md#creating-dictionaries)
in the Variable section. Values of these dictionaries are accessible
as attributes like `${FINNISH.cat}`. These dictionaries are also ordered, but
preserving the source order requires also the original dictionary to be
ordered.

The variables in both the examples above could be created also using the
Variable section below.

```robotframework
*** Variables ***
${VARIABLE}            An example string
${ANOTHER VARIABLE}    This is pretty easy!
${INTEGER}             ${42}
@{STRINGS}             one          two           kolme         four
@{NUMBERS}             ${1}         ${INTEGER}    ${3.14}
&{MAPPING}             one=${1}     two=${2}      three=${3}
@{ANIMALS}             cat          dog
&{FINNISH}             cat=kissa    dog=koira
```
!!! note
    Variables are not replaced in strings got from variable files.
    For example, `VAR = "an ${example}"` would create
    variable `${VAR}` with a literal string value
    `an ${example}` regardless would variable `${example}`
    exist or not.

#### Using objects as values

Variables in variable files are not limited to having only strings or
other base types as values like Variable sections. Instead, their
variables can contain any objects. In the example below, the variable
`${MAPPING}` contains a Python dictionary and also has two variables
created from a custom object implemented in the same file.

```python
MAPPING = {'one': 1, 'two': 2}

class MyObject:
    def __init__(self, name):
        self.name = name

OBJ1 = MyObject('John')
OBJ2 = MyObject('Jane')
```
#### Creating variables dynamically

Because variable files are created using a real programming language,
they can have dynamic logic for setting variables.

```python
import os
import random
import time

USER = os.getlogin()                # current login name
RANDOM_INT = random.randint(0, 10)  # random integer in range [0,10]
CURRENT_TIME = time.asctime()       # timestamp like 'Thu Apr  6 12:45:21 2006'
if time.localtime()[3] > 12:
    AFTERNOON = True
else:
    AFTERNOON = False
```
The example above uses standard Python libraries to set different
variables, but you can use your own code to construct the values. The
example below illustrates the concept, but similarly, your code could
read the data from a database, from an external file or even ask it from
the user.

```python
import math

def get_area(diameter):
    radius = diameter / 2
    area = math.pi * radius * radius
    return area

AREA1 = get_area(1)
AREA2 = get_area(2)
```
#### Selecting which variables to include

When Robot Framework processes variable files, all their attributes
that do not start with an underscore are expected to be
variables. This means that even functions or classes created in the
variable file or imported from elsewhere are considered variables. For
example, the last example would contain the variables `${math}`
and `${get_area}` in addition to `${AREA1}` and
`${AREA2}`.

Normally the extra variables do not cause problems, but they
could override some other variables and cause hard-to-debug
errors. One possibility to ignore other attributes is prefixing them
with an underscore:

```python
import math as _math

def _get_area(diameter):
    radius = diameter / 2.0
    area = _math.pi * radius * radius
    return area

AREA1 = _get_area(1)
AREA2 = _get_area(2)
```
If there is a large number of other attributes, instead of prefixing
them all, it is often easier to use a special attribute
`__all__` and give it a list of attribute names to be processed
as variables.

```python
import math

__all__ = ['AREA1', 'AREA2']

def get_area(diameter):
    radius = diameter / 2.0
    area = math.pi * radius * radius
    return area

AREA1 = get_area(1)
AREA2 = get_area(2)
```
!!! note
    The `__all__` attribute is also, and originally, used
          by Python to decide which attributes to import
          when using the syntax `from modulename import *`.

The third option to select what variables are actually created is using
a special `get_variables` function discussed below.

### Getting variables from a special function

An alternative approach for getting variables is having a special
`get_variables` function (also camelCase syntax `getVariables` is possible)
in a variable file. If such a function exists, Robot Framework calls it and
expects to receive variables as a Python dictionary with variable names as keys
and variable values as values. Created variables can
be used as scalars, lists, and dictionaries exactly like when [getting
variables directly from a module](#getting-variables-directly-from-a-module), and it is possible to use `LIST__` and
`DICT__` prefixes to make creating list and dictionary variables more explicit.
The example below is functionally identical to the first example related to
[getting variables directly from a module](#getting-variables-directly-from-a-module).

```python
def get_variables():
    variables = {"VARIABLE ": "An example string",
                 "ANOTHER VARIABLE": "This is pretty easy!",
                 "INTEGER": 42,
                 "STRINGS": ["one", "two", "kolme", "four"],
                 "NUMBERS": [1, 42, 3.14],
                 "MAPPING": {"one": 1, "two": 2, "three": 3}}
    return variables
```
`get_variables` can also take arguments, which facilitates changing
what variables actually are created. Arguments to the function are set just
as any other arguments for a Python function. When [taking variable files
into use](#taking-variable-files-into-use), arguments are specified after the path
to the variable file, and in the command line they are separated from the
path with a colon or a semicolon.

The dummy example below shows how to use arguments with variable files. In a
more realistic example, the argument could be a path to an external text file
or database where to read variables from.

```python
variables1 = {'scalar': 'Scalar variable',
              'LIST__list': ['List','variable']}
variables2 = {'scalar' : 'Some other value',
              'LIST__list': ['Some','other','value'],
              'extra': 'variables1 does not have this at all'}

def get_variables(arg):
    if arg == 'one':
        return variables1
    else:
        return variables2
```
Starting from Robot Framework 7.0, arguments to variable files support automatic
argument conversion as well as named argument syntax. For example, a variable
file with `get_variables(first: int = 0, second: str = '')` could be imported
like this:

```robotframework
*** Settings ***
Variables    example.py    42              # Converted to integer.
Variables    example.py    second=value    # Named argument syntax.
```
### Implementing variable file as a class

It is possible to implement variables files also as a class.

#### Implementation

Because variable files are always imported using a file system path,
the class must have the same name as the module it is located in.

The framework will create an instance of the class using no arguments and
variables will be gotten from the instance. Similarly as with modules,
variables can be defined as attributes directly
in the instance or gotten from a special `get_variables` method.

When variables are defined directly in an instance, all attributes containing
callable values are ignored to avoid creating variables from possible methods
the instance has. If you would actually need callable variables, you need
to use other approaches to create variable files.

#### Examples

The first examples create variables from attributes.
It creates variables `${VARIABLE}` and `@{LIST}` from class
attributes and `${ANOTHER VARIABLE}` from an instance attribute.

```python
class StaticExample:
    variable = 'value'
    LIST__list = [1, 2, 3]
    _not_variable = 'starts with an underscore'

    def __init__(self):
        self.another_variable = 'another value'
```
The second examples utilizes dynamic approach for getting variables. It
creates only one variable `${DYNAMIC VARIABLE}`.

```python
class DynamicExample:

    def get_variables(self, *args):
        return {'dynamic variable': ' '.join(args)}
```
### Variable file as YAML

Variable files can also be implemented as [YAML](https://yaml.org) files.
YAML is a data serialization language with a simple and human-friendly syntax
that is nevertheless easy for machines to parse.
The following example demonstrates a simple YAML file:

```yaml
string:   Hello, world!
integer:  42
list:
  - one
  - two
dict:
  one: yksi
  two: kaksi
  with spaces: kolme
```
YAML variable files can be used exactly like normal variable files
from the command line using `--variablefile` option, in the Settings
section using `Variables` setting, and dynamically using the
*Import Variables* keyword. They are automatically recognized by their
extension that must be either *.yaml* or *.yml*.
If the above YAML file is imported, it will create exactly the same variables
as this Variable section:

```robotframework
*** Variables ***
${STRING}     Hello, world!
${INTEGER}    ${42}
@{LIST}       one         two
&{DICT}       one=yksi    two=kaksi    with spaces=kolme
```
YAML files used as variable files must always be mappings on the top level.
As the above example demonstrates, keys and values in the mapping become
variable names and values, respectively. Variable values can be any data
types supported by YAML syntax. If names or values contain non-ASCII
characters, YAML variables files must be UTF-8 encoded.

Mappings used as values are automatically converted to special dictionaries
that are used also when [creating dictionaries](variables.md#creating-dictionaries) in the Variable section.
Most importantly, values of these dictionaries are accessible as attributes
like `${DICT.one}`, assuming their names are valid as Python attribute names.
If the name contains spaces or is otherwise not a valid attribute name, it is
always possible to access dictionary values using syntax like
`${DICT}[with spaces]` syntax.

!!! note
    Using YAML files with Robot Framework requires [PyYAML](http://pyyaml.org) module to be installed. You can typically
    install it with [pip](test-data-syntax.md#pipe-separated-format) like `pip install pyyaml`.

### Variable file as JSON

Variable files can also be implemented as [JSON](https://json.org) files.
Similarly as YAML discussed in the previous section, JSON is a data
serialization format targeted both for humans and machines. It is based on
JavaScript syntax and it is not as human-friendly as YAML, but it still
relatively easy to understand and modify. The following example contains
exactly the same data as the earlier YAML example:

```json
{
    "string": "Hello, world!",
    "integer": 42,
    "list": [
        "one",
        "two"
    ],
    "dict": {
        "one": "yksi",
        "two": "kaksi",
        "with spaces": "kolme"
    }
}
```
JSON variable files are automatically recognized by their *.json*
extension and they can be used exactly like YAML variable files. They
also have exactly same requirements for structure, encoding, and so on.
Unlike YAML, Python supports JSON out-of-the-box so no extra modules need
to be installed.

!!! note
    Support for JSON variable files is new in Robot Framework 6.1.
