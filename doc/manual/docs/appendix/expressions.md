# Evaluating expressions

This appendix explains how expressions are evaluated using Python in different
contexts and how variables in expressions are handled.

## Introduction

Constructs such as [IF/ELSE structures](../creating-test-data/control-structures.md#ifelse-structures), [WHILE loops](../creating-test-data/control-structures.md#while-loops) and [inline Python evaluation](../creating-test-data/variables.md#inline-python-evaluation)
as well as several [BuiltIn](../creating-test-data/using-test-libraries.md#builtin) keywords accept an expression that is evaluated in Python:

```robotframework
*** Test Cases ***
IF/ELSE
    IF    ${x} > 0
        Log to console   ${x} is positive
    ELSE
        Log to console   ${x} is negative
    END

Inline Python evaluation
    Log to console    ${x} is ${{'positive' if ${x} > 0 else 'negative'}}

Evaluate keyword
    ${type} =    Evaluate    'positive' if ${x} > 0 else 'negative'
    Log to console    ${x} is ${type}

Should Be True keyword
    Should Be True    ${x} > 0
```
Notice that instead of creating complicated
expressions, it is often better to move the logic into a [test library](../extending/creating-test-libraries.md#creating-test-library-class-or-module).
That typically eases maintenance and also enhances execution speed.

## Evaluation namespace

Expressions are evaluated using Python's [eval](http://docs.python.org/library/functions.html#eval) function so that normal Python
constructs like `'${x}' == 'expected'`, `${x} > 0` and
`'${x}'.upper() not in ('FAIL', 'BAD')` can be used and all
builtin functions like `len()` and `int()` are available.
In addition to that, all unrecognized Python variables are considered to be
modules that are automatically imported. It is possible to use all available
Python modules, including the standard modules and the installed third party
modules.

The following examples demonstrate using Python builtins as well as modules
using the [inline Python evaluation](../creating-test-data/variables.md#inline-python-evaluation) syntax, but same expressions would also
work with [IF/ELSE structures](../creating-test-data/control-structures.md#ifelse-structures) and [BuiltIn](../creating-test-data/using-test-libraries.md#builtin) keywords without the need to use
the `${{}}` decoration around the expression:

```robotframework
*** Variables ***
${VAR}           123

*** Test Cases ***
Python syntax
    Should Be True       ${{'${VAR}' == '123'}}
    Should Be True       ${{'${VAR}'.startswith('x') or '${VAR}' in '012345'}}

Python builtins
    Should Be Equal      ${{len('${VAR}')}}        ${3}
    Should Be Equal      ${{int('${VAR}')}}        ${123}

Access modules
    Should Be Equal      ${{os.sep}}               ${/}
    Should Be Equal      ${{round(math.pi, 2)}}    ${3.14}
    Should Start With    ${{robot.__version__}}    4.
```
A limitation of using modules is that nested modules like `rootmod.submod`
can only be used if the root module automatically imports the submodule. That is
not always the case and using such modules is not possible. An concrete example
that is relevant in the automation context is the `selenium` module that is
implemented, at least at the time of this writing, so that just importing
`selenium` does not import the `selenium.webdriver` submodule.
Another limitation is that modules cannot be used in the expression part of
a list comprehension. A workaround to both of these problems
is using the [BuiltIn](../creating-test-data/using-test-libraries.md#builtin) keyword *Evaluate* that accepts modules to be imported
and added to the evaluation namespace as an argument:

```robotframework
*** Test Cases ***
Does not work due to nested module structure
    Log    ${{selenium.webdriver.ChromeOptions()}}

Evaluate keyword with nested module
    ${options} =    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    Log    ${options}

Does not work due to list comprehension
    Log    ${{[json.loads(item) for item in ('1', '"b"')]}}

Evaluate keyword with list comprehension
    ${items} =    Evaluate    [json.loads(item) for item in ('1', '"b"')]    modules=json
    Log    ${items}
```
The *Evaluate* keyword also supports custom evaluation namespaces if further
customization is needed. See its documentation in the [BuiltIn](../creating-test-data/using-test-libraries.md#builtin) library for more details.

## Using variables

### Normal `${variable}` syntax

When a variable is used in the expression using the normal `${variable}`
syntax, its value is replaced before the expression is evaluated. This
means that the value used in the expression will be the string
representation of the variable value, not the variable value itself.
This is not a problem with numbers and other objects that have a string
representation that can be evaluated directly. For example, if we have
a return code as an integer in variable `${rc}`, using something like
`${rc} > 0` is fine.

With other objects the behavior depends on the string representation.
Most importantly, strings must always be quoted either with
single or double quotes like `'${x}'`, and if they can contain newlines, they must be
triple-quoted like `'''${x}'''`. Strings containing quotes themselves cause
additional problems, but triple-quoting typically handles them. Also the
backslash character `\\` is problematic, but can be handled by
using Python's raw-string notation like `r'${path}'`.

```robotframework
*** Test Cases ***
Using normal variable syntax
    Should Be True    ${rc} > 0
    IF    '${status}'.upper() == 'PASS'
        Log    Passed
    END
    IF    'FAIL' in r'''${output}'''
        Log    Output contains FAIL
    END
```
### Special `$variable` syntax

Quoting strings is not that convenient, but there are cases where replacing the variable
with its string representation causes even bigger problems. For example, if the variable
value can be either a string or Python `None`, quoting like `'${var}'` is needed because
otherwise strings do not work, but then `None` is interpreted to be a string as well.
Luckily there is an easy solution to these problems discussed in this section.

Actual variables values are available in the evaluation namespace and can be accessed
using special variable syntax without the curly braces like `$variable`. Such variables
should never be quoted, not even if they contain strings.

Compare this these examples with the example in the previous section:

```robotframework
*** Test Cases ***
Using special variable syntax
    Should Be True    $rc > 0
    IF    $status.upper() == 'PASS'
        Log    Passed
    END
    IF    'FAIL' in $output
        Log    Output contains FAIL
    END

Only possible using special variable syntax
    Should Be True    $example is not None
    Should Be True    len($result) > 1 and $result[1] == 'OK'
```
Using the `$variable` syntax slows down expression evaluation a little.
This should not typically matter, but should be taken into account if
complex expressions are evaluated often and there are strict time
constrains. Moving such logic to test libraries is typically a good idea
anyway.

!!! note
    Due to technical reasons, these special variables are available during
    evaluation as local variables. That makes them unavailable in non-local
    scopes such as in the expression part of list comprehensions and inside
    lambdas.

