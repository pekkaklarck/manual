
<a id="library-api"></a>
# Creating test libraries

Robot Framework's actual testing capabilities are provided by test
libraries. There are many existing libraries, some of which are even
bundled with the core framework, but there is still often a need to
create new ones. This task is not too complicated because, as this
chapter illustrates, Robot Framework's library API is simple
and straightforward.

## Introduction

### Supported programming languages

Robot Framework itself is written with [Python](../executing-tests/configuring-execution.md#pythonpath) and naturally test
libraries extending it can be implemented using the same
language. It is also possible to implement libraries with C
using [Python C API](http://docs.python.org/c-api/index.html), although it is often easier to interact with
C code from Python libraries using [ctypes](http://docs.python.org/library/ctypes.html) module.

Libraries implemented using Python can
also act as wrappers to functionality implemented using other
programming languages. A good example of this approach is the [Remote
library](../creating-test-data/using-test-libraries.md#remote-library), and another widely used approaches is running external
scripts or tools as separate processes.

### Different library APIs

Robot Framework has two different library APIs.

Static API

  The simplest approach is having a module or a class
  with functions/methods which map directly to
  [keyword names](#keyword-names). Keywords also take the same [arguments](https://docs.python.org/3/reference/simple_stmts.html#import) as
  the methods implementing them.  Keywords [report failures](https://docs.python.org/3/reference/datamodel.html#object.__getattr__) with
  exceptions, [log](https://docs.python.org/tutorial/controlflow.html#keyword-arguments) by writing to standard output and can [return
  values](https://www.python.org/dev/peps/pep-3102) using the `return` statement.

Dynamic API

  Dynamic libraries are classes that implement a method to get the names
  of the keywords they implement, a method to execute a specified keyword
  with given arguments, and various optional methods for providing more
  information about the implemented keywords and the library itself.
  The names of the keywords to implement, as well as how they are executed,
  can be determined dynamically at runtime, but reporting the status, logging
  and returning values is done similarly as in the static API.

This chapter concentrates on the static API and there is a separate chapter
about the [dynamic library API](dynamic-library-api.md#dynamic-library-api).

## Creating test library class or module

Test libraries can be implemented as Python modules or classes.

### Library name

As discussed under the [Using test libraries](../creating-test-data/using-test-libraries.md#using-test-libraries) section, libraries can
be [imported by name or path](https://www.python.org/dev/peps/pep-0570/):

```robotframework
*** Settings ***
Library    MyLibrary
Library    module.LibraryClass
Library    path/AnotherLibrary.py
```
When a library is imported by a name, the library module must be in the
[module search path](../executing-tests/configuring-execution.md#module-search-path) and the name can either refer to a library module
or to a library class. When a name refers directly to a library class,
the name must be in format like `modulename.ClassName`. Paths to libraries
always refer to modules.

Even when a library import refers to a module, either by a name or by a path,
a class in the module, not the module itself, is used as a library in these cases:

1. If the module contains a class that has the same name as the module.
   The class can be either implemented in the module or imported into it.

   This makes it possible to import libraries using simple names like `MyLibrary`
   instead of specifying both the module and the class like `module.MyLibrary` or
   `MyLibrary.MyLibrary`. When importing a library by a path, it is not even
   possible to directly refer to a library class and automatically using a class
   from the imported module is the only option.

2. If the module contains exactly one class decorated with the [@library decorator](#library-decorator).
   In this case the class needs to be implemented in the module, not imported to it.

   This approach has all the same benefits as the earlier one, but it also allows
   the class name to differ from the module name.

   Using the [@library decorator](#library-decorator) for this purpose is new in Robot Framework 7.2.

!!! tip
    If the library name is really long, it is often a good idea to give
    it a [simpler alias](http://docs.python.org/c-api/index.html) at the import time.

### Providing arguments to libraries

All test libraries implemented as classes can take arguments. These
arguments are specified after the library name when the library is imported,
and when Robot Framework creates an instance of the imported library,
it passes them to its constructor. Libraries implemented as a module
cannot take any arguments.

The number of arguments needed by the library is the same
as the number of arguments accepted by the library's `__init__` method.
The default values, argument conversion, and other such features work
the same way as with [keyword arguments](../creating-test-data/creating-user-keywords.md#user-keyword-arguments). Arguments passed
to the library, as well as the library name itself, can be specified
using variables, so it is possible to alter them, for example, from the
command line.

```robotframework
*** Settings ***
Library    MyLibrary     10.0.0.1    8080
Library    AnotherLib    ${ENVIRONMENT}
```
Example implementations for the libraries used in the above example:

```python
from example import Connection

class MyLibrary:

    def __init__(self, host, port=80):
        self.connection = Connection(host, port)

    def send_message(self, message):
        self.connection.send(message)
```
```python
class AnotherLib:

    def __init__(self, environment):
        self.environment = environment

    def do_something(self):
        if self.environment == 'test':
            do_something_in_test_environment()
        else:
            do_something_in_other_environments()
```
If a library is imported multiple times with different arguments within a single
suite, it needs to be given a [custom name](http://docs.python.org/c-api/index.html) or otherwise latter imports are ignored:

```robotframework
*** Settings ***
Library    MyLibrary     10.0.0.1    8080    AS    RemoteLibrary
Library    MyLibrary     127.0.0.1    AS    LocalLibrary

*** Test Cases ***
Example
    RemoteLibrary.Send Message    Hello!
    LocalLibrary.Send Message    Hi!
```

### Library scope

Libraries implemented as classes can have an internal state, which can
be altered by keywords and with arguments to the constructor of the
library. Because the state can affect how keywords actually behave, it
is important to make sure that changes in one test case do not
accidentally affect other test cases. These kind of dependencies may
create hard-to-debug problems, for example, when new test cases are
added and they use the library inconsistently.

Robot Framework attempts to keep test cases independent from each
other: by default, it creates new instances of test libraries for
every test case. However, this behavior is not always desirable,
because sometimes test cases should be able to share a common
state. Additionally, all libraries do not have a state and creating
new instances of them is simply not needed.

Test libraries can control when new libraries are created with a
class attribute `ROBOT_LIBRARY_SCOPE` . This attribute must be
a string and it can have the following three values:

`TEST`
  A new instance is created for every test case. A possible suite setup
  and suite teardown share yet another instance.

  Prior to Robot Framework 3.2 this value was `TEST CASE`, but nowadays
  `TEST` is recommended. Because all unrecognized values are considered
  same as `TEST`, both values work with all versions. For the same reason
  it is possible to also use value `TASK` if the library is targeted for
  [RPA](../creating-test-data/creating-tasks.md#rpa) usage more than testing. `TEST` is also the default value if the
  `ROBOT_LIBRARY_SCOPE` attribute is not set.

`SUITE`
  A new instance is created for every test suite. The lowest-level test
  suites, created from test case files and containing test cases, have
  instances of their own, and higher-level suites all get their own instances
  for their possible setups and teardowns.

  Prior to Robot Framework 3.2 this value was `TEST SUITE`. That value still
  works, but `SUITE` is recommended with libraries targeting Robot Framework
  3.2 and newer.

`GLOBAL`
  Only one instance is created during the whole test execution and it
  is shared by all test cases and test suites. Libraries created from
  modules are always global.

!!! note
    If a library is imported multiple times with different [arguments](http://docs.python.org/c-api/index.html),
    a new instance is created every time regardless the scope.

When the `SUITE` or `GLOBAL` scopes are used with libraries that have a state,
it is recommended that libraries have some
special keyword for cleaning up the state. This keyword can then be
used, for example, in a suite setup or teardown to ensure that test
cases in the next test suites can start from a known state. For example,
*SeleniumLibrary* uses the `GLOBAL` scope to enable
using the same browser in different test cases without having to
reopen it, and it also has the *Close All Browsers* keyword for
easily closing all opened browsers.

Example library using the `SUITE` scope:

```python
class ExampleLibrary:
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self._counter = 0

    def count(self):
        self._counter += 1
        print(self._counter)

    def clear_count(self):
        self._counter = 0
```

### Library version

When a test library is taken into use, Robot Framework tries to
determine its version. This information is then written into the [syslog](../executing-tests/result-files.md#syslog)
to provide debugging information. Library documentation tool
[Libdoc](../supporting-tools/libdoc.md#libdoc) also writes this information into the keyword
documentations it generates.

Version information is read from attribute
`ROBOT_LIBRARY_VERSION`, similarly as [library scope](#library-scope) is
read from `ROBOT_LIBRARY_SCOPE`. If
`ROBOT_LIBRARY_VERSION[ does not exist, information is tried to
be read from ](http://docs.python.org/c-api/index.html)version__[ attribute. These attributes must be
class or module attributes, depending whether the library is
implemented as a class or a module.

An example module using ](http://docs.python.org/library/ctypes.html)version__`:

```python
__version__ = '0.1'

def keyword():
    pass
```
### Documentation format

Library documentation tool [Libdoc](../supporting-tools/libdoc.md#libdoc)
supports documentation in multiple formats. If you want to use something
else than Robot Framework's own [documentation formatting](../appendices/documentation-formatting.md#documentation-formatting), you can specify
the format in the source code using  `ROBOT_LIBRARY_DOC_FORMAT` attribute
similarly as [scope](http://docs.python.org/c-api/index.html) and [version](http://docs.python.org/library/ctypes.html) are set with their own
`ROBOT_LIBRARY_*` attributes.

The possible case-insensitive values for documentation format are
`ROBOT` (default), `HTML`, `TEXT` (plain text),
and `reST` ([reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText)). Using the `reST` format requires
the [docutils](https://pypi.python.org/pypi/docutils) module to be installed when documentation is generated.

Setting the documentation format is illustrated by the following example that
uses reStructuredText format.
See [Documenting libraries](#documenting-libraries) section and [Libdoc](../supporting-tools/libdoc.md#libdoc) chapter for more information
about documenting test libraries in general.

```python
"""A library for *documentation format* demonstration purposes.

This documentation is created using reStructuredText__. Here is a link
to the only \`Keyword\`.

"""

ROBOT_LIBRARY_DOC_FORMAT = 'reST'

def keyword():
    """**Nothing** to see here. Not even in the table below.

    =======  =====  =====
    Table    here   has
    nothing  to     see.
    =======  =====  =====
    """
    pass
```

### Library acting as listener

[Listener interface](listener-interface.md#listener-interface) allows external listeners to get notifications about
test execution. They are called, for example, when suites, tests, and keywords
start and end. Sometimes getting such notifications is also useful for test
libraries, and they can register a custom listener by using
`ROBOT_LIBRARY_LISTENER` attribute. The value of this attribute
should be an instance of the listener to use, possibly the library itself.

For more information and examples see [Libraries as listeners](listener-interface.md#libraries-as-listeners) section.

### `@library` decorator

An easy way to configure libraries implemented as classes is using
the `robot.api.deco.library` class decorator. It allows configuring library's
[scope](http://docs.python.org/c-api/index.html), [version](http://docs.python.org/library/ctypes.html), [custom argument converters](https://docs.python.org/3/reference/simple_stmts.html#import), [documentation format](#documentation-format)
and [listener](https://docs.python.org/3/reference/datamodel.html#object.__getattr__) with optional arguments `scope`, `version`, `converter`,
`doc_format` and `listener`, respectively. When these arguments are used, they
set the matching `ROBOT_LIBRARY_SCOPE`, `ROBOT_LIBRARY_VERSION`,
`ROBOT_LIBRARY_CONVERTERS`, `ROBOT_LIBRARY_DOC_FORMAT` and `ROBOT_LIBRARY_LISTENER`
attributes automatically:

```python
from robot.api.deco import library

from example import Listener

@library(scope='GLOBAL', version='3.2b1', doc_format='reST', listener=Listener())
class Example:
    ...
```
The `@library` decorator also disables the [automatic keyword discovery](http://docs.python.org/c-api/index.html)
by setting the `ROBOT_AUTO_KEYWORDS` argument to `False` by default. This
means that it is mandatory to decorate methods with the [@keyword decorator](https://www.python.org/dev/peps/pep-0570/)
to expose them as keywords. If only that behavior is desired and no further
configuration is needed, the decorator can also be used without parenthesis
like:

```python
from robot.api.deco import library

@library
class Example:
    ...
```
If needed, the automatic keyword discovery can be enabled by using the
`auto_keywords` argument:

```python
from robot.api.deco import library

@library(scope='GLOBAL', auto_keywords=True)
class Example:
    ...
```
The `@library` decorator only sets class attributes `ROBOT_LIBRARY_SCOPE`,
`ROBOT_LIBRARY_VERSION`, `ROBOT_LIBRARY_CONVERTERS`, `ROBOT_LIBRARY_DOC_FORMAT`
and `ROBOT_LIBRARY_LISTENER` if the respective arguments `scope`, `version`,
`converters`, `doc_format` and `listener` are used. The `ROBOT_AUTO_KEYWORDS`
attribute is set always and its presence can be used as an indication that
the `@library` decorator has been used. When attributes are set, they
override possible existing class attributes.

When a class is decorated with the `@library` decorator, it is used as a library
even when a [library import refers only to a module containing it](http://docs.python.org/c-api/index.html). This is done
regardless does the class name match the module name or not.

!!! note
    The `@library` decorator is new in Robot Framework 3.2,
    the `converters` argument is new in Robot Framework 5.0, and
    specifying that a class in an imported module should be used as
    a library is new in Robot Framework 7.2.

<a id="static-library-api"></a>
## Creating keywords

### What methods are considered keywords

Robot Framework, by default, uses introspection to find out what attributes
a library contains, and considers all functions and methods that do not start
with an underscore to be keywords. For example, this library implements a single
keyword *My Keyword*:

```python
def my_keyword(arg):
    return _helper(arg)

def _helper(arg):
    return arg.upper()
```
!!! note
    In Python anything starting with an underscore is considered private
    and Robot Framework follows that convention.

Automatically considering all public methods and functions to be keywords typically
works well, especially in simple cases, but there are situations where it is not
desired. For example, when implementing a library as class, it can be a surprise that
also methods in possible base classes are considered keywords. When implementing
a library as a module, functions imported into the module namespace becoming keywords
is probably even a bigger surprise. For example, this library implements a keyword
*Example Keyword*, as expected, but also a keyword *Current Thread*:

```python
from threading import current_thread

def example_keyword():
    name = current_thread().name
    print(f"Running in thread '{name}'.")
```
The next section explain different ways how to control the keyword
discovery and avoid problems like the one above.

### Controlling keyword discovery

This section explains how to control which methods and functions become keywords.

#### Avoiding imported public functions with module based libraries

As the previous section explained, with module based libraries also imported
functions become keywords. The are two simple ways how imports themselves can be
adjusted to avoid this problem:

1. Import only modules, not functions:

    ```python
import threading

def example_keyword():
: name = threading.current_thread().name
    print(f"Running in thread '{name}'.")
```
2. Use import aliases to prefix imported functions with an underscore:

    ```python
from threading import current_thread as _current_thread

def example_keyword():
    name = _current_thread().name
    print(f"Running in thread '{name}'.")
```
Although both of these solutions are simple, they are not very explicit and
there is a risk that someone refactors the code so that functions are exposed
as keywords. Adding a comment or using the approaches discussed below for
limiting what keywords are exposed can be a good idea, at least if a library
grows bigger.

#### Using `@library` decorator

With class based libraries the easiest way to disable public methods becoming
keywords is using the [@library decorator](#library-decorator). This decorator, by default, disables
the automatic keyword discovery and requires keywords to be explicitly marked
with the [@keyword decorator](#implicit-argument-types-based-on-default-values). For example, this library creates single keyword
*My Keyword*:

```python
from robot.api.deco import keyword, library

@library
class MyLibrary:

    @keyword
    def my_keyword(self, arg):
        return self.helper(arg)

    def helper(self, arg):
        return arg.upper()
```
#### Using `ROBOT_AUTO_KEYWORDS` attribute

An alternative to using the `@library` decorator for disabling the automatic
keyword discovery is setting the special `ROBOT_AUTO_KEYWORDS` attribute to
`False`. This is especially useful with module based libraries that cannot
themselves be decorated:

```python
from robot.api.deco import keyword

ROBOT_AUTO_KEYWORDS = False

@keyword
def my_keyword(arg):
    return helper(arg)

def helper(arg):
    return arg.upper()
```
!!! note
    The `@library` decorator internally sets the `ROBOT_AUTO_KEYWORDS`
    attribute as well.

#### Using `@not_keyword` decorator

Functions in modules and methods in classes can be explicitly marked as
"not keywords" by using the `@not_keyword` decorator:

```python
from robot.api.deco import not_keyword

def my_keyword(arg):
    return helper(arg)

@not_keyword
def helper(arg):
    return arg.upper()
```
When a library is implemented as a module, this decorator can be explicitly called
to avoid exposing imported functions as keywords:

```python
from threading import current_thread

from robot.api.deco import not_keyword

not_keyword(current_thread)  # Don't expose `current_thread` as a keyword.

def example_keyword():
    thread_name = current_thread().name
    print(f"Running in thread '{thread_name}'.")
```
#### Using `__all__[ attribute

Python modules can define the special ](http://docs.python.org/c-api/index.html)all__` attribute to specify what
[public names](http://docs.python.org/library/ctypes.html) they contain. If a module based library has such an attribute,
Robot Framework respects it and considers only listed functions as keywords:

```python
__all__ = ["my_keyword"]

def my_keyword(arg):
    return helper(arg)

def helper(arg):
    return arg.upper()
```

<a id="hybrid-library-api"></a>
#### Using `get_keyword_names` method

Class based libraries can explicitly tell to Robot Framework which methods are
keywords by using the special `get_keyword_names` method  that must return a list
of exposed method names:

```python
class MyLibrary:

    def get_keyword_names(self):
        return ["my_keyword"]

    def my_keyword(self, arg):
        return self.helper(arg)

    def helper(self, arg):
        return arg.upper()
```
Everything else than getting the list of method names works exactly the same way
as with other static libraries. It is, however, possible to create the actual
keywords dynamically by utilizing Python's [__getattr__](http://docs.python.org/c-api/index.html) method that is called
by Python if a returned method name does not exist:

```python
class MyLibrary:

    def get_keyword_names(self):
        return ["normal_keyword", "dynamic_keyword"]

    def normal_keyword(self, arg):
        print("This is a normal keyword.")

    def __getattr__(self, name):
        if name != "dynamic_keyword":
            raise AttributeError(name)

        def dynamically_created_keyword():
            print("This is a dynamically created keyword.")

        return dynamically_created_keyword
```
In the above example the actual keyword is defined inside the `__getattr__` method.
In more realistic cases it could, for example, be imported or got dynamically from
some object.

!!! note
    Libraries having the `get_keyword_names` method, but otherwise working
    the same way as normal static libraries, are sometimes called
    *hybrid libraries* and this API can be called the *hybrid library API*.
    The reason is that libraries using the [dynamic library API](dynamic-library-api.md#dynamic-library-api) also
    specify their keywords using the `get_keyword_names` method, but
    they also execute keywords differently.

!!! note
    Due to legacy reasons the `get_keyword_names` method can also be
    spelled like `getKeywordNames`. The former variant is recommended,
    though.

#### Using dynamic library API

The [dynamic library API](dynamic-library-api.md#dynamic-library-api) requires explicitly listing the implemented keywords
by using the `get_keyword_names` method. That entirely avoids the problem that
methods or functions could accidentally be exposed as keywords.

### Keyword names

Keyword names used in the test data are compared with method names to
find the method implementing these keywords. Name comparison is
case-insensitive, and also spaces and underscores are ignored. For
example, the method `hello` maps to the keyword name
*Hello*, *hello* or even *h e l l o*. Similarly both the
`do_nothing` and `doNothing` methods can be used as the
*Do Nothing* keyword in the test data.

Example library implemented as a module in the *MyLibrary.py* file:

```python
def hello(name):
    print(f"Hello, {name}!")

def do_nothing():
    pass
```
The example below illustrates how the example library above can be
used. If you want to try this yourself, make sure that the library is
in the [module search path](../executing-tests/configuring-execution.md#module-search-path).

```robotframework
*** Settings ***
Library    MyLibrary

*** Test Cases ***
My Test
    Do Nothing
    Hello    world
```
#### Setting custom name

It is possible to expose a different name for a keyword instead of the
default keyword name which maps to the method name.  This can be accomplished
by setting the `robot_name` attribute on the method to the desired custom name:

```python
def login(username, password):
    ...

login.robot_name = 'Login via user panel'
```
```robotframework
*** Test Cases ***
My Test
    Login Via User Panel    ${username}    ${password}
```
Instead of explicitly setting the `robot_name` attribute like in the above
example, it is typically easiest to use the [@keyword decorator](#specifying-argument-types-using-function-annotations):

```python
from robot.api.deco import keyword

@keyword('Login via user panel')
def login(username, password):
    ...
```
Using this decorator without an argument will have no effect on the exposed
keyword name, but will still set the `robot_name` attribute.  This allows
[marking methods to expose as keywords](dynamic-library-api.md#marking-methods-to-expose-as-keywords) without actually changing keyword
names. Methods that have the `robot_name`
attribute also create keywords even if the method name itself would start with
an underscore.

Setting a custom keyword name can also enable library keywords to accept
arguments using the [embedded arguments](http://docs.python.org/c-api/index.html) syntax.

### Keyword tags

Library keywords and [user keywords](http://docs.python.org/library/ctypes.html) can have tags. Library keywords can
define them by setting the `robot_tags` attribute on the method to a list
of desired tags. Similarly as when [setting custom name](#setting-custom-name), it is easiest to
set this attribute by using the [@keyword decorator](#keyword-decorator):

```python
from robot.api.deco import keyword

@keyword(tags=['tag1', 'tag2'])
def login(username, password):
    ...

@keyword('Custom name', ['tags', 'here'])
def another_example():
    ...
```
Another option for setting tags is giving them on the last line of
[keyword documentation](http://docs.python.org/c-api/index.html) with `Tags:` prefix and separated by a comma. For
example:

```python
def login(username, password):
    """Log user in to SUT.

    Tags: tag1, tag2
    """
    .<a id="user-keyword-tags-documenting-libraries-keyword-arguments-with-a-static-and-hybrid-api-the-information-on-how-many-arguments-a-keyword-needs-is-got-directly-from-the-method-that-implements-it-libraries-using-the-dynamic-library-api-have-other-means-for-sharing-this-information-so-this-section-is-not-relevant-to-them-the-most-common-and-also-the-simplest-situation-is-when-a-keyword-needs-an-exact-number-of-arguments-in-this-case-the-method-simply-take-exactly-those-arguments-for-example-a-method-implementing-a-keyword-with-no-arguments-takes-no-arguments-either-a-method-implementing-a-keyword-with-one-argument-also-takes-one-argument-and-so-on-example-keywords-taking-different-numbers-of-arguments"></a>
```
```python
def no_arguments():
    print("Keyword got no arguments.")

def one_argument(arg):
    print(f"Keyword got one argument '{arg}'.")

def three_arguments(a1, a2, a3):
    print(f"Keyword got three arguments '{a1}', '{a2}' and '{a3}'.")
```
### Default values to keywords

It is often useful that some of the arguments that a keyword uses have
default values.

In Python a method has always exactly one implementation and possible
default values are specified in the method signature. The syntax,
which is familiar to all Python programmers, is illustrated below:

```python
def one_default(arg='default'):
    print(f"Got argument '{arg}'.")

def multiple_defaults(arg1, arg2='default 1', arg3='default 2'):
    print(f"Got arguments '{arg1}', '{arg2}' and '{arg3}'.")
```
The first example keyword above can be used either with zero or one
arguments. If no arguments are given, `arg` gets the value
`default`. If there is one argument, `arg` gets that value,
and calling the keyword with more than one argument fails. In the
second example, one argument is always required, but the second and
the third one have default values, so it is possible to use the keyword
with one to three arguments.

```robotframework
*** Test Cases ***
Defaults
    One Default
    One Default    argument
    Multiple Defaults    required arg
    Multiple Defaults    required arg    optional
    Multiple Defaults    required arg    optional 1    optional 2
```
<a id="varargs-library"></a>
### Variable number of arguments (`*varargs`)

Robot Framework supports also keywords that take any number of
arguments.

Python supports methods accepting any number of arguments. The same
syntax works in libraries and, as the examples below show, it can also
be combined with other ways of specifying arguments:

```python
def any_arguments(*args):
    print("Got arguments:")
    for arg in args:
        print(arg)

def one_required(required, *others):
    print(f"Required: {required}\nOthers:")
    for arg in others:
        print(arg)

def also_defaults(req, def1="default 1", def2="default 2", *rest):
    print(req, def1, def2, rest)
```
```robotframework
*** Test Cases ***
Varargs
    Any Arguments
    Any Arguments    argument
    Any Arguments    arg 1    arg 2    arg 3    arg 4    arg 5
    One Required     required arg
    One Required     required arg    another arg    yet another
    Also Defaults    required
    Also Defaults    required    these two    have defaults
    Also Defaults    1    2    3    4    5    6
```
<a id="kwargs-library"></a>
### Free keyword arguments (`**kwargs`)

Robot Framework supports [Python's **kwargs syntax](http://docs.python.org/c-api/index.html).
How to use use keywords that accept *free keyword arguments*,
also known as *free named arguments*, is [discussed under the Creating test
cases section](http://docs.python.org/library/ctypes.html). In this section we take a look at how to create such keywords.

If you are already familiar how kwargs work with Python, understanding how
they work with Robot Framework test libraries is rather simple. The example
below shows the basic functionality:

```python
def example_keyword(**stuff):
    for name, value in stuff.items():
        print(name, value)
```
```robotframework
*** Test Cases ***
Keyword Arguments
    Example Keyword    hello=world        # Logs 'hello world'.
    Example Keyword    foo=1    bar=42    # Logs 'foo 1' and 'bar 42'.
```
Basically, all arguments at the end of the keyword call that use the
[named argument syntax](../creating-test-data/creating-test-cases.md#named-argument-syntax) `name=value`, and that do not match any
other arguments, are passed to the keyword as kwargs. To avoid using a literal
value like `foo=quux` as a free keyword argument, it must be [escaped](http://docs.python.org/c-api/index.html)
like `foo\=quux`.

The following example illustrates how normal arguments, varargs, and kwargs
work together:

```python
def various_args(arg=None, *varargs, **kwargs):
    if arg is not None:
        print('arg:', arg)
    for value in varargs:
        print('vararg:', value)
    for name, value in sorted(kwargs.items()):
        print('kwarg:', name, value)
```
```robotframework
*** Test Cases ***
Positional
    Various Args    hello    world                # Logs 'arg: hello' and 'vararg: world'.

Named
    Various Args    arg=value                     # Logs 'arg: value'.

Kwargs
    Various Args    a=1    b=2    c=3             # Logs 'kwarg: a 1', 'kwarg: b 2' and 'kwarg: c 3'.
    Various Args    c=3    a=1    b=2             # Same as above. Order does not matter.

Positional and kwargs
    Various Args    1    2    kw=3                # Logs 'arg: 1', 'vararg: 2' and 'kwarg: kw 3'.

Named and kwargs
    Various Args    arg=value      hello=world    # Logs 'arg: value' and 'kwarg: hello world'.
    Various Args    hello=world    arg=value      # Same as above. Order does not matter.
```
For a real world example of using a signature exactly like in the above
example, see *Run Process* and *Start Keyword* keywords in the
[Process](../creating-test-data/using-test-libraries.md#process) library.

### Keyword-only arguments

Starting from Robot Framework 3.1, it is possible to use [named-only arguments](../creating-test-data/creating-test-cases.md#named-only-arguments)
with different keywords. This support
is provided by Python's [keyword-only arguments](http://docs.python.org/c-api/index.html). Keyword-only arguments
are specified after possible `*varargs` or after a dedicated `*` marker when
`*varargs` are not needed. Possible `**kwargs` are specified after keyword-only
arguments.

Example:

```python
def sort_words(*words, case_sensitive=False):
    key = str.lower if case_sensitive else None
    return sorted(words, key=key)

def strip_spaces(word, *, left=True, right=True):
    if left:
        word = word.lstrip()
    if right:
        word = word.rstrip()
    return word
```
```robotframework
*** Test Cases ***
Example
    Sort Words    Foo    bar    baZ
    Sort Words    Foo    bar    baZ    case_sensitive=True
    Strip Spaces    ${word}    left=False
```

### Positional-only arguments

Python supports so called [positional-only arguments](http://docs.python.org/c-api/index.html) that make it possible to
specify that an argument can only be given as a [positional argument](../creating-test-data/creating-test-cases.md#positional-argument), not as
a [named argument](../creating-test-data/creating-test-cases.md#named-argument) like `name=value`. Positional-only arguments are specified
before normal arguments and a special `/` marker must be used after them:

```python
def keyword(posonly, /, normal):
    print(f"Got positional-only argument {posonly} and normal argument {normal}.")
```
The above keyword could be used like this:

```robotframework
*** Test Cases ***
Example
    # Positional-only and normal argument used as positional arguments.
    Keyword    foo    bar
    # Normal argument can also be named.
    Keyword    foo    normal=bar
```
If a positional-only argument is used with a value that contains an equal sign
like `example=usage`, it is not considered to mean [named argument syntax](../creating-test-data/creating-test-cases.md#named-argument-syntax)
even if the part before the `=` would match the argument name. This rule
only applies if the positional-only argument is used in its correct position
without other arguments using the name argument syntax before it, though.

```robotframework
*** Test Cases ***
Example
    # Positional-only argument gets literal value `posonly=foo` in this case.
    Keyword    posonly=foo    normal=bar
    # This fails.
    Keyword    normal=bar    posonly=foo
```
Positional-only arguments are fully supported starting from Robot Framework 4.0.
Using them as positional arguments works also with earlier versions,
but using them as named arguments causes an error on Python side.

### Argument conversion

Arguments defined in Robot Framework test data are, by default,
passed to keywords as Unicode strings. There are, however, several ways
to use non-string values as well:

- [Variables](../creating-test-data/variables.md#variables) can contain any kind of objects as values, and variables used
  as arguments are passed to keywords as-is.
- Keywords can themselves [convert arguments they accept](http://docs.python.org/c-api/index.html) to other types.
- It is possible to specify argument types explicitly using
  [function annotations](http://docs.python.org/library/ctypes.html) or the [@keyword decorator](https://docs.python.org/3/reference/simple_stmts.html#import). In these cases
  Robot Framework converts arguments automatically.
- Automatic conversion is also done based on [keyword default values](https://docs.python.org/3/reference/datamodel.html#object.__getattr__).
- Libraries can register [custom argument converters](#library-scope).

Automatic argument conversion based on function annotations, types specified
using the `@keyword` decorator, and argument default values are all new
features in Robot Framework 3.1. The [Supported conversions](#supported-conversions) section
specifies which argument conversion are supported in these cases.

Prior to Robot Framework 4.0, automatic conversion was done only if the given
argument was a string. Nowadays it is done regardless the argument type.

#### Manual argument conversion

If no type information is specified to Robot Framework, all arguments not
passed as [variables](../creating-test-data/variables.md#variables) are given to keywords as Unicode strings. This includes
cases like this:

```robotframework
*** Test Cases ***
Example
    Example Keyword    42    False
```
It is always possible to convert arguments passed as strings insider keywords.
In simple cases this means using `int()` or `float()` to convert arguments
to numbers, but other kind of conversion is possible as well. When working
with Boolean values, care must be taken because all non-empty strings,
including string `False`, are considered true by Python. Robot Framework's own
`robot.utils.is_truthy()` utility handles this nicely as it considers strings
like `FALSE`, `NO` and `NONE` (case-insensitively) to be false:

```python
from robot.utils import is_truthy

def example_keyword(count, case_insensitive):
    count = int(count)
    if is_truthy(case_insensitive):
        ...
```
Keywords can also use Robot Framework's argument conversion functionality via
the [robot.api.TypeInfo](http://docs.python.org/c-api/index.html) class and its `convert` method. This can be useful
if the needed conversion logic is more complicated or the are needs for better
error reporting than what simply using, for example, `int()` provides.

```python
from robot.api import TypeInfo

def example_keyword(count, case_insensitive):
    count = TypeInfo.from_type(int).convert(count)
    if TypeInfo.from_type(bool).convert(case_insensitive):
        ...
```
!!! tip
    It is generally recommended to specify types using type hints or otherwise
    and let Robot Framework handle argument conversion automatically. Manual
    argument conversion should only be needed in special cases.

!!! note
    `robot.api.TypeInfo` is new in Robot Framework 7.0.

#### Specifying argument types using function annotations

Starting from Robot Framework 3.1, arguments passed to keywords are automatically
converted if argument type information is available and the type is recognized.
The most natural way to specify types is using Python [function annotations](https://www.python.org/dev/peps/pep-3107/).
For example, the keyword in the previous example could be implemented as
follows and arguments would be converted automatically:

```python
def example_keyword(count: int, case_insensitive: bool = True):
    if case_insensitive:
        ...
```
See the [Supported conversions](#supported-conversions) section below for a list of types that
are automatically converted and what values these types accept. It is
an error if an argument having one of the supported types is given
a value that cannot be converted. Annotating only some of the arguments
is fine.

Annotating arguments with other than the supported types is not an error,
and it is also possible to use annotations for other than typing
purposes. In those cases no conversion is done, but annotations are
nevertheless shown in the documentation generated by [Libdoc](../supporting-tools/libdoc.md#libdoc).

Keywords can also have a return type annotation specified using the `->`
notation at the end of the signature like `def example() -> int:`.
This information is not used for anything during execution, but starting from
Robot Framework 7.0 it is shown by [Libdoc](../supporting-tools/libdoc.md#libdoc) for documentation purposes.

#### Specifying argument types using `@keyword` decorator

An alternative way to specify explicit argument types is using the
[@keyword decorator](#keyword-decorator). Starting from Robot Framework 3.1,
it accepts an optional `types` argument that can be used to specify argument
types either as a dictionary mapping argument names to types or as a list
mapping arguments to types based on position. These approaches are shown
below implementing the same keyword as in earlier examples:

```python
from robot.api.deco import keyword

@keyword(types={'count': int, 'case_insensitive': bool})
def example_keyword(count, case_insensitive=True):
    if case_insensitive:
        ...

@keyword(types=[int, bool])
def example_keyword(count, case_insensitive=True):
    if case_insensitive:
        ...
```
Regardless of the approach that is used, it is not necessarily to specify
types for all arguments. When specifying types as a list, it is possible
to use `None` to mark that a certain argument does not have type information
and arguments at the end can be omitted altogether. For example, both of these
keywords specify the type only for the second argument:

```python
@keyword(types={'second': float})
def example1(first, second, third):
    ...

@keyword(types=[None, float])
def example2(first, second, third):
    ...
```
Starting from Robot Framework 7.0, it is possible to specify the keyword return
type by using key `'return'` with an appropriate type in the type dictionary.
This information is not used for anything during execution, but it is shown by
[Libdoc](../supporting-tools/libdoc.md#libdoc) for documentation purposes.

If any types are specified using the `@keyword` decorator, type information
got from [annotations](http://docs.python.org/c-api/index.html) is ignored with that keyword. Setting `types` to `None`
like `@keyword(types=None)` disables type conversion altogether so that also
type information got from [default values](http://docs.python.org/library/ctypes.html) is ignored.

#### Implicit argument types based on default values

If type information is not got explicitly using annotations or the `@keyword`
decorator, Robot Framework 3.1 and newer tries to get it based on possible
argument default value. In this example `count` and `case_insensitive` get
types `int` and `bool`, respectively:

```python
def example_keyword(count=-1, case_insensitive=True):
    if case_insensitive:
        ...
```
When type information is got implicitly based on the default values,
argument conversion itself is not as strict as when the information is
got explicitly:

- Conversion may be attempted also to other "similar" types. For example,
  if converting to an integer fails, float conversion is attempted.

- Conversion failures are not errors, keywords get the original value in
  these cases instead.

If an argument has an explicit type and a default value, conversion is first
attempted based on the explicit type. If that fails, then conversion is attempted
based on the default value. In this special case conversion based on the default
value is strict and a conversion failure causes an error.

If argument conversion based on default values is not desired, the whole
argument conversion can be disabled with the [@keyword decorator](http://docs.python.org/c-api/index.html) like
`@keyword(types=None)`.

!!! note
    Prior to Robot Framework 4.0 conversion was done based on the default
    value only if the argument did not have an explict type.

#### Supported conversions

The table below lists the types that Robot Framework 3.1 and newer convert
arguments to. These characteristics apply to all conversions:

- Type can be explicitly specified using [function annotations](http://docs.python.org/library/ctypes.html) or
  the [@keyword decorator](https://docs.python.org/3/reference/simple_stmts.html#import).
- If not explicitly specified, type can be got implicitly from [argument
  default values](https://docs.python.org/3/reference/datamodel.html#object.__getattr__).
- Conversion is done regardless of the type of the given argument. If the
  argument type is incompatible with the expected type, conversion fails.
- Conversion failures cause an error if the type has been specified explicitly.
  If the type is got based on a default value, the given argument is used as-is.

!!! note
    If an argument has both a type hint and a default value, conversion is
    first attempted based on the type hint and then, if that fails, based on
    the default value type. This behavior is likely to change in the future
    so that conversion based on the default value is done *only* if the argument
    does not have a type hint. That will change conversion behavior in cases
    like `arg: list = None` where `None` conversion will not be attempted
    anymore. Library creators are strongly recommended to specify the default
    value type explicitly like `arg: list | None = None` already now.

The type to use can be specified either using concrete types (e.g. [list](https://docs.python.org/library/stdtypes.html#list)),
by using abstract base classes (ABC) (e.g. [Sequence](https://docs.python.org/library/collections.abc.html#collections.abc.Sequence)), or by using sub
classes of these types (e.g. [MutableSequence](https://docs.python.org/library/collections.abc.html#collections.abc.MutableSequence)). Also types in in the [typing](https://docs.python.org/library/typing.html)
module that map to the supported concrete types or ABCs (e.g. `List`) are
supported. In all these cases the argument is converted to the concrete type.

In addition to using the actual types (e.g. `int`), it is possible to specify
the type using type names as a string (e.g. `'int'`) and some types also have
aliases (e.g. `'integer'`). Matching types to names and aliases is
case-insensitive.

The Accepts column specifies which given argument types are converted.
If the given argument already has the expected type, no conversion is done.
Other types cause conversion failures.

| Type | ABC | Aliases | Accepts | Explanation | Examples |
| --- | --- | --- | --- | --- | --- |
| [bool](https://docs.python.org/library/functions.html#bool) |  | boolean | [str](https://docs.python.org/library/functions.html#func-str), [int](https://docs.python.org/library/functions.html#int), [float](https://docs.python.org/library/functions.html#float), [None](https://docs.python.org/library/constants.html#None) | Strings `TRUE`, `YES`, `ON` and `1` are converted to `True`, the empty string as well as `FALSE`, `NO`, `OFF` and `0` are converted to `False`, and the string `NONE` is converted to `None`. Other strings and other accepted values are passed as-is, allowing keywords to handle them specially if needed. All string comparisons are case-insensitive.  True and false strings can be [localized](../creating-test-data/test-data-syntax.md#localized). See the [Translations](../appendices/translations.md#translations) appendix for supported translations. | `TRUE` (converted to `True`) `off` (converted to `False`) `example` (used as-is) |
| [int](https://docs.python.org/library/functions.html#int) | [Integral](https://docs.python.org/library/numbers.html#numbers.Integral) | integer, long | [str](https://docs.python.org/library/functions.html#func-str), [float](https://docs.python.org/library/functions.html#float) | Conversion is done using the [int](https://docs.python.org/library/functions.html#int) built-in function. Floats are accepted only if they can be represented as integers exactly. For example, `1.0` is accepted and `1.1` is not. If converting a string to an integer fails and the type is got implicitly based on a default value, conversion to float is attempted as well.  Starting from Robot Framework 4.1, it is possible to use hexadecimal, octal and binary numbers by prefixing values with `0x`, `0o` and `0b`, respectively.  Starting from Robot Framework 4.1, spaces and underscores can be used as visual separators for digit grouping purposes.  Starting from Robot Framework 7.0, strings representing floats are accepted as long as their decimal part is zero. This includes using the scientific notation like `1e100`. | `42` `-1` `10 000 000` `1e100` `0xFF` `0o777` `0b1010` `0xBAD_C0FFEE` `${1}` `${1.0}` |
| [float](https://docs.python.org/library/functions.html#float) | [Real](https://docs.python.org/library/numbers.html#numbers.Real) | double | [str](https://docs.python.org/library/functions.html#func-str), [Real](https://docs.python.org/library/numbers.html#numbers.Real) | Conversion is done using the [float](https://docs.python.org/library/functions.html#float) built-in.  Starting from Robot Framework 4.1, spaces and underscores can be used as visual separators for digit grouping purposes. | `3.14` `2.9979e8` `10 000.000 01` `10_000.000_01` |
| [Decimal](https://docs.python.org/library/decimal.html#decimal.Decimal) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [int](https://docs.python.org/library/functions.html#int), [float](https://docs.python.org/library/functions.html#float) | Conversion is done using the [Decimal](https://docs.python.org/library/decimal.html#decimal.Decimal) class. [Decimal](https://docs.python.org/library/decimal.html#decimal.Decimal) is recommended over [float](https://docs.python.org/library/functions.html#float) when decimal numbers need to be represented exactly.  Starting from Robot Framework 4.1, spaces and underscores can be used as visual separators for digit grouping purposes. | `3.14` `10 000.000 01` `10_000.000_01` |
| [str](https://docs.python.org/library/functions.html#func-str) |  | string, unicode | Anything | All arguments are converted to Unicode strings.  Most values are converted simply by using `str(value)`. An exception is that bytes are mapped directly to Unicode code points with same ordinals. This means that, for example, `b"hyv\xe4"` becomes `"hyvä"`. Another exception is that [Secret](https://robot-framework.readthedocs.io/en/master/autodoc/robot.utils.html#robot.utils.secret.Secret) objects are explicitly rejected.  New in Robot Framework 4.0. Converting bytes specially and rejecting `Secret` objects are new in Robot Framework 7.4. |  |
| [bytes](https://docs.python.org/library/functions.html#func-bytes) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [bytearray](https://docs.python.org/library/functions.html#func-bytearray) | Strings are converted to bytes so that each Unicode code point below 256 is directly mapped to a matching byte. Higher code points are not allowed.  Integers and sequences of integers are converted to matching bytes directly. They must be in range 0-255.  Support for integers and sequences of integers is new in Robot Framework 7.4. | Strings:  `good` `hyvä` (converted to `hyv\xe4`) `\x00` (converted to the null byte)  Integers and sequences of integers:  `0` (converted to the null byte) `[82, 70, 33]` (converted to `RF!`) |
| [bytearray](https://docs.python.org/library/functions.html#func-bytearray) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [bytes](https://docs.python.org/library/functions.html#func-bytes) | Same conversion as with [bytes](https://docs.python.org/library/functions.html#func-bytes), but the result is a [bytearray](https://docs.python.org/library/functions.html#func-bytearray). |  |
| [datetime](#specifying-argument-types-using-keyword-decorator)_ |  |  | [str](https://docs.python.org/library/functions.html#func-str), [int](https://docs.python.org/library/functions.html#int), [float](https://docs.python.org/library/functions.html#float) | String timestamps are expected to be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) like format `YYYY-MM-DD hh:mm:ss.mmmmmm`, where any non-digit character can be used as a separator or separators can be omitted altogether. Additionally, only the date part is mandatory, all possibly missing time components are considered to be zeros.  Special values `NOW` and `TODAY` (case-insensitive) can be used to get the current local `datetime`. This is new in Robot Framework 7.3.  Integers and floats are considered to represent seconds since the [Unix epoch](http://en.wikipedia.org/wiki/Unix_time). | `2022-02-09T16:39:43.632269` `20220209 16:39` `2022-02-09` `now` (current local date and time) `TODAY` (same as above) `${1644417583.632269}` (Epoch time) |
| [date](https://docs.python.org/library/datetime.html#datetime.date) |  |  | [str](https://docs.python.org/library/functions.html#func-str) | Same timestamp conversion as with [datetime](#dt-mod)_, but all time components are expected to be omitted or to be zeros.  Special values `NOW` and `TODAY` (case-insensitive) can be used to get the current local `date`. This is new in Robot Framework 7.3. | `2018-09-12` `20180912` `today` (current local date) `NOW` (same as above) |
| [timedelta](https://docs.python.org/library/datetime.html#datetime.timedelta) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [int](https://docs.python.org/library/functions.html#int), [float](https://docs.python.org/library/functions.html#float) | Strings are expected to represent a time interval in one of the time formats Robot Framework supports: [time as number](../appendices/time-format.md#time-as-number), [time as time string](../appendices/time-format.md#time-as-time-string) or [time as "timer" string](../appendices/time-format.md#time-as-timer-string). Integers and floats are considered to be seconds. | `42` (42 seconds) `1 minute 2 seconds` `01:02` (same as above) |
| [Path](#implicit-argument-types-based-on-default-values)_ | [PathLike](https://docs.python.org/library/os.html#os.PathLike) |  | [str](https://docs.python.org/library/functions.html#func-str) | Strings are converted to [pathlib.Path](#pathlib)_ objects. On Windows `/` is converted to `\\` automatically.     | | `rel  New in Robot Framework 6.0. | `/tmp/absolute/path` `name.txt` |
| [Enum](https://docs.python.org/library/enum.html#enum.Enum) |  |  | [str](https://docs.python.org/library/functions.html#func-str) | The specified type must be an enumeration (a subclass of [Enum](https://docs.python.org/library/enum.html#enum.Enum) or [Flag](https://docs.python.org/library/enum.html#enum.Flag)) and given arguments must match its member names.  Matching member names is case, space, underscore and hyphen insensitive, but exact matches have precedence over normalized matches. Ignoring hyphens is new in Robot Framework 7.0.  Enumeration documentation and members are shown in documentation generated by [Libdoc](../supporting-tools/libdoc.md#libdoc) automatically. | .. sourcecode:: python  class Direction(Enum): """Move direction.""" NORTH = auto() NORTH_WEST = auto()  def kw(arg: Direction): ...  `NORTH` (Direction.NORTH) `north west` (Direction.NORTH_WEST) |
| [IntEnum](https://docs.python.org/library/enum.html#enum.IntEnum) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [int](https://docs.python.org/library/functions.html#int) | The specified type must be an integer based enumeration (a subclass of [IntEnum](https://docs.python.org/library/enum.html#enum.IntEnum) or [IntFlag](https://docs.python.org/library/enum.html#enum.IntFlag)) and given arguments must match its member names or values.  Matching member names works the same way as with `Enum`. Values can be given as integers and as strings that can be converted to integers.  Enumeration documentation and members are shown in documentation generated by [Libdoc](../supporting-tools/libdoc.md#libdoc) automatically.  New in Robot Framework 4.1. | .. sourcecode:: python  class PowerState(IntEnum): """Turn system ON or OFF.""" OFF = 0 ON = 1  def kw(arg: PowerState): ...  `OFF` (PowerState.OFF) `1` (PowerState.ON) |
| [Literal](https://docs.python.org/library/typing.html#typing.Literal) |  |  | Depends on usage | Only specified values are accepted. Values can be strings, integers, bytes, Booleans, enums and `None`, and used arguments are converted using the value type specific conversion logic.  Strings are case, space, underscore and hyphen insensitive, but exact matches have precedence over normalized matches.  `Literal` provides similar functionality as `Enum`, but does not support custom documentation.  New in Robot Framework 7.0. | .. sourcecode:: python  def kw(arg: Literal['ON', 'OFF']): ...  `OFF` `on` |
| [None](https://docs.python.org/library/constants.html#None) |  |  | [str](https://docs.python.org/library/functions.html#func-str) | String `NONE` (case-insensitive) and the empty string are converted to the Python `None` object. Other values cause an error.  Converting the empty string is new in Robot Framework 7.4. | `None` |
| [Any](https://docs.python.org/library/typing.html#typing.Any) |  |  | Anything | Any value is accepted. No conversion is done.  New in Robot Framework 6.1. |  |
| [object](https://docs.python.org/3/library/functions.html#object) |  |  | Anything | Any value is accepted. No conversion is done.  New in Robot Framework 7.4. |  |
| [list](https://docs.python.org/library/stdtypes.html#list) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [Sequence](https://docs.python.org/library/collections.abc.html#collections.abc.Sequence) | Converts strings and sequences to `list`.  Strings must be Python list or tuple literals. They are converted using the [ast.literal_eval](https://docs.python.org/library/ast.html#ast.literal_eval) function and possible tuples converted further to lists. They can contain any values `ast.literal_eval` supports, including lists and other collections.  If the argument is a list, it is used without conversion. Tuples and other sequences are converted to lists.  Support for tuple literals is new in Robot Framework 7.4. | `['one', 'two']` `[('one', 1), ('two', 2)]` |
| [tuple](https://docs.python.org/library/stdtypes.html#tuple) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [Sequence](https://docs.python.org/library/collections.abc.html#collections.abc.Sequence) | Same as `list`, but the result is [tuple](https://docs.python.org/library/stdtypes.html#tuple).  Prior to Robot Framework 7.4, only tuple literals were supported. | `('one', 'two')` |
| [Sequence](https://docs.python.org/library/collections.abc.html#collections.abc.Sequence) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [Sequence](https://docs.python.org/library/collections.abc.html#collections.abc.Sequence) | Same as `list`, but any sequence is accepted without conversion.  If the used type is [MutableSequence](https://docs.python.org/library/collections.abc.html#collections.abc.MutableSequence), immutable values are converted to lists. | `[1, 2, 3]` (result is `list`) `(1, 2, 3)` (result is `tuple`) |
| [set](https://docs.python.org/library/stdtypes.html#set) | [Set](https://peps.python.org/pep-0604/)_ |  | [str](https://docs.python.org/library/functions.html#func-str), [Collection](https://docs.python.org/library/collections.abc.html#collections.abc.Collection) | Same as `list`, but also collection objects and set literals are supported and the result is [set](https://docs.python.org/library/stdtypes.html#set).  Prior to Robot Framework 7.4, only set literals were supported. | `{1, 2, 3, 42}` `set()` (an empty set) |
| [frozenset](https://docs.python.org/library/stdtypes.html#frozenset) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [Collection](https://docs.python.org/library/collections.abc.html#collections.abc.Collection) | Same as `set`, but the result is a [frozenset](https://docs.python.org/library/stdtypes.html#frozenset). | `{1, 2, 3, 42}` `frozenset()` (an empty set) |
| [dict](https://docs.python.org/library/stdtypes.html#dict) |  | dictionary | [str](https://docs.python.org/library/functions.html#func-str), [Mapping](https://docs.python.org/library/collections.abc.html#collections.abc.Mapping) | Converts strings and mappings to `dict`.  Strings must be Python dictionary literals. They are converted to `dict` using the [ast.literal_eval](https://docs.python.org/library/ast.html#ast.literal_eval) function. They can contain any values `ast.literal_eval` supports, including dictionaries and other collections. | `{'a': 1, 'b': 2}` `{'key': 1, 'nested': {'key': 2}}` |
| [Mapping](https://docs.python.org/library/collections.abc.html#collections.abc.Mapping) |  | map | [str](https://docs.python.org/library/functions.html#func-str), [Mapping](https://docs.python.org/library/collections.abc.html#collections.abc.Mapping) | Same as `dict`, but the original mapping type is preserved.  If type is [MutableMapping](https://docs.python.org/library/collections.abc.html#collections.abc.MutableMapping), immutable values are converted to `dict`. |  |
| [TypedDict](https://docs.python.org/library/typing.html#typing.TypedDict) |  |  | [str](https://docs.python.org/library/functions.html#func-str), [Mapping](https://docs.python.org/library/collections.abc.html#collections.abc.Mapping) | Same as `dict`, but dictionary items are also converted to the specified types and items not included in the type spec are not allowed.  New in Robot Framework 6.0. Normal `dict` conversion was used earlier. | .. sourcecode:: python  class Config(TypedDict): width: int enabled: bool  `{'width': 1600, 'enabled': True}` |
| [Secret](https://robot-framework.readthedocs.io/en/master/autodoc/robot.utils.html#robot.utils.secret.Secret) |  |  | [Secret](https://robot-framework.readthedocs.io/en/master/autodoc/robot.utils.html#robot.utils.secret.Secret) | Using the [Secret type](#secret-type) as a type hint ensures that only [secret variables](../creating-test-data/variables.md#secret-variables) are accepted as arguments.  New in Robot Framework 7.4. | .. sourcecode:: python  from robot.api.types import Secret   def login(token: Secret): do_something(token.value) |

!!! note
    Starting from Robot Framework 5.0, types that have a converted are
    automatically shown in [Libdoc](../supporting-tools/libdoc.md#libdoc) outputs.

!!! note
    Prior to Robot Framework 4.0, most types supported converting string `NONE` (case-insensitively) to Python
    `None`. That support has been removed and `None` conversion is only done if an argument has `None` as an
    explicit type or as a default value.

#### Specifying multiple possible types

It is possible to specify that an argument has multiple possible types. In this
situation argument conversion is attempted based on each type, from left to right,
and the value of the first succeeding conversion is used. If none of these conversions
succeeds, the whole conversion fails.

##### Union syntax

When using function annotations, the natural syntax to specify that an argument
has multiple possible types is using a [Union](https://docs.python.org/3/library/typing.html#typing.Union):

```python
from typing import Union

def example(length: Union[int, float], padding: Union[int, str, None] = None):
    ...
```
When using Python 3.10 or newer, it is possible to use the [native union syntax](http://docs.python.org/c-api/index.html)
like `int | float` instead:

```python
def example(length: int | float, padding: int | str | None = None):
    ...
```
Robot Framework 7.0 enhanced the support for the union syntax so that also
"stringly typed" unions like `"int | float"` work. This syntax works also
with older Python versions:

```python
def example(length: "int | float", padding: "int | str | None" = None):
    ...
```

##### Using tuples

An alternative is specifying types as a tuple. It is not recommended with annotations,
because that syntax is not supported by other tools, but it works well with
the `@keyword` decorator:

```python
from robot.api.deco import keyword

@keyword(types={'length': (int, float), 'padding': (int, str, None)})
def example(length, padding=None):
    ...
```
With the above examples the `length` argument would first be converted to an
integer and if that fails then to a float. The `padding` would be first
converted to an integer, then to a string, and finally to `None`.

##### When argument matches one of the types

If the given argument has one of the accepted types, then no conversion is done
and the argument is used as-is. For example, if the `length` argument typed
like `length: int | float` is used with a floating point number `1.5`, it is not
converted to an integer. Notice that using non-string values like floats as an
argument requires using variables as these examples giving different values to
the `length` argument demonstrate:

```robotframework
*** Test Cases ***
Conversion
    Example    10        # Argument is a string. Converted to an integer.
    Example    1.5       # Argument is a string. Converted to a float.
    Example    ${10}     # Argument is an integer. Accepted as-is.
    Example    ${1.5}    # Argument is a float. Accepted as-is.
```
If one of the accepted types is string like in `padding: int | str | None`,
then no conversion is done if the given argument is a string. As the following
examples giving different values to the `padding` argument demonstrate, also in
these cases passing other types is possible using variables:

```robotframework
*** Test Cases ***
Conversion
    Example    1    big        # Argument is a string. Accepted as-is.
    Example    1    10         # Argument is a string. Accepted as-is.
    Example    1    ${10}      # Argument is an integer. Accepted as-is.
    Example    1    ${None}    # Argument is `None`. Accepted as-is.
    Example    1    ${1.5}     # Argument is a float. Converted to an integer.
```
If the given argument does not have any of the accepted types, conversion is
attempted in the order types are specified.

!!! note
    The order of types changes the conversion result in cases where the used
    value does not match any of the types, but conversion to multiple types
    would succeed.

          For example, if typing is `float | int` and the used value is string `42`,
          the result will be float `42.0` instead of integer `42`. The reason is
          that a string does not match either of the types and `float` conversion
          is attempted first. If the order is changed to `int | float`, the result
          will be an integer.

          String `3.14` would be converted to a float regardless the order, because
          `int` conversion does not succeed. The order does not affect usages where
          the value is already an integer or a float either, because there is no
          need for conversion in such cases.

##### Handling `Any` and `object`

If `Any` or `object` is used as a type hint on its own like `arg: Any` or `arg: object`,
any value is accepted without conversion. How they work when used in an union differs,
though.

If `Any` is used in a union like `arg: int | Any`, any value is accepted without
conversion. This allows using `Any` as an escape hatch that disables argument conversion
altogether.

On the other hand, if `object` is used in an union like `arg: int | object`,
conversion is attempted to types before `object`. This allows attempting conversion
to certain type or types, but getting the original value if conversions fail.

!!! note
    Although this subtle difference in behavior may be useful, it is also
    somewhat confusing and the plan is to change it in Robot Framework 8.0
    so that `Any` behaves like `object`. See the issue [#5571](http://docs.python.org/c-api/index.html) for more
    information and comment the issue if you do not think the planned change
    is a good idea.

##### Handling unrecognized types

If types that are not recognized by Robot Framework are used in an union, they are
handled like this:

- If a used value matches any of the types, including unrecognized types, the value
  is used as-is without conversion.
- Otherwise conversion is attempted to recognized types from left to right.
- If any conversion succeeds, the converted value is returned.
- If no conversion succeeds, the original value is returned.

For example, with the following keyword string `"7"` would be converted to an integer,
but string `"something"` would be used as-is:

```python
def example(argument: int | Unrecognized):
    ...
```
Starting from Robot Framework 6.1, the above logic works also if an unrecognized
type is listed before a recognized type like `Unrecognized | int`.
Also in this case `int` conversion is attempted, and the argument id passed as-is
if it fails. With earlier Robot Framework versions, `int` conversion would not be
attempted at all.

#### Parameterized types

With generics also the parameterized syntax like `list[int]` or `dict[str, int]`
works. When this syntax is used, the given value is first converted to the base
type and then individual items are converted to the nested types. Conversion
with different generic types works according to these rules:

- With lists there can be only one type like `list[float]`. All list items are
  converted to that type.
- With tuples there can be any number of types like `tuple[int, int]` and
  `tuple[str, int, bool]`. Tuples used as arguments are expected to have
  exactly that amount of items and they are converted to matching types.
- To create a homogeneous tuple, it is possible to use exactly one type and
  ellipsis like `tuple[int, ...]`. In this case tuple can have any number
  of items, including zero, and they are all converted to the specified type.
- With dictionaries there must be exactly two types like `dict[str, int]`.
  Dictionary keys are converted using the first type and values using the second.
- With sets there can be exactly one type like `set[float]`. Conversion logic
  is the same as with lists.

Using the native `list[int]` syntax requires [Python 3.9](http://docs.python.org/c-api/index.html) or newer. If there
is a need to support also earlier Python versions, it is possible to either use
matching types from the [typing](https://docs.python.org/library/typing.html) module like `List[int]` or use the "stringly typed"
syntax like `'list[int]'`.

!!! note
    Support for converting nested types with generics is new in
    Robot Framework 6.0. Same syntax works also with earlier versions,
    but arguments are only converted to the base type and nested type
    information is ignored.

!!! note
    Support for "stringly typed" parameterized generics is new in
    Robot Framework 7.0.

#### Secret type

Robot Framework has a custom [robot.api.types.Secret](../creating-test-data/variables.md#secret-variables) type that
encapsulates values so that they are not shown in log files. If the `Secret`
type is used as an argument type, only `Secret` objects are accepted and trying
to use, for example, literal strings fails. The encapsulated value is available
in the `value` attribute so keywords can access it easily:

```python
from example import SUT
from robot.api.types import Secret

def login_to_sut(user: str, token: Secret):
    SUT.login(user, token.value)
```
The [Secret variables](../creating-test-data/variables.md#secret-variables) section explains how to create `Secret` objects
in the data, on the command line, and elsewhere. In the data that involves
using [variable type conversion](../creating-test-data/variables.md#variable-type-conversion) and, for example, [environment variables](../creating-test-data/variables.md#environment-variables):

```robotframework
*** Variables ***
${USER}             robot
${TOKEN: Secret}    %{ROBOT_TOKEN}

*** Test Cases ***
Example
    Login to SUT    ${USER}    ${TOKEN}
```
Keywords can also accept `Secret` objects in addition to strings by using
the union syntax like `str | Secret`:

```python
from example import SUT
from robot.api import logger
from robot.api.types import Secret

def input_password(password: str | Secret):
     logger.debug(f"Typing password: {password}")
     if isinstance(password, Secret):
         password = password.value
     SUT.input_password(password)
```
In this kind of cases it is important to not log or otherwise disclose actual
secret values. The string representation of `Secret` objects is always
`<secret>` and thus logging `f"Typing password: {password}"` in the above
example is safe, but logging it at the end of the example would not be.
The `repr()` of `Secret` objects is `Secret(value=<secret>)` so the real
value is not shown in that string representation either.

Using the `Secret` type in complex type hints works similarly as with other types.
The following example is similar to the example above, but uses a [TypedDict](https://docs.python.org/library/typing.html#typing.TypedDict)
with a `Secret` item:

```python
from typing import TypedDict

from robot.api.types import Secret

class Credential(TypedDict):
    user: str
    token: Secret

def login_to_sut(credentials: Credential):
    SUT.login(credentials["user"], credentials["token"].value)
```
```robotframework
*** Variables ***
${TOKEN: Secret}    %{ROBOT_TOKEN}
&{CREDENTIALS}      user=robot    token=${TOKEN}

*** Test Cases ***
Example
    Login to SUT    ${CREDENTIALS}
```
!!! warning
    Secret objects do not hide or encrypt their values. The real values
    are thus available for all code that can access these objects directly
    or indirectly via Robot Framework APIs.

!!! warning
    Actual secret values that keywords pass forward may be logged or
    otherwise disclosed by external modules or tools using them.

!!! note
    The [Secret](https://robot-framework.readthedocs.io/en/master/autodoc/robot.utils.html#robot.utils.secret.Secret) type is new in Robot Framework 7.4.

#### Custom argument converters

In addition to doing argument conversion automatically as explained in the
previous sections, Robot Framework supports custom argument conversion. This
functionality has two main use cases:

- Overriding the standard argument converters provided by the framework.

- Adding argument conversion for custom types and for other types not supported
  out-of-the-box.

Argument converters are functions or other callables that get arguments used
in data and convert them to desired format before arguments are passed to
keywords. Converters are registered for libraries by setting
`ROBOT_LIBRARY_CONVERTERS` attribute (case-sensitive) to a dictionary mapping
desired types to converts. When implementing a library as a module, this
attribute must be set on the module level, and with class based libraries
it must be a class attribute. With libraries implemented as classes, it is
also possible to use the `converters` argument with the [@library decorator](#library-decorator).
Both of these approaches are illustrated by examples in the following sections.

!!! note
    Custom argument converters are new in Robot Framework 5.0.

##### Overriding default converters

Let's assume we wanted to create a keyword that accepts [date](https://docs.python.org/library/datetime.html#datetime.date) objects for
users in Finland where the commonly used date format is `dd.mm.yyyy`.
The usage could look something like this:

```robotframework
*** Test Cases ***
Example
    Keyword    25.1.2022
```
[Automatic argument conversion](http://docs.python.org/c-api/index.html) supports dates, but it expects them
to be in `yyyy-mm-dd` format so it will not work. A solution is creating
a custom converter and registering it to handle [date](https://docs.python.org/library/datetime.html#datetime.date) conversion:

```python
from datetime import date

# Converter function.
def parse_fi_date(value):
    day, month, year = value.split('.')
    return date(int(year), int(month), int(day))

# Register converter function for the specified type.
ROBOT_LIBRARY_CONVERTERS = {date: parse_fi_date}

# Keyword using custom converter. Converter is resolved based on argument type.
def keyword(arg: date):
    print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')
```

##### Conversion errors

If we try using the above keyword with invalid argument like `invalid`, it
fails with this error:

```
ValueError: Argument 'arg' got value 'invalid' that cannot be converted to date: not enough values to unpack (expected 3, got 1)
```

This error is not too informative and does not tell anything about the expected
format. Robot Framework cannot provide more information automatically, but
the converter itself can be enhanced to validate the input. If the input is
invalid, the converter should raise a `ValueError` with an appropriate message.
In this particular case there would be several ways to validate the input, but
using [regular expressions](http://docs.python.org/c-api/index.html) makes it possible to validate both that the input
has dots (`.`) in correct places and that date parts contain correct amount
of digits:

```python
from datetime import date
import re

def parse_fi_date(value):
    # Validate input using regular expression and raise ValueError if not valid.
    match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})$', value)
    if not match:
        raise ValueError(f"Expected date in format 'dd.mm.yyyy', got '{value}'.")
    day, month, year = match.groups()
    return date(int(year), int(month), int(day))

ROBOT_LIBRARY_CONVERTERS = {date: parse_fi_date}

def keyword(arg: date):
    print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')
```
With the above converter code, using the keyword with argument `invalid` fails
with a lot more helpful error message:

```
ValueError: Argument 'arg' got value 'invalid' that cannot be converted to date: Expected date in format 'dd.mm.yyyy', got 'invalid'.
```

##### Restricting value types

By default Robot Framework tries to use converters with all given arguments
regardless their type. This means that if the earlier example keyword would
be used with a variable containing something else than a string, conversion
code would fail in the `re.match` call. For example, trying to use it with
argument `${42}` would fail like this:

```
ValueError: Argument 'arg' got value '42' (integer) that cannot be converted to date: TypeError: expected string or bytes-like object
```

This error situation could naturally handled in the converter code by checking
the value type, but if the converter only accepts certain types, it is typically
easier to just restrict the value to that type. Doing it requires only adding
appropriate type hint to the converter:

```python
def parse_fi_date(value: str):
    ...
```
Notice that this type hint *is not* used for converting the value before calling
the converter, it is used for strictly restricting which types can be used.
With the above addition calling the keyword with `${42}` would fail like this:

```
ValueError: Argument 'arg' got value '42' (integer) that cannot be converted to date.
```

If the converter can accept multiple types, it is possible to specify types
as a [Union](https://docs.python.org/3/library/typing.html#typing.Union). For example, if we wanted to enhance our keyword to accept also
integers so that they would be considered seconds since the [Unix epoch](http://en.wikipedia.org/wiki/Unix_time),
we could change the converter like this:

```python
from datetime import date
import re
from typing import Union

# Accept both strings and integers.
def parse_fi_date(value: Union[str, int]):
    # Integers are converted separately.
    if isinstance(value, int):
        return date.fromtimestamp(value)
    match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})$', value)
    if not match:
        raise ValueError(f"Expected date in format 'dd.mm.yyyy', got '{value}'.")
    day, month, year = match.groups()
    return date(int(year), int(month), int(day))

ROBOT_LIBRARY_CONVERTERS = {date: parse_fi_date}

def keyword(arg: date):
    print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')
```
##### Converting custom types

A problem with the earlier example is that [date](https://docs.python.org/library/datetime.html#datetime.date) objects could only be given
in `dd.mm.yyyy` format. It would not work if there was a need to
support dates in different formats like in this example:

```robotframework
*** Test Cases ***
Example
    Finnish     25.1.2022
    US          1/25/2022
    ISO 8601    2022-01-22
```
A solution to this problem is creating custom types instead of overriding
the default [date](https://docs.python.org/library/datetime.html#datetime.date) conversion:

```python
from datetime import date
import re
from typing import Union

from robot.api.deco import keyword, library

# Custom type. Extends an existing type but that is not required.
class FiDate(date):

    # Converter function implemented as a classmethod. It could be a normal
    # function as well, but this way all code is in the same class.
    @classmethod
    def from_string(cls, value: str):
        match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})$', value)
        if not match:
            raise ValueError(f"Expected date in format 'dd.mm.yyyy', got '{value}'.")
        day, month, year = match.groups()
        return cls(int(year), int(month), int(day))

# Another custom type.
class UsDate(date):

    @classmethod
    def from_string(cls, value: str):
        match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})$', value)
        if not match:
            raise ValueError(f"Expected date in format 'mm/dd/yyyy', got '{value}'.")
        month, day, year = match.groups()
        return cls(int(year), int(month), int(day))

# Register converters using '@library' decorator.
@library(converters={FiDate: FiDate.from_string, UsDate: UsDate.from_string})
class Library:

    # Uses custom converter supporting 'dd.mm.yyyy' format.
    @keyword
    def finnish(self, arg: FiDate):
        print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')

    # Uses custom converter supporting 'mm/dd/yyyy' format.
    @keyword
    def us(self, arg: UsDate):
        print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')

    # Uses IS0-8601 compatible default conversion.
    @keyword
    def iso_8601(self, arg: date):
        print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')

    # Accepts date in different formats.
    @keyword
    def any(self, arg: Union[FiDate, UsDate, date]):
        print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')
```
##### Strict type validation

Converters are not used at all if the argument is of the specified type to
begin with. It is thus easy to enable strict type validation with a custom
converter that does not accept any value. For example, the *Example*
keyword accepts only `StrictType` instances:

```python
class StrictType:
    pass

def strict_converter(arg):
    raise TypeError(f'Only StrictType instances accepted, got {type(arg).__name__}.')

ROBOT_LIBRARY_CONVERTERS = {StrictType: strict_converter}

def example(argument: StrictType):
    assert isinstance(argument, StrictType)
```
As a convenience, Robot Framework allows setting converter to `None` to get
the same effect. For example, this code behaves exactly the same way as
the code above:

```python
class StrictType:
    pass

ROBOT_LIBRARY_CONVERTERS = {StrictType: None}

def example(argument: StrictType):
    assert isinstance(argument, StrictType)
```
!!! note
    Using `None` as a strict converter is new in Robot Framework 6.0.
    An explicit converter function needs to be used with earlier versions.

##### Accessing the test library from converter

Starting from Robot Framework 6.1, it is possible to access the library
instance from a converter function. This allows defining dynamic type conversions
that depend on the library state. For example, if the library can be configured to
test particular locale, you might use the library state to determine how a date
should be parsed like this:

```python
from datetime import date
import re

def parse_date(value, library):
    # Validate input using regular expression and raise ValueError if not valid.
    # Use locale based from library state to determine parsing format.
    if library.locale == 'en_US':
        match = re.match(r'(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})$', value)
        format = 'mm/dd/yyyy'
    else:
        match = re.match(r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})$', value)
        format = 'dd.mm.yyyy'
    if not match:
        raise ValueError(f"Expected date in format '{format}', got '{value}'.")
    return date(int(match.group('year')), int(match.group('month')), int(match.group('day')))

ROBOT_LIBRARY_CONVERTERS = {date: parse_date}

def keyword(arg: date):
    print(f'year: {arg.year}, month: {arg.month}, day: {arg.day}')
```
The `library` argument to converter function is optional, i.e. if the converter function
only accepts one argument, the `library` argument is omitted. Similar result can be achieved
by making the converter function accept only variadic arguments, e.g. `def parse_date(*varargs)`.

##### Converter documentation

Information about converters is added to outputs produced by [Libdoc](../supporting-tools/libdoc.md#libdoc)
automatically. This information includes the name of the type, accepted values
(if specified using type hints) and documentation. Type information is
automatically linked to all keywords using these types.

Used documentation is got from the converter function by default. If it does
not have any documentation, documentation is got from the type. Both of these
approaches to add documentation to converters in the previous example thus
produce the same result:

```python
class FiDate(date):

    @classmethod
    def from_string(cls, value: str):
        """Date in `dd.mm.yyyy` format."""
        ...

class UsDate(date):
    """Date in `mm/dd/yyyy` format."""

    @classmethod
    def from_string(cls, value: str):
        ...
```
Adding documentation is in general recommended to provide users more
information about conversion. It is especially important to document
converter functions registered for existing types, because their own
documentation is likely not very useful in this context.

### `@keyword` decorator

Although Robot Framework gets lot of information about keywords automatically,
such as their names and arguments, there are sometimes needs to configure this
information further. This is typically easiest done by using the
`robot.api.deco.keyword` decorator. It has several useful usages that are
explained thoroughly elsewhere and only listened here as a reference:

- Exposing methods and functions as keywords when the [automatic keyword
  discovery](http://docs.python.org/c-api/index.html) has been disabled by using the [@library decorator](#library-decorator) or
  otherwise.

- Setting a [custom name](http://docs.python.org/library/ctypes.html) to a keyword. This is especially useful when using
  the [embedded argument syntax](https://docs.python.org/3/reference/simple_stmts.html#import).

- Setting [keyword tags](#keyword-tags).

- Setting [type information](https://docs.python.org/3/reference/datamodel.html#object.__getattr__) to enable automatic argument type conversion.
  Supports also disabling the argument conversion altogether.

- [Marking methods to expose as keywords](dynamic-library-api.md#marking-methods-to-expose-as-keywords) when using the [dynamic library API](dynamic-library-api.md#dynamic-library-api).

### `@not_keyword` decorator

The `robot.api.deco.not_keyword` decorator can be used for
[disabling functions or methods becoming keywords](https://docs.python.org/tutorial/controlflow.html#keyword-arguments).

### Using custom decorators

When implementing keywords, it is sometimes useful to modify them with
[Python decorators](https://www.python.org/dev/peps/pep-3102). However, decorators often modify function signatures
and can thus confuse Robot Framework's introspection when determining which
arguments keywords accept. This is especially problematic when creating
library documentation with [Libdoc](../supporting-tools/libdoc.md#libdoc) and when using external tools like [RIDE](https://github.com/robotframework/RIDE).
The easiest way to avoid this problem is decorating the
decorator itself using [functools.wraps](https://www.python.org/dev/peps/pep-0570/). Other solutions include using
external modules like [decorator](https://robot-framework.readthedocs.io/en/stable/autodoc/robot.running.arguments.html#robot.running.arguments.typeinfo.TypeInfo) and [wrapt](https://peps.python.org/pep-0604/) that allow creating fully
signature-preserving decorators.

!!! note
    Support for "unwrapping" decorators decorated with `functools.wraps`
    is a new feature in Robot Framework 3.2.

### Embedding arguments into keyword names

Library keywords can also accept *embedded arguments* the same way as
[user keywords](https://docs.python.org/3/reference/datamodel.html#object.__getattr__). This section mainly covers the Python syntax to use to
create such keywords, the embedded arguments syntax itself is covered in
detail as part of [user keyword documentation](https://github.com/robotframework/robotframework/issues/5571).

Library keywords with embedded arguments need to have a [custom name](https://peps.python.org/pep-0585/) that
is typically set using the [@keyword decorator](#keyword-decorator). Values matching embedded
arguments are passed to the function or method implementing the keyword as
positional arguments. If the function or method accepts more arguments, they
can be passed to the keyword as normal positional or named arguments.
Argument names do not need to match the embedded argument names, but that
is generally a good convention.

Keywords accepting embedded arguments:

```python
from robot.api.deco import keyword

@keyword('Select ${animal} from list')
def select_animal_from_list(animal):
    ...

@keyword('Number of ${animals} should be')
def number_of_animals_should_be(animals, count):
    ...
```
Tests using the above keywords:

```robotframework
*** Test Cases ***
Embedded arguments
    Select cat from list
    Select dog from list

Embedded and normal arguments
    Number of cats should be    2
    Number of dogs should be    count=3
```
If type information is specified, automatic [argument conversion](#argument-conversion) works also
with embedded arguments:

```python
@keyword('Add ${quantity} copies of ${item} to cart')
def add_copies_to_cart(quantity: int, item: str):
    ...
```
!!! note
    Embedding type information to keyword names like
    `Add ${quantity: int} copies of ${item: str} to cart` similarly
    as with [user keywords](http://docs.python.org/c-api/index.html) *is not supported* with library keywords.

!!! note
    Support for mixing embedded arguments and normal arguments is new
    in Robot Framework 7.0.

### Asynchronous keywords

Starting from Robot Framework 6.1, it is possible to run native asynchronous
functions (created by `async def`) just like normal functions:

```python
import asyncio

from robot.api.deco import keyword

@keyword
async def this_keyword_waits():
    await asyncio.sleep(5)
```
You can get the reference of the loop using `asyncio.get_running_loop()` or
`asyncio.get_event_loop()`. Be careful when modifying how the loop runs, it is
a global resource. For example, never call `loop.close()` because it will make it
impossible to run any further coroutines. If you have any function or resource that
requires the event loop, even though `await` is not used explicitly, you have to define
your function as async to have the event loop available.

More examples of functionality:

```python
import asyncio
from robot.api.deco import keyword

async def task_async():
    await asyncio.sleep(5)

@keyword
async def examples():
    tasks = [task_async() for _ in range(10)]
    results = await asyncio.gather(*tasks)

    background_task = asyncio.create_task(task_async())
    await background_task

    # If running with Python 3.10 or higher
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(task_async())
        task2 = tg.create_task(task_async())
```
!!! note
    Robot Framework waits for the function to complete. If you want to have a task that runs
    for a long time, use, for example, `asyncio.create_task()`. It is your responsibility to
    manage the task and save a reference to avoid it being garbage collected. If the event loop
    closes and a task is still pending, a message will be printed to the console.

!!! note
    If execution of keyword cannot continue for some reason, for example a signal stop,
    Robot Framework will cancel the async task and any of its children. Other async tasks will
    continue running normally.

## Communicating with Robot Framework

After a method implementing a keyword is called, it can use any
mechanism to communicate with the system under test. It can then also
send messages to Robot Framework's log file, return information that
can be saved to variables and, most importantly, report if the
keyword passed or not.

### Reporting keyword status

Reporting keyword status is done simply using exceptions. If an executed
method raises an exception, the keyword status is `FAIL`, and if it
returns normally, the status is `PASS`.

Normal execution failures and errors can be reported using the standard exceptions
such as `AssertionError`, `ValueError` and `RuntimeError`. There are, however, some
special cases explained in the subsequent sections where special exceptions are needed.

#### Error messages

The error message shown in logs, reports and the console is created
from the exception type and its message. With generic exceptions (for
example, `AssertionError`, `Exception`, and
`RuntimeError`), only the exception message is used, and with
others, the message is created in the format `ExceptionType:
Actual message`.

It is possible to avoid adding the
exception type as a prefix to failure message also with non generic exceptions.
This is done by adding a special `ROBOT_SUPPRESS_NAME` attribute with
value `True` to your exception.

Python:

```python
class MyError(RuntimeError):
    ROBOT_SUPPRESS_NAME = True
```
In all cases, it is important for the users that the exception message is as
informative as possible.

#### HTML in error messages

It is also possible to have HTML formatted
error messages by starting the message with text `*HTML*`:

```python
raise AssertionError("*HTML* <a href='robotframework.org'>Robot Framework</a> rulez!!")
```
This method can be used both when raising an exception in a library, like
in the example above, and [when users provide an error message in the test data](http://docs.python.org/c-api/index.html).

#### Cutting long messages automatically

If the error message is longer than 40 lines, it will be automatically
cut from the middle to prevent reports from getting too long and
difficult to read. The full error message is always shown in the log
message of the failed keyword.

#### Tracebacks

The traceback of the exception is also logged using `DEBUG` [log level](#exceptions-provided-by-robot-framework).
These messages are not visible in log files by default because they are very
rarely interesting for normal users. When developing libraries, it is often a
good idea to run tests using `--loglevel DEBUG`.

### Exceptions provided by Robot Framework

Robot Framework provides some exceptions that libraries can use for reporting
failures and other events. These exceptions are exposed via the [robot.api](http://docs.python.org/library/ctypes.html)
package and contain the following:

`Failure`
: Report failed validation. There is no practical difference in using this exception
    compared to using the standard `AssertionError`. The main benefit of using this
    exception is that its name is consistent with other provided exceptions.

`Error`
: Report error in execution. Failures related to the system not behaving as expected
    should typically be reported using the `Failure` exception or the standard
    `AssertionError`. This exception can be used, for example, if the keyword is used
    incorrectly. There is no practical difference, other than consistent naming with
    other provided exceptions, compared to using this exception and the standard
    `RuntimeError`.

`ContinuableFailure`
: Report failed validation but allow continuing execution.
    See the [Continuable failures](#continuable-failures) section below for more information.

`SkipExecution`
: Mark the executed test or task [skipped](../executing-tests/test-execution.md#skipped).
    See the [Skipping tests](#skipping-tests) section below for more information.

`FatalError`
: Report error that stops the whole execution.
    See the [Stopping test execution](#stopping-test-execution) section below for more information.

!!! note
    All these exceptions are new in Robot Framework 4.0. Other features than
    skipping tests, which is also new in Robot Framework 4.0, are available
    by other means in earlier versions.

### Continuable failures

It is possible to [continue test execution even when there are failures](https://docs.python.org/3/reference/simple_stmts.html#import).
The easiest way to do that is using the [provided](https://docs.python.org/3/reference/datamodel.html#object.__getattr__) `robot.api.ContinuableFailure`
exception:

```python
from robot.api import ContinuableFailure

def example_keyword():
    if something_is_wrong():
        raise ContinuableFailure('Something is wrong but execution can continue.')
    ...
```
An alternative is creating a custom exception that has a special
`ROBOT_CONTINUE_ON_FAILURE` attribute set to a `True` value.
This is demonstrated by the example below.

```python
class MyContinuableError(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True
```

### Skipping tests

It is possible to [skip](../executing-tests/test-execution.md#skip) tests with a library keyword. The easiest way to
do that is using the [provided](http://docs.python.org/c-api/index.html) `robot.api.SkipExecution` exception:

```python
from robot.api import SkipExecution

def example_keyword():
    if test_should_be_skipped():
        raise SkipExecution('Cannot proceed, skipping test.')
    ...
```
An alternative is creating a custom exception that has a special
`ROBOT_SKIP_EXECUTION` attribute set to a `True` value.
This is demonstrated by the example below.

```python
class MySkippingError(RuntimeError):
    ROBOT_SKIP_EXECUTION = True
```

### Stopping test execution

It is possible to fail a test case so that [the whole test execution is
stopped](http://docs.python.org/c-api/index.html). The easiest way to accomplish this is using the [provided](http://docs.python.org/library/ctypes.html)
`robot.api.FatalError` exception:

```python
from robot.api import FatalError

def example_keyword():
    if system_is_not_running():
        raise FatalError('System is not running!')
    ...
```
In addition to using the `robot.api.FatalError` exception, it is possible create
a custom exception that has a special `ROBOT_EXIT_ON_FAILURE` attribute set to
a `True` value. This is illustrated by the example below.

```python
class MyFatalError(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = True
```

### Logging information

Exception messages are not the only way to give information to the
users. In addition to them, methods can also send messages to [log
files](../executing-tests/result-files.md#log) simply by writing to the standard output stream (stdout) or to
the standard error stream (stderr), and they can even use different
[log levels](../executing-tests/result-files.md#log-levels). Another, and often better, logging possibility is using
the [programmatic logging APIs](#programmatic-logging-apis).

By default, everything written by a method into the standard output is
written to the log file as a single entry with the log level
`INFO`. Messages written into the standard error are handled
similarly otherwise, but they are echoed back to the original stderr
after the keyword execution has finished. It is thus possible to use
the stderr if you need some messages to be visible on the console where
tests are executed.

#### Using log levels

To use other log levels than `INFO`, or to create several
messages, specify the log level explicitly by embedding the level into
the message in the format `*LEVEL* Actual log message`.
In this formant `*LEVEL*` must be in the beginning of a line and `LEVEL`
must be one of the available concrete log levels `TRACE`, `DEBUG`,
`INFO`, `WARN` or `ERROR`, or a pseudo log level `HTML` or `CONSOLE`.
The pseudo levels can be used for [logging HTML](#logging-html) and [logging to console](#logging-to-console),
respectively.

#### Errors and warnings

Messages with `ERROR` or `WARN` level are automatically written to the
console and a separate [Test Execution Errors section](http://docs.python.org/c-api/index.html) in the log
files. This makes these messages more visible than others and allows
using them for reporting important but non-critical problems to users.

#### Logging HTML

Everything normally logged by the library will be converted into a
format that can be safely represented as HTML. For example,
`<b>foo</b>` will be displayed in the log exactly like that and
not as **foo**. If libraries want to use formatting, links, display
images and so on, they can use a special pseudo log level
`HTML`. Robot Framework will write these messages directly into
the log with the `INFO` level, so they can use any HTML syntax
they want. Notice that this feature needs to be used with care,
because, for example, one badly placed `</table>` tag can ruin
the log file quite badly.

When using the [public logging API](#public-logging-api), various logging methods
have optional `html` attribute that can be set to `True`
to enable logging in HTML format.

#### Timestamps

By default messages logged via the standard output or error streams
get their timestamps when the executed keyword ends. This means that
the timestamps are not accurate and debugging problems especially with
longer running keywords can be problematic.

Keywords have a possibility to add an accurate timestamp to the messages
they log if there is a need. The timestamp must be given as milliseconds
since the [Unix epoch](http://en.wikipedia.org/wiki/Unix_time) and it must be placed after the [log level](http://docs.python.org/library/ctypes.html)
separated from it with a colon:

```
*INFO:1308435758660* Message with timestamp
*HTML:1308435758661* <b>HTML</b> message with timestamp
```

As illustrated by the examples below, adding the timestamp is easy.
It is, however, even easier to get accurate timestamps using the
[programmatic logging APIs](#programmatic-logging-apis). A big benefit of adding timestamps explicitly
is that this approach works also with the [remote library interface](remote-library.md#remote-library-interface).

```python
import time

def example_keyword():
    timestamp = int(time.time() * 1000)
    print(f'*INFO:{timestamp}* Message with timestamp')
```

#### Logging to console

Libraries have several options for writing messages to the console.
As already discussed, warnings and all messages written to the
standard error stream are written both to the log file and to the
console. Both of these options have a limitation that the messages end
up to the console only after the currently executing keyword finishes.

Starting from Robot Framework 6.1, libraries can use a pseudo log level
`CONSOLE` for logging messages *both* to the log file and to the console:

```python
def my_keyword(arg):
    print('*CONSOLE* Message both to log and to console.')
```
These messages will be logged to the log file using the `INFO` level similarly
as with the `HTML` pseudo log level. When using this approach, messages
are logged to the console only after the keyword execution ends.

Another option is writing messages to `sys.[__stdout](http://docs.python.org/c-api/index.html)` or `sys.[__stderr](http://docs.python.org/library/ctypes.html)`.
When using this approach, messages are written to the console immediately
and are not written to the log file at all:

```python
import sys

def my_keyword(arg):
    print('Message only to console.', file=sys.__stdout__)
```
The final option is using the [public logging API](#public-logging-api). Also in with this approach
messages are written to the console immediately:

```python
from robot.api import logger

def log_to_console(arg):
    logger.console('Message only to console.')

def log_to_console_and_log_file(arg):
    logger.info('Message both to log and to console.', also_console=True)
```
#### Logging example

In most cases, the `INFO` level is adequate. The levels below it,
`DEBUG` and `TRACE`, are useful for writing debug information.
These messages are normally not shown, but they can facilitate debugging
possible problems in the library itself. The `WARN` or `ERROR` level can
be used to make messages more visible and `HTML` is useful if any
kind of formatting is needed. Level `CONSOLE` can be used when the
message needs to shown both in console and in the log file.

The following examples clarify how logging with different levels
works.

```python
print('Hello from a library.')
print('*WARN* Warning from a library.')
print('*ERROR* Something unexpected happen that may indicate a problem in the test.')
print('*INFO* Hello again!')
print('This will be part of the previous message.')
print('*INFO* This is a new message.')
print('*INFO* This is <b>normal text</b>.')
print('*CONSOLE* This logs into console and log file.')
print('*HTML* This is <b>bold</b>.')
print('*HTML* <a href="http://robotframework.org">Robot Framework</a>')
```
<table class="messages">
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">Hello from a library.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="warn level">WARN</td>
    <td class="msg">Warning from a library.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="error level">ERROR</td>
    <td class="msg">Something unexpected happen that may indicate a problem in the test.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">Hello again!<br>This will be part of the previous message.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">This is a new message.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">This is &lt;b&gt;normal text&lt;/b&gt;.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">This logs into console and log file.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg">This is <b>bold</b>.</td>
  </tr>
  <tr>
    <td class="time">16:18:42.123</td>
    <td class="info level">INFO</td>
    <td class="msg"><a href="http://robotframework.org">Robot Framework</a></td>
  </tr>
</table>
### Programmatic logging APIs

Programmatic APIs provide somewhat cleaner way to log information than
using the standard output and error streams.

#### Public logging API

Robot Framework has a Python based logging API for writing
messages to the log file and to the console. Test libraries can use
this API like `logger.info('My message')` instead of logging
through the standard output like `print('*INFO* My message')`. In
addition to a programmatic interface being a lot cleaner to use, this
API has a benefit that the log messages have accurate [timestamps](#timestamps).

The public logging API [is thoroughly documented](http://docs.python.org/c-api/index.html) as part of the API
documentation at https://robot-framework.readthedocs.org. Below is
a simple usage example:

```python
from robot.api import logger

def my_keyword(arg):
    logger.debug(f"Got argument '{arg}'.")
    do_something()
    logger.info('<i>This</i> is a boring example', html=True)
    logger.console('Hello, console!')
```
An obvious limitation is that test libraries using this logging API have
a dependency to Robot Framework. If Robot Framework is not running,
the messages are redirected automatically to Python's standard [logging](http://docs.python.org/c-api/index.html)
module.

#### Using Python's standard `logging` module

In addition to the new [public logging API](#public-logging-api), Robot Framework offers a
built-in support to Python's standard [logging](http://docs.python.org/library/ctypes.html) module. This
works so that all messages that are received by the root logger of the
module are automatically propagated to Robot Framework's log
file. Also this API produces log messages with accurate [timestamps](#timestamps),
but logging HTML messages or writing messages to the console are not
supported. A big benefit, illustrated also by the simple example
below, is that using this logging API creates no dependency to Robot
Framework.

```python
import logging

def my_keyword(arg):
    logging.debug(f"Got argument '{arg}'.")
    do_something()
    logging.info('This is a boring example')
```
The `logging` module has slightly different log levels than
Robot Framework. Its levels `DEBUG`, `INFO`, `WARNING` and `ERROR` are mapped
directly to the matching Robot Framework log levels, and `CRITICAL`
is mapped to `ERROR`. Custom log levels are mapped to the closest
standard level smaller than the custom level. For example, a level
between `INFO` and `WARNING` is mapped to Robot Framework's `INFO` level.

### Logging during library initialization

Libraries can also log during the test library import and initialization.
These messages do not appear in the [log file](../executing-tests/result-files.md#log-file) like the normal log messages,
but are instead written to the [syslog](../executing-tests/result-files.md#syslog). This allows logging any kind of
useful debug information about the library initialization. Messages logged
using the `WARN` or `ERROR` levels are also visible in the [test execution errors](../executing-tests/basic-usage.md#test-execution)
section in the log file.

Logging during the import and initialization is possible both using the
[standard output and error streams](http://docs.python.org/c-api/index.html) and the [programmatic logging APIs](#programmatic-logging-apis).
Both of these are demonstrated below.

Library logging using the logging API during import:

```python
from robot.api import logger

logger.debug("Importing library")

def keyword():
    ...
```
!!! note
    If you log something during initialization, i.e. in Python
    `__init__`, the messages may be
    logged multiple times depending on the [library scope](#library-scope).

### Returning values

The final way for keywords to communicate back to the core framework
is returning information retrieved from the system under test or
generated by some other means. The returned values can be [assigned to
variables](http://docs.python.org/c-api/index.html) in the test data and then used as inputs for other keywords,
even from different test libraries.

Values are returned using the `return` statement in methods. Normally,
one value is assigned into one [scalar variable](http://docs.python.org/library/ctypes.html), as illustrated in
the example below. This example
also illustrates that it is possible to return any objects and to use
[extended variable syntax](../creating-test-data/variables.md#extended-variable-syntax) to access object attributes.

```python
from mymodule import MyObject

def return_string():
    return "Hello, world!"

def return_object(name):
    return MyObject(name)
```
```robotframework
*** Test Cases ***
Returning one value
    ${string} =    Return String
    Should Be Equal    ${string}    Hello, world!
    ${object} =    Return Object    Robot
    Should Be Equal    ${object.name}    Robot
```
Keywords can also return values so that they can be assigned into
several [scalar variables](../creating-test-data/variables.md#scalar-variables) at once, into [a list variable](http://docs.python.org/c-api/index.html), or
into scalar variables and a list variable. All these usages require
that returned values are lists or list-like objects.

```python
def return_two_values():
    return 'first value', 'second value'

def return_multiple_values():
    return ['a', 'list', 'of', 'strings']
```
```robotframework
*** Test Cases ***
Returning multiple values
    ${var1}    ${var2} =    Return Two Values
    Should Be Equal    ${var1}    first value
    Should Be Equal    ${var2}    second value
    @{list} =    Return Two Values
    Should Be Equal    @{list}[0]    first value
    Should Be Equal    @{list}[1]    second value
    ${s1}    ${s2}    @{li} =    Return Multiple Values
    Should Be Equal    ${s1} ${s2}    a list
    Should Be Equal    @{li}[0] @{li}[1]    of strings
```
### Detecting is Robot Framework running

Starting from Robot Framework 6.1, it is easy to detect is Robot Framework
running at all and is the dry-run mode active by using the `robot_running`
and `dry_run_active` properties of the BuiltIn library. A relatively common
use case is that library initializers may want to avoid doing some work if
the library is not used during execution but is initialized, for example,
by [Libdoc](../supporting-tools/libdoc.md#libdoc):

```python
from robot.libraries.BuiltIn import BuiltIn

class MyLibrary:

    def __init__(self):
        builtin = BuiltIn()
        if builtin.robot_running and not builtin.dry_run_active:
            # Do some initialization that only makes sense during real execution.
```
For more information about using the BuiltIn library as a programmatic API,
including another example using `robot_running`, see the [Using BuiltIn library](#using-builtin-library)
section.

### Communication when using threads

If a library uses threads, it should generally communicate with the
framework only from the main thread. If a worker thread has, for
example, a failure to report or something to log, it should pass the
information first to the main thread, which can then use exceptions or
other mechanisms explained in this section for communication with the
framework.

This is especially important when threads are run on background while
other keywords are running. Results of communicating with the
framework in that case are undefined and can in the worst case cause a
crash or a corrupted output file. If a keyword starts something on
background, there should be another keyword that checks the status of
the worker thread and reports gathered information accordingly.

Messages logged by non-main threads using the normal logging methods from
[programmatic logging APIs](#programmatic-logging-apis)  are silently ignored.

There is also a `BackgroundLogger` in separate [robotbackgroundlogger](http://docs.python.org/c-api/index.html) project,
with a similar API as the standard `robot.api.logger`. Normal logging
methods will ignore messages from other than main thread, but the
`BackgroundLogger` will save the background messages so that they can be later
logged to Robot's log.

## Distributing test libraries

### Documenting libraries

A test library without documentation about what keywords it
contains and what those keywords do is rather useless. To ease
maintenance, it is highly recommended that library documentation is
included in the source code and generated from it. Basically, that
means using [docstrings](http://www.python.org/dev/peps/pep-0257) as in the example below.

```python
class MyLibrary:
    """This is an example library with some documentation."""

    def keyword_with_short_documentation(self, argument):
        """This keyword has only a short documentation"""
        pass

    def keyword_with_longer_documentation(self):
        """First line of the documentation is here.

        Longer documentation continues here and it can contain
        multiple lines or paragraphs.
        """
        pass
```
Python has tools for creating an API documentation of a
library documented as above. However, outputs from these tools can be slightly
technical for some users. Another alternative is using Robot
Framework's own documentation tool [Libdoc](../supporting-tools/libdoc.md#libdoc). This tool can
create a library documentation from libraries
using the static library API, such as the ones above, but it also handles
libraries using the [dynamic library API](dynamic-library-api.md#dynamic-library-api).

The first logical line of a keyword documentation, until the first empty line,
is used for a special purpose and should contain a short overall description
of the keyword. It is used as a *short documentation* by [Libdoc](../supporting-tools/libdoc.md#libdoc) (for example,
as a tool tip) and also shown in the [test logs](../executing-tests/result-files.md#log).

By default documentation is considered to follow Robot Framework's
[documentation formatting](../appendices/documentation-formatting.md#documentation-formatting) rules. This simple format allows often used
styles like `*bold*[and](../creating-test-data/variable-files.md#command-line)italic_`, tables, lists, links, etc.
It is possible to use also HTML, plain
text and [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) formats. See the [Documentation format](#documentation-format)
section for information how to set the format in the library source code and
[Libdoc](../supporting-tools/libdoc.md#libdoc) chapter for more information about the formats in general.

!!! note
    Prior to Robot Framework 3.1, the short documentation contained
    only the first physical line of the keyword documentation.

### Testing libraries

Any non-trivial test library needs to be thoroughly tested to prevent
bugs in them. Of course, this testing should be automated to make it
easy to rerun tests when libraries are changed.

Python has excellent unit testing tools, and they suite
very well for testing libraries. There are no major differences in
using them for this purpose compared to using them for some other
testing. The developers familiar with these tools do not need to learn
anything new, and the developers not familiar with them should learn
them anyway.

It is also easy to use Robot Framework itself for testing libraries
and that way have actual end-to-end acceptance tests for them. There are
plenty of useful keywords in the [BuiltIn](../creating-test-data/using-test-libraries.md#builtin) library for this
purpose. One worth mentioning specifically is *Run Keyword And Expect
Error*, which is useful for testing that keywords report errors
correctly.

Whether to use a unit- or acceptance-level testing approach depends on
the context. If there is a need to simulate the actual system under
test, it is often easier on the unit level. On the other hand,
acceptance tests ensure that keywords do work through Robot
Framework. If you cannot decide, of course it is possible to use both
the approaches.

### Packaging libraries

After a library is implemented, documented, and tested, it still needs
to be distributed to the users. With simple libraries consisting of a
single file, it is often enough to ask the users to copy that file
somewhere and set the [module search path](../executing-tests/configuring-execution.md#module-search-path) accordingly. More
complicated libraries should be packaged to make the installation
easier.

Since libraries are normal programming code, they can be packaged
using normal packaging tools. For information about packaging and
distributing Python code see https://packaging.python.org/. When such
a package is installed using [pip](../creating-test-data/test-data-syntax.md#pipe-separated-format) or other tools, it is automatically
in the [module search path](../executing-tests/configuring-execution.md#module-search-path).

### Deprecating keywords

Sometimes there is a need to replace existing keywords with new ones
or remove them altogether. Just informing the users about the change
may not always be enough, and it is more efficient to get warnings at
runtime. To support that, Robot Framework has a capability to mark
keywords *deprecated*. This makes it easier to find old keywords from
the test data and remove or replace them.

Keywords can be deprecated by starting their documentation with text
`*DEPRECATED`, case-sensitive, and having a closing `*` also on the first
line of the documentation. For example, `*DEPRECATED*`, `*DEPRECATED.*`, and
`*DEPRECATED in version 1.5.*` are all valid markers.

When a deprecated keyword is executed, a deprecation warning is logged and
the warning is shown also in [the console and the Test Execution Errors
section in log files](http://docs.python.org/c-api/index.html). The deprecation warning starts with text `Keyword
'<name>' is deprecated.` and has rest of the [short documentation](http://docs.python.org/library/ctypes.html) after
the deprecation marker, if any, afterwards. For example, if the following
keyword is executed, there will be a warning like shown below in the log file.

```python
def example_keyword(argument):
    """*DEPRECATED!!* Use keyword `Other Keyword` instead.

    This keyword does something to given `argument` and returns results.
    """
    return do_something(argument)
```
<table class="messages">
  <tr>
    <td class="time">20080911&nbsp;16:00:22.650</td>
    <td class="warn level">WARN</td>
    <td class="msg">Keyword 'SomeLibrary.Example Keyword' is deprecated. Use keyword `Other Keyword` instead.</td>
  </tr>
</table>
This deprecation system works with most test libraries and also with
[user keywords](http://docs.python.org/c-api/index.html).

## Handling Robot Framework's timeouts

Robot Framework has its own [timeouts](../creating-test-data/advanced-features.md#timeouts) that can be used for stopping keyword
execution if a test or a keyword takes too much time.
There are two things to take into account related to them.

### Doing cleanup if timeout occurs

Timeouts are technically implemented using `robot.errors.TimeoutExceeded`
exception that can occur any time during a keyword execution. If a keyword
wants to make sure possible cleanup activities are always done, it needs to
handle these exceptions. Probably the simplest way to handle exceptions is
using Python's `try/finally` structure:

```python
def example():
    try:
        do_something()
    finally:
        do_cleanup()
```
A benefit of the above is that cleanup is done regardless of the exception.
If there is a need to handle timeouts specially, it is possible to catch
`TimeoutExceeded` explicitly. In that case it is important to re-raise the
original exception afterwards:

```python
from robot.errors import TimeoutExceeded

def example():
    try:
        do_something()
    except TimeoutExceeded:
        do_cleanup()
        raise
```
`TimeoutExceeded` is based directly on Python's [BaseException](http://docs.python.org/c-api/index.html), which means that
it is not caught by code handling [Exception](http://docs.python.org/library/ctypes.html) and its subtypes. The motivation is
to avoid timeouts being accidentally disabled if code catches all normal exceptions
like in this example:

```python
def example():
    try:
        do_something()
    except Exception as err:
        print(f"Error occurred: {err}")
```
If you want to handle `TimeoutExceeded`, catch it explicitly or use `finally`
like in the earlier examples.

!!! note
    Prior to Robot Framework 7.5, `TimeoutExceeded` was based on
    `Exception`, not `BaseException`.

!!! note
    The `TimeoutExceeded` exception was named `TimeoutError` prior to
    Robot Framework 7.3. It was renamed to avoid a conflict with Python's
    standard exception with the same name. The old name still exists as
    a backwards compatible alias in the `robot.errors` module and can
    be used if older Robot Framework versions need to be supported.

### Allowing timeouts to stop execution

Robot Framework's timeouts can stop normal Python code, but if the code calls
functionality implemented using C or some other language, timeouts may
not work. Well behaving keywords should thus avoid long blocking calls that
cannot be interrupted.

As an example, [subprocess.run](http://docs.python.org/c-api/index.html) cannot be interrupted on Windows, so
the following simple keyword cannot be stopped by timeouts there:

```python
import subprocess

def run_command(command, *args):
    result = subprocess.run([command, *args], encoding='UTF-8')
    print(f'stdout: {result.stdout}\nstderr: {result.stderr}')
```
This problem can be avoided by using the lower level [subprocess.Popen](http://docs.python.org/c-api/index.html)
and handling waiting in a loop with short timeouts. This adds quite a lot
of complexity, though, so it may not be worth the effort in all cases.

```python
import subprocess

def run_command(command, *args):
    process = subprocess.Popen([command, *args], encoding='UTF-8',
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        try:
            stdout, stderr = process.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            continue
        else:
            break
    print(f'stdout: {stdout}\nstderr: {stderr}')
```

## Using Robot Framework's internal modules

Test libraries can use Robot Framework's
internal modules, for example, to get information about the executed
tests and the settings that are used. This powerful mechanism to
communicate with the framework should be used with care, though,
because all Robot Framework's APIs are not meant to be used by
externally and they might change radically between different framework
versions.

### Available APIs

[API documentation](http://robot-framework.readthedocs.org) is hosted separately
at the excellent [Read the Docs](http://readthedocs.org) service. If you are unsure how to use
certain API or is using them forward compatible, please send a question
to [mailing list](../getting-started/introduction.md#mailing-list).

### Using BuiltIn library

The safest API to use are methods implementing keywords in the
[BuiltIn](../creating-test-data/using-test-libraries.md#builtin) library. Changes to keywords are rare and they are always
done so that old usage is first deprecated. One of the most useful
methods is `replace_variables` which allows accessing currently
available variables. The following example demonstrates how to get
`${OUTPUT_DIR}` which is one of the many handy [automatic
variables](../creating-test-data/variables.md#automatic-variables). It is also possible to set new variables from libraries
using `set_test_variable`, `set_suite_variable` and
`set_global_variable`.

```python
import os.path
from robot.libraries.BuiltIn import BuiltIn

def do_something(argument):
    builtin = BuiltIn()
    output = do_something_that_creates_a_lot_of_output(argument)
    if builtin.robot_running:
        output_dir = builtin.replace_variables('${OUTPUT_DIR}')
    else:
        output_dir = '.'
    with open(os.path.join(output_dir, 'output.txt'), 'w') as file:
        file.write(output)
    print('*HTML* Output written to <a href="output.txt">output.txt</a>')
```
As the above examples illustrates, BuiltIn also has a convenient `robot_running`
property for [detecting is Robot Framework running](#detecting-is-robot-framework-running).

The only catch with using methods from `BuiltIn` is that all
`run_keyword` method variants must be handled specially.
Methods that use `run_keyword` methods have to be registered
as *run keywords* themselves using `register_run_keyword`
method in `BuiltIn` module. This method's documentation explains
why this needs to be done and obviously also how to do it.

## Extending existing test libraries

This section explains different approaches how to add new
functionality to existing test libraries and how to use them in your
own libraries otherwise.

### Modifying original source code

If you have access to the source code of the library you want to
extend, you can naturally modify the source code directly. The biggest
problem of this approach is that it can be hard for you to update the
original library without affecting your changes. For users it may also
be confusing to use a library that has different functionality than
the original one. Repackaging the library may also be a big extra
task.

This approach works extremely well if the enhancements are generic and
you plan to submit them back to the original developers. If your
changes are applied to the original library, they are included in the
future releases and all the problems discussed above are mitigated. If
changes are non-generic, or you for some other reason cannot submit
them back, the approaches explained in the subsequent sections
probably work better.

### Using inheritance

Another straightforward way to extend an existing library is using
inheritance. This is illustrated by the example below that adds new
*Title Should Start With* keyword to the [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary).

```python
from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary

class ExtendedSeleniumLibrary(SeleniumLibrary):

    @keyword
    def title_should_start_with(self, expected):
        title = self.get_title()
        if not title.startswith(expected):
            raise AssertionError(f"Title '{title}' did not start with '{expected}'.")
```
A big difference with this approach compared to modifying the original
library is that the new library has a different name than the
original. A benefit is that you can easily tell that you are using a
custom library, but a big problem is that you cannot easily use the
new library with the original. First of all your new library will have
same keywords as the original meaning that there is always
[conflict](http://docs.python.org/c-api/index.html). Another problem is that the libraries do not share their
state.

This approach works well when you start to use a new library and want
to add custom enhancements to it from the beginning. Otherwise other
mechanisms explained in this section are probably better.

### Using other libraries directly

Because test libraries are technically just classes or modules, a
simple way to use another library is importing it and using its
methods. This approach works great when the methods are static and do
not depend on the library state. This is illustrated by the earlier
example that uses [Robot Framework's BuiltIn library](http://docs.python.org/library/ctypes.html).

If the library has state, however, things may not work as you would
hope.  The library instance you use in your library will not be the
same as the framework uses, and thus changes done by executed keywords
are not visible to your library. The next section explains how to get
an access to the same library instance that the framework uses.

### Getting active library instance from Robot Framework

[BuiltIn](../creating-test-data/using-test-libraries.md#builtin) keyword *Get Library Instance* can be used to get the
currently active library instance from the framework itself. The
library instance returned by this keyword is the same as the framework
itself uses, and thus there is no problem seeing the correct library
state. Although this functionality is available as a keyword, it is
typically used in test libraries directly by importing the *BuiltIn*
library class [as discussed earlier](https://docs.python.org/3/reference/simple_stmts.html#import). The following example illustrates
how to implement the same *Title Should Start With* keyword as in
the earlier example about [using inheritance](#using-inheritance).

```python
from robot.libraries.BuiltIn import BuiltIn

def title_should_start_with(expected):
    seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
    title = seleniumlib.get_title()
    if not title.startswith(expected):
        raise AssertionError(f"Title '{title}' did not start with '{expected}'.")
```
This approach is clearly better than importing the library directly
and using it when the library has a state. The biggest benefit over
inheritance is that you can use the original library normally and use
the new library in addition to it when needed. That is demonstrated in
the example below where the code from the previous examples is
expected to be available in a new library *SeLibExtensions*.

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    SeLibExtensions

*** Test Cases ***
Example
    Open Browser    http://example      # SeleniumLibrary
    Title Should Start With    Example  # SeLibExtensions
```
