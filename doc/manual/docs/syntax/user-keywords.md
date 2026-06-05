
<a id="user-keyword"></a>
# Creating user keywords

Keyword sections are used to create new higher-level keywords by
combining existing keywords together. These keywords are called *user
keywords* to differentiate them from lowest level *library keywords*
that are implemented in test libraries. The syntax for creating user
keywords is very close to the syntax for creating test cases, which
makes it easy to learn.

## User keyword syntax

### Basic syntax

In many ways, the overall user keyword syntax is identical to the
[test case syntax](creating-test-cases.md#test-case-syntax).  User keywords are created in Keyword sections
which differ from Test Case sections only by the name that is used to
identify them. User keyword names are in the first column similarly as
test cases names. Also user keywords are created from keywords, either
from keywords in test libraries or other user keywords. Keyword names
are normally in the second column, but when setting variables from
keyword return values, they are in the subsequent columns.

```robotframework
*** Keywords ***
Open Login Page
    Open Browser    http://host/login.html
    Title Should Be    Login Page

Title Should Start With
    [Arguments]    ${expected}
    ${title} =    Get Title
    Should Start With    ${title}    ${expected}
```
Most user keywords take some arguments. This important feature is used
already in the second example above, and it is explained in detail
[later in this section](https://www.python.org/dev/peps/pep-3102), similarly as [user keyword return
values](#user-keyword-return-values).

User keywords can be created in [suite files](creating-test-suites.md#suite-files), [resource files](resource-files.md#resource-files),
and [suite initialization files](creating-test-suites.md#suite-initialization-files). Keywords created in resource
files are available for files using them, whereas other keywords are
only available in the files where they are created.

### Settings in the Keyword section

User keywords can have similar settings as [test cases](http://en.wikipedia.org/wiki/Regular_expression), and they
have the same square bracket syntax separating them from keyword
names. All available settings are listed below and explained later in
this section.

`[Documentation]`
: Used for setting a [user keyword documentation](#user-keyword-documentation).

`[Tags]`
: Sets [tags](https://docs.python.org/3/library/re.html#regular-expression-syntax) for the keyword.

`[Arguments]`
: Specifies [user keyword arguments](#user-keyword-arguments).

`[Setup]`, `[Teardown]`
: Specify [user keyword setup and teardown](#user-keyword-setup-and-teardown). `[Setup]` is new in
   Robot Framework 7.0.

`[Timeout]`
: Sets the possible [user keyword timeout](advanced-features.md#user-keyword-timeout). [Timeouts](advanced-features.md#timeouts) are discussed
   in a section of their own.

`[Return]`
: Specifies [user keyword return values](#user-keyword-return-values). Deprecated in Robot Framework 7.0,
   the [RETURN](#return) statement should be used instead.

!!! note
    The format used above is recommended, but setting names are
    case-insensitive and spaces are allowed between brackets and the name.
    For example, `[ TAGS ]`:setting is valid.

<a id="user-keyword-documentation"></a>
## User keyword name and documentation

The user keyword name is defined in the first column of the
Keyword section. Of course, the name should be descriptive, and it is
acceptable to have quite long keyword names. Actually, when creating
use-case-like test cases, the highest-level keywords are often
formulated as sentences or even paragraphs.

User keywords can have a documentation that is set with the
`[Documentation]` setting. It supports same formatting,
splitting to multiple lines, and other features as [test case documentation](creating-test-cases.md#test-case-documentation).
This setting documents the user keyword in the test data. It is also shown
in a more formal keyword documentation, which the [Libdoc](../supporting-tools/libdoc.md#libdoc) tool can create
from [resource files](resource-files.md#resource-files). Finally, the first logical row of the documentation,
until the first empty row, is shown as a keyword documentation in [test logs](../executing-tests/result-files.md#log).

```robotframework
*** Keywords ***
One line documentation
    [Documentation]    One line documentation.
    No Operation

Multiline documentation
    [Documentation]    The first line creates the short doc.
    ...
    ...                This is the body of the documentation.
    ...                It is not shown in Libdoc outputs but only
    ...                the short doc is shown in logs.
    No Operation

Short documentation in multiple lines
    [Documentation]    If the short doc gets longer, it can span
    ...                multiple physical lines.
    ...
    ...                The body is separated from the short doc with
    ...                an empty line.
    No Operation
```
Sometimes keywords need to be removed, replaced with new ones, or
deprecated for other reasons.  User keywords can be marked deprecated
by starting the documentation with `*DEPRECATED*`, which will
cause a warning when the keyword is used. For more information, see
the [Deprecating keywords](../extending/creating-test-libraries.md#deprecating-keywords) section.

!!! note
    Prior to Robot Framework 3.1, the short documentation contained
    only the first physical line of the keyword documentation.

## User keyword tags

Both user keywords and [library keywords](../extending/creating-test-libraries.md#creating-keywords) can have tags. Similarly as when
[tagging test cases](creating-test-cases.md#tagging-test-cases), there are two settings affecting user keyword tags:

`Keyword Tags` setting in the Settings section
: All keywords in a file with this setting always get specified tags.

`[Tags]` setting with each keyword
: Keywords get these tags in addition to possible tags specified using the
   `Keyword Tags` setting. The `[Tags]` setting also allows
   removing tags set with `Keyword Tags` by using the `-tag` syntax.

```robotframework
*** Settings ***
Keyword Tags       gui    html

*** Keywords ***
No own tags
    [Documentation]    Keyword has tags 'gui' and 'html'.
    No Operation

Own tags
    [Documentation]    Keyword has tags 'gui', 'html', 'own' and 'tags'.
    [Tags]    own    tags
    No Operation

Remove common tag
    [Documentation]    Test has tags 'gui' and 'own'.
    [Tags]    own    -html
    No Operation
```
Keyword tags can be specified using variables, the `-tag` syntax supports
patterns, and so on, exactly as [test case tags](creating-test-cases.md#test-case-tags).

In addition to using the dedicated settings, keyword tags can be specified on
the last line of the documentation with `Tags:` prefix so that tags are separated
with a comma. For example, following two keywords get same three tags:

```robotframework
*** Keywords ***
Settings tags using separate setting
    [Tags]    my    fine    tags
    No Operation

Settings tags using documentation
    [Documentation]    I have documentation. And my documentation has tags.
    ...                Tags: my, fine, tags
    No Operation
```
Keyword tags are shown in logs and in documentation generated by [Libdoc](../supporting-tools/libdoc.md#libdoc),
where the keywords can also be searched based on tags. The [--removekeywords](https://www.python.org/dev/peps/pep-3102)
and [--flattenkeywords](http://en.wikipedia.org/wiki/Regular_expression) commandline options also support selecting keywords by
tag, and new usages for keywords tags are possibly added in later releases.

Similarly as with [test case tags](creating-test-cases.md#test-case-tags), user keyword tags with the `robot:`
prefix are [reserved](https://docs.python.org/3/library/re.html#regular-expression-syntax) for special features by Robot Framework
itself. Users should thus not use any tag with these prefixes unless actually
activating the special functionality. Starting from Robot Framework 6.1,
[flattening keyword during execution time](../executing-tests/result-files.md#flattening-keyword-during-execution-time) can be taken into use using
reserved tag `robot:flatten`.

!!! note
    `Keyword Tags` is new in Robot Framework 6.0. With earlier
    versions all keyword tags need to be specified using the
    `[Tags]` setting.

!!! note
    The `-tag` syntax for removing common tags is new in Robot Framework 7.0.

## User keyword arguments

Most user keywords need to take some arguments. The syntax for
specifying them is probably the most complicated feature normally
needed with Robot Framework, but even that is relatively easy,
particularly in most common cases. Arguments are normally specified with
the `[Arguments]` setting, and argument names use the same
syntax as [variables](variables.md#variables), for example `${arg}`.

### Positional arguments with user keywords

The simplest way to specify arguments (apart from not having them at all)
is using only positional arguments. In most cases, this is all
that is needed.

The syntax is such that first the `[Arguments]` setting is
given and then argument names are defined in the subsequent
cells. Each argument is in its own cell, using the same syntax as with
variables. The keyword must be used with as many arguments as there
are argument names in its signature. The actual argument names do not
matter to the framework, but from users' perspective they should
be as descriptive as possible. It is recommended
to use lower-case letters in variable names, either as
`${my_arg}`, `${my arg}` or `${myArg}`.

```robotframework
*** Keywords ***
One Argument
    [Arguments]    ${arg_name}
    Log    Got argument ${arg_name}

Three Arguments
    [Arguments]    ${arg1}    ${arg2}    ${arg3}
    Log    1st argument: ${arg1}
    Log    2nd argument: ${arg2}
    Log    3rd argument: ${arg3}
```
### Default values with user keywords

When creating user keywords, positional arguments are sufficient in
most situations. It is, however, sometimes useful that keywords have
[default values](creating-test-cases.md#default-values) for some or all of their arguments. Also user keywords
support default values, and the needed new syntax does not add very much
to the already discussed basic syntax.

In short, default values are added to arguments, so that first there is
the equals sign (`=`) and then the value, for example `${arg}=default`.
There can be many arguments with defaults, but they all must be given after
the normal positional arguments. The default value can contain a [variable](variables.md#variable)
created on [test, suite or global scope](https://www.python.org/dev/peps/pep-3102), but local variables of the keyword
executor cannot be used. Default value can
also be defined based on earlier arguments accepted by the keyword.

!!! note
    The syntax for default values is space sensitive. Spaces
    before the `=` sign are not allowed, and possible spaces
    after it are considered part of the default value itself.

```robotframework
*** Keywords ***
One Argument With Default Value
    [Arguments]    ${arg}=default value
    [Documentation]    This keyword takes 0-1 arguments
    Log    Got argument ${arg}

Two Arguments With Defaults
    [Arguments]    ${arg1}=default 1    ${arg2}=${VARIABLE}
    [Documentation]    This keyword takes 0-2 arguments
    Log    1st argument ${arg1}
    Log    2nd argument ${arg2}

One Required And One With Default
    [Arguments]    ${required}    ${optional}=default
    [Documentation]    This keyword takes 1-2 arguments
    Log    Required: ${required}
    Log    Optional: ${optional}

 Default Based On Earlier Argument
    [Arguments]    ${a}    ${b}=${a}    ${c}=${a} and ${b}
    Should Be Equal    ${a}    ${b}
    Should Be Equal    ${c}    ${a} and ${b}
```
When a keyword accepts several arguments with default values and only
some of them needs to be overridden, it is often handy to use the
[named arguments](creating-test-cases.md#named-arguments) syntax. When this syntax is used with user
keywords, the arguments are specified without the `${}`
decoration. For example, the second keyword above could be used like
below and `${arg1}` would still get its default value.

```robotframework
*** Test Cases ***
Example
    Two Arguments With Defaults    arg2=new value
```
As all Pythonistas must have already noticed, the syntax for
specifying default arguments is heavily inspired by Python syntax for
function default values.

### Variable number of arguments with user keywords

Sometimes even default values are not enough and there is a need
for a keyword accepting [variable number of arguments](creating-test-cases.md#variable-number-of-arguments). User keywords
support also this feature. All that is needed is having [list variable](variables.md#list-variable) such
as `@{varargs}` after possible positional arguments in the keyword signature.
This syntax can be combined with the previously described default values, and
at the end the list variable gets all the leftover arguments that do not match
other arguments. The list variable can thus have any number of items, even zero.

```robotframework
*** Keywords ***
Any Number Of Arguments
    [Arguments]    @{varargs}
    Log Many    @{varargs}

One Or More Arguments
    [Arguments]    ${required}    @{rest}
    Log Many    ${required}    @{rest}

Required, Default, Varargs
    [Arguments]    ${req}    ${opt}=42    @{others}
    Log    Required: ${req}
    Log    Optional: ${opt}
    Log    Others:
    FOR    ${item}    IN    @{others}
        Log    ${item}
    END
```
Notice that if the last keyword above is used with more than one
argument, the second argument `${opt}` always gets the given
value instead of the default value. This happens even if the given
value is empty. The last example also illustrates how a variable
number of arguments accepted by a user keyword can be used in a [for
loop](https://www.python.org/dev/peps/pep-3102). This combination of two rather advanced functions can
sometimes be very useful.

The keywords in the examples above could be used, for example, like this:

```robotframework
*** Test Cases ***
Varargs with user keywords
    Any Number Of Arguments
    Any Number Of Arguments    arg
    Any Number Of Arguments    arg1    arg2    arg3   arg4
    One Or More Arguments    required
    One Or More Arguments    arg1    arg2    arg3   arg4
    Required, Default, Varargs    required
    Required, Default, Varargs    required    optional
    Required, Default, Varargs    arg1    arg2    arg3    arg4    arg5
```
Again, Pythonistas probably notice that the variable number of
arguments syntax is very close to the one in Python.

### Free named arguments with user keywords

User keywords can also accept [free named arguments](creating-test-cases.md#free-named-arguments) by having a [dictionary
variable](variables.md#dictionary-variable) like `&{named}` as the absolutely last argument. When the keyword
is called, this variable will get all [named arguments](creating-test-cases.md#named-arguments) that do not match
any [positional argument](https://www.python.org/dev/peps/pep-3102) or [named-only argument](http://en.wikipedia.org/wiki/Regular_expression) in the keyword
signature.

```robotframework
*** Keywords ***
Free Named Only
    [Arguments]    &{named}
    Log Many    &{named}

Positional And Free Named
    [Arguments]    ${required}    &{extra}
    Log Many    ${required}    &{extra}

Run Program
    [Arguments]    @{args}    &{config}
    Run Process    program.py    @{args}    &{config}
```
The last example above shows how to create a wrapper keyword that
accepts any positional or named argument and passes them forward.
See [free named argument examples](creating-test-cases.md#free-named-argument-examples) for a full example with same keyword.

Free named arguments support with user keywords works similarly as kwargs
work in Python. In the signature and also when passing arguments forward,
`&{kwargs}` is pretty much the same as Python's `**kwargs`.

### Named-only arguments with user keywords

User keywords support [named-only arguments](creating-test-cases.md#named-only-arguments) that are inspired by Python's
[keyword-only arguments](https://www.python.org/dev/peps/pep-3102).
This syntax is typically used by having normal arguments *after*
[variable number of arguments](http://en.wikipedia.org/wiki/Regular_expression) (`@{varargs}`). If the keywords does not
use varargs, it is possible to use just `@{}` to denote that the subsequent
arguments are named-only:

```robotframework
*** Keywords ***
With Varargs
    [Arguments]    @{varargs}    ${named}
    Log Many    @{varargs}    ${named}

Without Varargs
    [Arguments]    @{}    ${first}    ${second}
    Log Many    ${first}    ${second}
```
Named-only arguments can be used together with [positional arguments](https://www.python.org/dev/peps/pep-3102) as
well as with [free named arguments](http://en.wikipedia.org/wiki/Regular_expression). When using free named arguments, they
must be last:

```robotframework
*** Keywords ***
With Positional
    [Arguments]    ${positional}    @{}    ${named}
    Log Many    ${positional}    ${named}

With Free Named
    [Arguments]    @{varargs}    ${named only}    &{free named}
    Log Many    @{varargs}    ${named only}    &{free named}
```
When passing named-only arguments to keywords, their order does not matter
other than they must follow possible positional arguments. The keywords above
could be used, for example, like this:

```robotframework
*** Test Cases ***
Example
    With Varargs    named=value
    With Varargs    positional    second positional    named=foobar
    Without Varargs    first=1    second=2
    Without Varargs    second=toka    first=eka
    With Positional    foo    named=bar
    With Positional    named=2    positional=1
    With Free Named    positional    named only=value    x=1    y=2
    With Free Named    foo=a    bar=b    named only=c    quux=d
```
Named-only arguments can have default values similarly as [normal user
keyword arguments](https://www.python.org/dev/peps/pep-3102). A minor difference is that the order of arguments
with and without default values is not important.

```robotframework
*** Keywords ***
With Default
    [Arguments]    @{}    ${named}=default
    Log Many    ${named}

With And Without Defaults
    [Arguments]    @{}    ${optional}=default    ${mandatory}    ${mandatory 2}    ${optional 2}=default 2    ${mandatory 3}
    Log Many    ${optional}    ${mandatory}    ${mandatory 2}    ${optional 2}    ${mandatory 3}
```

### Argument conversion with user keywords

User keywords support automatic argument conversion based on explicitly specified
types. The type syntax `${name: type}` is the same, and the supported conversions
are the same, as when [creating variables](https://www.python.org/dev/peps/pep-3102).

The basic usage with normal arguments is very simple. You only need to specify
the type like `${count: int}` and the used value is converted automatically.
If an argument has a default value like `${count: int}=1`, also the default
value will be converted. If conversion fails, calling the keyword fails with
an informative error message.

```robotframework
*** Test Cases ***
Move around
    Move    3
    Turn    LEFT
    Move    2.3    log=True
    Turn    right

Failing move
    Move    bad

Failing turn
    Turn    oops

*** Keywords ***
Move
    [Arguments]    ${distance: float}    ${log: bool}=False
    IF    ${log}
        Log    Moving ${distance} meters.
    END

 Turn
    [Arguments]    ${direction: Literal["LEFT", "RIGHT"]}
    Log    Turning ${direction}.
```
!!! tip
    Using `Literal`, like in the above example, is a convenient way to
    limit what values are accepted.

When using [variable number of arguments](https://www.python.org/dev/peps/pep-3102), the type is specified like
`@{numbers: int}` and is applied to all arguments. If arguments may have
different types, it is possible to use an union like `@{numbers: float | int}`.
With [free named arguments](http://en.wikipedia.org/wiki/Regular_expression) the type is specified like `&{named: int}` and
it is applied to all argument values. Converting argument names is not supported.

```robotframework
*** Test Cases ***
Varargs
    Send bytes    Hello!    Hyvä!    \x00\x00\x07

Free named
    Log releases    rc 1=2025-05-08    rc 2=2025-05-19    rc 3=2025-05-21    final=2025-05-30

*** Keywords ***
Send bytes
    [Arguments]    @{data: bytes}
    FOR    ${value}    IN    @{data}
        Log    ${value}    formatter=repr
    END

Log releases
    [Arguments]    &{releases: date}
    FOR    ${version}    ${date}    IN    &{releases}
        Log    RF 7.3 ${version} was released on ${date.day}.${date.month}.${date.year}.
    END
```
!!! note
    Argument conversion with user keywords is new in Robot Framework 7.3.

<a id="embedded-argument-syntax"></a>
## Embedding arguments into keyword name

The previous section explained how to pass arguments to keywords so
that they are listed separately after the keyword name. Robot
Framework has also another approach to pass arguments, embedding them
directly to the keyword name, used by the second test below:

```robotframework
*** Test Cases ***
Normal arguments
    Select from list    cat

Embedded arguments
    Select cat from list
```
As the example illustrates, embedding arguments to keyword names
can make the data easier to read and understand even for people without
any Robot Framework experience.

### Basic syntax

The previous example showed how using a keyword *Select cat from list* is
more fluent than using *Select from list* so that `cat` is passed to
it as an argument. We obviously could implement *Select cat from list*
as a normal keyword accepting no arguments, but then we needed to implement
various other keywords like *Select dog from list* for other animals.
Embedded arguments simplify this and we can instead implement just one
keyword with name *Select ${animal} from list* and use it with any
animal:

```robotframework
*** Test Cases ***
Embedded arguments
    Select cat from list
    Select dog from list

*** Keywords ***
Select ${animal} from list
    Open Page    Pet Selection
    Select Item From List    animal_list    ${animal}
```
As the above example shows, embedded arguments are specified simply by using
variables in keyword names. The arguments used in the name are naturally
available inside the keyword and they have different values depending on how
the keyword is called. In the above example, `${animal}` has value `cat` when
the keyword is used for the first time and `dog` when it is used for
the second time.

Starting from Robot Framework 6.1, it is possible to create user keywords
that accept both embedded and "normal" arguments:

```robotframework
*** Test Cases ***
Embedded and normal arguments
    Number of cats should be    2
    Number of dogs should be    count=3

*** Keywords ***
Number of ${animals} should be
    [Arguments]    ${count}
    Open Page    Pet Selection
    Select Items From List    animal_list    ${animals}
    Number of Selected List Items Should Be    ${count}
```
Other than the special name, keywords with embedded
arguments are created just like other user keywords. They are also used the same
way as other keywords except that spaces and underscores are not ignored in their
names when keywords are matched. They are, however, case-insensitive like
other keywords. For example, the *Select ${animal} from list* keyword could
be used like *select cow from list*, but not like *Select cow fromlist*.

Embedded arguments do not support default values or variable number of
arguments like normal arguments do. If such functionality is needed, normal
arguments should be used instead. Passing embedded arguments as variables
is possible, but that can reduce readability:

```robotframework
*** Variables ***
${SELECT}        cat

*** Test Cases ***
Embedded arguments with variable
    Select ${SELECT} from list

*** Keywords ***
Select ${animal} from list
    Open Page    Pet Selection
    Select Item From List    animal_list    ${animal}
```
### Embedded arguments matching wrong values

One tricky part in using embedded arguments is making sure that the
values used when calling the keyword match the correct arguments. This
is a problem especially if there are multiple arguments and characters
separating them may also appear in the given values. For example,
*Select Los Angeles Lakers* in the following example matches
*Select ${city} ${team}* so that `${city}` contains `Los` and
`${team}` contains `Angeles Lakers`:

```robotframework
*** Test Cases ***
Example
    Select Chicago Bulls
    Select Los Angeles Lakers

*** Keywords ***
Select ${city} ${team}
    Log    Selected ${team} from ${city}.
```
An easy solution to this problem is surrounding arguments with double quotes or
other characters not used in the actual values. This fixed example works so
that cities and teams match correctly:

```robotframework
*** Test Cases ***
Example
    Select "Chicago" "Bulls"
    Select "Los Angeles" "Lakers"

*** Keywords ***
Select "${city}" "${team}"
    Log    Selected ${team} from ${city}.
```
This approach is not enough to resolve all conflicts, but it helps in common
cases and is generally recommended. Another benefit is that it makes arguments
stand out from rest of the keyword.

Prior to Robot Framework 7.1, embedded arguments starting the keyword name also
matched possible [given/when/then/and/but prefixes](https://www.python.org/dev/peps/pep-3102) typically used in Behavior
Driven Development (BDD). For example, *${name} goes home* matched
*Given Janne goes home* so that `${name}` got value `Given Janne`.
Nowadays the prefix is ignored and `${name}` will be `Janne` as expected.
If older Robot Framework versions need to be supported, it is easiest to quote
the argument like in *"${name}" goes home* to get consistent behavior.

An alternative solution for limiting what values arguments match is
[using custom regular expressions](#using-custom-regular-expressions).

### Resolving conflicts

When using embedded arguments, it is pretty common that there are multiple
keyword implementations that match the keyword that is used. For example,
*Execute "ls" with "lf"* in the example below matches both of the keywords.
It matching *Execute "${cmd}" with "${opts}"* is pretty obvious and what
we want, but it also matches *Execute "${cmd}"* so that `${cmd}` matches
`ls" with "-lh`.

```robotframework
*** Settings ***
Library          Process

*** Test Cases ***
Automatic conflict resolution
    Execute "ls"
    Execute "ls" with "-lh"

*** Keywords ***
Execute "${cmd}"
    Run Process    ${cmd}    shell=True

Execute "${cmd}" with "${opts}"
    Run Process    ${cmd} ${opts}    shell=True
```
When this kind of conflicts occur, Robot Framework tries to automatically select
the best match and use that. In the above example, *Execute "${cmd}" with "${opts}"*
is considered a better match than the more generic *Execute "${cmd}"* and
running the example thus succeeds without conflicts.

It is not always possible to find a single match that is better than others.
For example, the second test below fails because *Robot Framework* matches
both of the keywords equally well. This kind of conflicts need to be resolved
manually either by renaming keywords or by [using custom regular expressions](#using-custom-regular-expressions).

```robotframework
*** Test Cases ***
No conflict
    Automation framework
    Robot uprising

Unresolvable conflict
    Robot Framework

*** Keywords ***
${type} Framework
    Should Be Equal    ${type}    Automation

Robot ${action}
    Should Be Equal    ${action}    uprising
```
Keywords that accept only "normal" arguments or no arguments at all are
considered to match better than keywords accepting embedded arguments.
For example, if the following keyword is added to the above example,
*Robot Framework* used by the latter test matches it and the test
succeeds:

```robotframework
*** Keywords ***
Robot Framework
    No Operation
```
Before looking which match is best, Robot Framework checks are some of the matching
keywords implemented in the same file as the caller keyword. If there are such keywords,
they are given precedence over other keywords. Alternatively, [library search order](advanced-features.md#library-search-order)
can be used to control the order in which Robot Framework looks for keywords in resources
and libraries.

!!! note
    Automatically resolving conflicts if multiple keywords with embedded
    arguments match is a new feature in Robot Framework 6.0. With older
    versions custom regular expressions explained below can be used instead.

### Using custom regular expressions

When keywords with embedded arguments are called, the values are matched
internally using [regular expressions](https://www.python.org/dev/peps/pep-3102) (regexps for short). The default
logic goes so that every argument in the name is replaced with a pattern `.*?`
that matches any string and tries to match as little as possible. This logic works
fairly well normally, but as discussed above, sometimes keywords
[match wrong values](http://en.wikipedia.org/wiki/Regular_expression) and sometimes there are [conflicts that cannot
be resolved](https://docs.python.org/3/library/re.html#regular-expression-syntax) . A solution in these cases is specifying a custom regular
expression that makes sure that the keyword matches only what it should in that
particular context. To be able to use this feature, and to fully
understand the examples in this section, you need to understand at
least the basics of the regular expression syntax.

A custom embedded argument regular expression is defined after the
base name of the argument so that the argument and the regexp are
separated with a colon. For example, an argument that should match
only numbers can be defined like `${arg:\d+}`.
If needed, custom patterns can be prefixed with [inline flags](http://docs.python.org/library/re.html) such as
`(?i)` for case-insensitivity.

Using custom regular expressions is illustrated by the following examples.
The first one shows how the earlier problem with *Select ${city} ${team}*
not matching *Select Los Angeles Lakers* properly can be resolved without
quoting by implementing the keyword so that `${team}` can only contain non-whitespace
characters.

```robotframework
*** Test Cases ***
Do not match whitespace characters
    Select Chicago Bulls
    Select Los Angeles Lakers

Match numbers and characters from set
    1 + 2 = 3
    53 - 11 = 42

Match either date or literal 'today'
    Deadline is 2022-09-21
    Deadline is today

Case-insensitive match
    Select dog
    Select CAT

*** Keywords ***
Select ${city} ${team:\S+}
    Log    Selected ${team} from ${city}.

${number1:\d+} ${operator:[+-]} ${number2:\d+} = ${expected:\d+}
    ${result} =    Evaluate    ${number1} ${operator} ${number2}
    Should Be Equal As Integers    ${result}    ${expected}

Deadline is ${deadline: date:\d{4}-\d{2}-\d{2}|today}
    # The ': date' part of the above argument specifies the argument type.
    # See the separate section about argument conversion for more information.
    Log    Deadline is ${deadline.day}.${deadline.month}.${deadline.year}.

Select ${animal:(?i)cat|dog}
    [Documentation]    Inline flag `(?i)` makes the pattern case-insensitive.
    Log    Selected ${animal}!
```
!!! note
    Support for inline flags is new in Robot Framework 7.2.

#### Supported regular expression syntax

Being implemented with Python, Robot Framework naturally uses Python's
[re module](https://www.python.org/dev/peps/pep-3102) that has pretty standard regular expressions syntax.
This syntax is otherwise fully supported with embedded arguments, but
regexp extensions in format `(?...)` cannot be used. If the regular
expression syntax is invalid, creating the keyword fails with an error
visible in [test execution errors](http://en.wikipedia.org/wiki/Regular_expression).

#### Escaping special characters

Regular expressions use the backslash character (`\\`) heavily both
to form special sequences (e.g. `\d`) and to escape characters that have
a special meaning in regexps (e.g. `\$`). Typically in Robot Framework data
backslash characters [need to be escaped](https://docs.python.org/3/library/re.html#regular-expression-syntax) with another backslash, but
that is not required in this context. If there is a need to have a literal
backslash in the pattern, then the backslash must be escaped like
`${path:c:\\temp\\.*}`.

Possible lone opening and closing curly braces in the pattern must be escaped
like `${open:\{}` and `${close:\}}` or otherwise Robot Framework is not able
to parse the variable syntax correctly. If there are matching braces like in
`${digits:\d{2}}`, escaping is not needed.

!!! note
    Prior to Robot Framework 3.2, it was mandatory to escape all
    closing curly braces in the pattern like `${digits:\d{2\}}`.
    This syntax is unfortunately not supported by Robot Framework 3.2
    or newer and keywords using it must be updated when upgrading.

!!! note
    Prior to Robot Framework 6.0, using literal backslashes in the pattern
    required double escaping them like `${path:c:\\\\temp\\\\.*}`.
    Patterns using literal backslashes need to be updated when upgrading.

#### Using variables with custom embedded argument regular expressions

When using embedded arguments with custom regular expressions, specifying
values using variables works only if variables match the whole embedded
argument, not if there is any additional content with the variable.
For example, the first test below succeeds because the variable `${DATE}`
is used on its own, but the last test fails because `${YEAR}-${MONTH}-${DAY}`
is not a single variable.

```robotframework
*** Variables ***
${DATE}           2011-06-27
${YEAR}           2011
${MONTH}          06
${DAY}            27

*** Test Cases ***
Succeeds
    Deadline is ${DATE}

Succeeds without variables
    Deadline is 2011-06-27

Fails
    Deadline is ${YEAR}-${MONTH}-${DAY}

*** Keywords ***
Deadline is ${deadline:\d{4}-\d{2}-\d{2}}
    Should Be Equal    ${deadline}    2011-06-27
```
Another limitation of using variables is that their actual values are not matched
against custom regular expressions. As the result keywords may be called with
values that their custom regexps would not allow. This behavior is deprecated
starting from Robot Framework 6.0 and values will be validated in the future.
For more information see issue [#4462](https://www.python.org/dev/peps/pep-3102).

### Argument conversion with embedded arguments

User keywords accepting embedded arguments support argument conversion with type
syntax `${name: type}` similarly as [normal user keywords](http://en.wikipedia.org/wiki/Regular_expression). If a [custom pattern](https://docs.python.org/3/library/re.html#regular-expression-syntax)
is needed, it can be separated with an additional colon like `${name: type:pattern}`.

```robotframework
*** Test Cases ***
Example
    Buy 3 books
    Deadline is 2025-05-30

*** Keywords ***
Buy ${quantity: int} books
    Should Be Equal    ${quantity}    ${3}

Deadline is ${deadline: date:\d{4}-\d{2}-\d{2}}
    Should Be Equal    ${deadline.year}     ${2025}
    Should Be Equal    ${deadline.month}    ${5}
    Should Be Equal    ${deadline.day}      ${30}
```
Because the type separator is a colon followed by a space (e.g. `${arg: int}`)
and the pattern separator is just a colon (e.g. `${arg:\d+}`), there typically
are no conflicts when using only a type or only a pattern. The only exception
is using a pattern starting with a space, but in that case the space can be
escaped like `${arg:\ abc}` or a type added like `${arg: str: abc}`.

!!! note
    Argument conversion with user keywords is new in Robot Framework 7.3.

### Behavior-driven development example

A big benefit of having arguments as part of the keyword name is that it
makes it easier to use higher-level sentence-like keywords when using the
[behavior-driven style](creating-test-cases.md#behavior-driven-style) to write tests. As the example below shows, this
support is typically used in combination with the possibility to
[omit Given, When and Then prefixes](https://www.python.org/dev/peps/pep-3102) in keyword definitions:

```robotframework
*** Test Cases ***
Add two numbers
    Given I have Calculator open
    When I add 2 and 40
    Then result should be 42

Add negative numbers
    Given I have Calculator open
    When I add 1 and -2
    Then result should be -1

*** Keywords ***
I have ${program} open
    Start Program    ${program}

I add ${number 1} and ${number 2}
    Input Number    ${number 1}
    Push Button     +
    Input Number    ${number 2}
    Push Button     =

Result should be ${expected}
    ${result} =    Get Result
    Should Be Equal    ${result}    ${expected}
```
!!! note
    Embedded arguments feature in Robot Framework is inspired by
    how *step definitions* are created in the popular BDD tool [Cucumber](https://www.python.org/dev/peps/pep-3102).

## User keyword return values

Similarly as library keywords, also user keywords can return values.
When using Robot Framework 5.0 or newer, the recommended approach is
using the native [RETURN](#return) statement. The old `[Return]`
setting was deprecated in Robot Framework 7.0 and also [BuiltIn](using-test-libraries.md#builtin) keywords
*Return From Keyword* and *Return From Keyword If* are considered
deprecated.

Regardless how values are returned, they can be [assigned to variables](http://en.wikipedia.org/wiki/Regular_expression)
in test cases and in other user keywords.

<a id="return"></a>
### Using `RETURN` statement

The recommended approach to return values is using the `RETURN` statement.
It accepts optional return values and can be used with [IF](control-structures.md#if) and [inline IF](control-structures.md#inline-if)
structures. Its usage is easiest explained with examples:

```robotframework
*** Keywords ***
Return One Value
    [Arguments]    ${arg}
    [Documentation]    Return a value unconditionally.
    ...                Notice that keywords after RETURN are not executed.
    ${value} =    Convert To Upper Case    ${arg}
    RETURN    ${value}
    Fail    Not executed

Return Three Values
    [Documentation]    Return multiple values.
    RETURN    a    b    c

Conditional Return
    [Arguments]    ${arg}
    [Documentation]    Return conditionally.
    Log    Before
    IF    ${arg} == 1
        Log    Returning!
        RETURN
    END
    Log    After

Find Index
    [Arguments]    ${test}    ${items}
    [Documentation]    Advanced example involving FOR loop, inline IF and @{list} variable syntax.
    FOR    ${index}    ${item}    IN ENUMERATE    @{items}
        IF    $item == $test    RETURN    ${index}
    END
    RETURN    ${-1}
```
If you want to test the above examples yourself, you can use them with these test cases:

```robotframework
*** Settings ***
Library           String

*** Test Cases ***
One return value
    ${ret} =    Return One Value    argument
    Should Be Equal    ${ret}    ARGUMENT

Multiple return values
    ${a}    ${b}    ${c} =    Return Three Values
    Should Be Equal    ${a}, ${b}, ${c}    a, b, c

Conditional return
    Conditional Return    1
    Conditional Return    2

Advanced
    @{list} =    Create List    foo    bar    baz
    ${index} =    Find Index    bar    ${list}
    Should Be Equal    ${index}    ${1}
    ${index} =    Find Index    non existing    ${list}
    Should Be Equal    ${index}    ${-1}
```
!!! note
    `RETURN` syntax is case-sensitive similarly as [IF](control-structures.md#if) and [FOR](control-structures.md#for).

!!! note
    `RETURN` is new in Robot Framework 5.0. Use approaches explained
    below if you need to support older versions.

### Using `[Return]` setting

The `[Return]` setting defines what the keyword should return after
it has been executed. Although it is recommended to have it at the end of keyword
where it logically belongs, its position does not affect how it is used.

An inherent limitation of the `[Return]` setting is that cannot be used
conditionally. Thus only the first two earlier `RETURN` statement examples
can be created using it.

```robotframework
*** Keywords ***
Return One Value
    [Arguments]    ${arg}
    ${value} =    Convert To Upper Case    ${arg}
    [Return]    ${value}

Return Three Values
    [Return]    a    b    c
```
!!! note
    The `[Return]` setting was deprecated in Robot Framework 7.0
    and the `RETURN` statement should be used instead. If there is a need
    to support older Robot Framework versions that do not support `RETURN`,
    it is possible to use the special keywords discussed in the next section.

### Using special keywords to return

[BuiltIn](using-test-libraries.md#builtin) keywords *Return From Keyword* and *Return From Keyword If*
allow returning from a user keyword conditionally in the middle of the keyword.
Both of them also accept optional return values that are handled exactly like
with the `RETURN` statement and the `[Return]` setting discussed above.

The introduction of the `RETURN` statement makes these keywords redundant.
Examples below contain same keywords as earlier `RETURN` examples but these
ones are more verbose:

```robotframework
*** Keywords ***
Return One Value
    [Arguments]    ${arg}
    ${value} =    Convert To Upper Case    ${arg}
    Return From Keyword    ${value}
    Fail    Not executed

Return Three Values
    Return From Keyword        a    b    c

Conditional Return
    [Arguments]    ${arg}
    Log    Before
    IF    ${arg} == 1
        Log    Returning!
        Return From Keyword
    END
    Log    After

Find Index
    [Arguments]    ${test}    ${items}
    FOR    ${index}    ${item}    IN ENUMERATE    @{items}
        Return From Keyword If    $item == $test    ${index}
    END
    Return From Keyword    ${-1}
```
!!! note
    These keywords are effectively deprecated and the `RETURN` statement should be
    used unless there is a need to support also older versions than Robot Framework
    5.0. There is no visible deprecation warning when using these keywords yet, but
    they will be loudly deprecated and eventually removed in the future.

## User keyword setup and teardown

A user keyword can have a setup and a teardown similarly as [tests](https://www.python.org/dev/peps/pep-3102).
They are specified using `[Setup]` and `[Teardown]`
settings, respectively, directly to the keyword having them. Unlike with
tests, it is not possible to specify a common setup or teardown to all
keywords in a certain file.

A setup and a teardown are always a single keyword, but they can themselves be
user keywords executing multiple keywords internally. It is possible to specify
them as variables, and using a special `NONE` value (case-insensitive) is
the same as not having a setup or a teardown at all.

User keyword setup is not much different to the first keyword inside the created
user keyword. The only functional difference is that a setup can be specified as
a variable, but it can also be useful to be able to explicitly mark a keyword
to be a setup.

User keyword teardowns are, exactly as test teardowns, executed also if the user
keyword fails. They are thus very useful when needing to do something at the
end of the keyword regardless of its status. To ensure that all cleanup activities
are done, the [continue on failure](../executing-tests/test-execution.md#continue-on-failure) mode is enabled by default with user keyword
teardowns the same way as with test teardowns.

```robotframework
*** Keywords ***
Setup and teardown
    [Setup]       Log    New in RF 7!
    Do Something
    [Teardown]    Log    Old feature.

Using variables
    [Setup]       ${SETUP}
    Do Something
    [Teardown]    ${TEARDOWN}
```

!!! note
    User keyword setups are new in Robot Framework 7.0.

## Private user keywords

User keywords can be [tagged](https://www.python.org/dev/peps/pep-3102) with a special `robot:private` tag to indicate
that they should only be used in the file where they are created:

```robotframework
*** Keywords ***
Public Keyword
    Private Keyword

Private Keyword
    [Tags]    robot:private
    No Operation
```
Using the `robot:private` tag does not outright prevent using the keyword
outside the file where it is created, but such usages will cause a warning.
If there is both a public and a private keyword with the same name,
the public one will be used but also this situation causes a warning.

Private keywords are included in spec files created by [Libdoc](../supporting-tools/libdoc.md#libdoc) but not in its
HTML output files.

!!! note
    Private user keywords are new in Robot Framework 6.0.

## Recursion

User keywords can call themselves either directly or indirectly. This kind of
recursive usage is fine as long as the recursion ends, typically based on some
condition, before the recursion limit is exceeded. The limit exists because
otherwise infinite recursion would crash the execution.

Robot Framework's recursion detection works so, that it checks is the current
recursion level close to the recursion limit of the underlying Python process.
If it is close enough, no more new started keywords or control structures are
allowed and execution fails.

Python's default recursion limit is 1000 stack frames, which in practice means that
it is possible to start approximately 140 keywords or control structures.
If that is not enough, Python's recursion limit can be raised using the
[sys.setrecursionlimit()](https://www.python.org/dev/peps/pep-3102) function. As the documentation of the function explains,
this should be done with care, because a too-high level can lead to a crash.

!!! note
    Prior to Robot Framework 7.2, the recursion limit was hard-coded to
    100 started keywords or control structures.

