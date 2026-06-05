<a id="rpa"></a>
# Creating tasks

In addition to test automation, Robot Framework can be used for other
automation purposes, including [robotic process automation](https://en.wikipedia.org/wiki/Robotic_process_automation) (RPA).
It has always been possible, but Robot Framework 3.1 added official
support for automating *tasks*, not only tests. For most parts creating
tasks works the same way as [creating tests](creating-test-cases.md#creating-tests) and the only real difference
is in terminology. Tasks can also be organized into [suites](creating-test-suites.md#creating-test-suites) exactly like
test cases.

## Task syntax

Tasks are created based on the available keywords exactly like test cases,
and the task syntax is in general identical to the [test case syntax](creating-test-cases.md#test-case-syntax).
The main difference is that tasks are created in Task sections
instead of Test Case sections:

```robotframework
*** Tasks ***
Process invoice
    Read information from PDF
    Validate information
    Submit information to backend system
    Validate information is visible in web UI
```
It is an error to have both tests and tasks in same file.

## Task related settings

Settings that can be used in the task section are exactly the same as in
the [test case section](https://en.wikipedia.org/wiki/Robotic_process_automation). In the [setting section](variable-files.md#setting-section) it is possible to use
`Task Setup`, `Task Teardown`, `Task Template`
and `Task Timeout` instead of their `Test` variants.

