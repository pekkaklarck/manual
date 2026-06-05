<a id="rebot"></a>

<a id="post-process-outputs"></a>
# Post-processing outputs

[XML output files](output-files.md#xml-output-files) that are generated during the test execution can be
post-processed afterwards by the Rebot tool, which is an integral
part of Robot Framework. It is used automatically when test
reports and logs are generated during the test execution, and using it
separately allows creating custom reports and logs as well as combining
and merging results.


<a id="rebot"></a>
<a id="Post-processingoutputs"></a>
<a id="post-process outputs"></a>
## Using Rebot

### Synopsis

```
rebot [options] outputs
python -m robot.rebot [options] outputs
python path/to/robot/rebot.py [options] outputs
```

The most common way to use Rebot is using the `rebot` command.
Alternatively it is possible to execute the installed `robot.rebot`
module or the `robot/rebot.py` file using the selected Python
interpreter.

### Specifying options and arguments

The basic syntax for using Rebot is exactly the same as when
[starting test execution](basic-usage.md#starting-test-execution) and also most of the command line options are
identical. The main difference is that arguments to Rebot are
[XML output files](output-files.md#xml-output-files) instead of test data files or directories.

### Return codes with Rebot

Return codes from Rebot are exactly same as when [running tests](basic-usage.md#return-codes).

### Controlling execution mode

Rebot notices have [tests](../creating-test-data/creating-test-cases.md#example-tests) or [tasks](../creating-test-data/creating-tasks.md#creating-tasks) been run, and by default preserves the
execution mode. The mode affects logs and reports so that in the former case
they will use term *test* like `Test Log` and `Test Statistics`, and in
the latter case term *task* like `Task Log` and `Task Statistics`.

Rebot also supports using `--rpa` or `--norpa` options to set
the execution mode explicitly. This is necessary if multiple output files
are processed and they have conflicting modes.

## Creating reports, logs and output files

You can use Rebot for creating the same reports and logs that
are created automatically during the test execution. Of course, it is
not sensible to create the exactly same files, but, for example,
having one report with all test cases and another with only some
subset of tests can be useful:

```
rebot output.xml
rebot path/to/output_file.xml
rebot --include smoke --name Smoke_Tests c:\results\output.xml
```

Another common usage is creating only the output file when running tests
(log and report generation can be disabled with  `--log NONE
--report NONE`) and generating logs and reports later. Tests can,
for example, be executed on different environments, output files collected
to a central place, and reports and logs created there.

Rebot does not create XML output files by default, but it is possible to
create them by using the `--output (-o)` option. Log and report
are created by default, but they can be disabled by using value `NONE`
(case-insensitive) if they are not needed:

```
rebot --include smoke --output smoke.xml --log none --report none original.xml
```

## Combining results

An important feature in Rebot is its ability to combine
results from different execution rounds. This capability allows,
for example, running the same test cases on different environments and
generating an overall report from all outputs. Combining results is
extremely easy, all that needs to be done is giving several output
files as arguments:

```
rebot output1.xml output2.xml
rebot outputs/*.xml
```

When results are combined, a new top-level test suite is created so
that test suites in the given output files are its child suites. This
works the same way when [multiple test data files or directories are
executed](test-execution.md#test-execution), and also in this case the name of the top-level test
suite is created by joining child suite names with an ampersand (&)
and spaces. These automatically generated names are not that good, and
it is often a good idea to use `--name` to give a more
meaningful name:

```
rebot --name "Browser Compatibility" firefox.xml opera.xml safari.xml ie.xml
rebot --include smoke --name Smoke c:\results\*.xml
```

## Merging results

If same tests are re-executed or a single test suite executed in pieces,
combining results like discussed above creates an unnecessary top-level
test suite. In these cases it is typically better to merge results instead.
Merging is done by using `--merge (-R)` option which changes the way how
Rebot combines two or more output files. This option itself takes no
arguments and all other command line options can be used with it normally:

```
rebot --merge original.xml merged.xml
rebot --merge --name Example first.xml second.xml third.xml
```

When suites are merged, documentation, suite setup and suite teardown are got
from the last merged suite. Suite metadata from all merged suites is preserved
so that values in latter suites have precedence.

How merging tests works is explained in the following sections discussing
the two main merge use cases.

!!! note
    Getting suite documentation and metadata from merged suites is new in
    Robot Framework 6.0.

### Merging re-executed tests

There is often a need to re-execute a subset of tests, for example, after
fixing a bug in the system under test or in the tests themselves. This can be
accomplished by [selecting test cases](configuring-execution.md#selecting-test-cases) by names (`--test` and
`--suite` options), tags (`--include` and `--exclude`),
or by previous status (`--rerunfailed` or `--rerunfailedsuites`).

Combining re-execution results with the original results using the default
[combining results](#combining-results) approach does not work too well. The main problem is
that you get separate test suites and possibly already fixed failures are
also shown. In this situation it is better to use `--merge (-R)`
option to tell Rebot to merge the results instead. In practice this
means that tests from the latter test runs replace tests in the original.
An exception to this rule is that [skipped](test-execution.md#skipped) tests in latter runs are ignored
and original tests preserved.

This usage is best illustrated by a practical example using
`--rerunfailed` and `--merge` together:

```
robot --output original.xml tests                          # first execute all tests
robot --rerunfailed original.xml --output rerun.xml tests  # then re-execute failing
rebot --merge original.xml rerun.xml                       # finally merge results
```

The message of the merged tests contains a note that results have been
replaced. The message also shows the old status and message of the test.

Merged results must always have same top-level test suite. Tests and suites
in merged outputs that are not found from the original output are added into
the resulting output. How this works in practice is discussed in the next
section.

!!! note
    Ignoring skipped tests in latter runs is new in Robot Framework 4.1.

### Merging suites executed in pieces

Another important use case for the `--merge` option is merging results
got when running a test suite in pieces using, for example, `--include`
and `--exclude` options:

```
robot --include smoke --output smoke.xml tests   # first run some tests
robot --exclude smoke --output others.xml tests  # then run others
rebot --merge smoke.xml others.xml               # finally merge results
```

When merging outputs like this, the resulting output contains all tests and
suites found from all given output files. If some test is found from multiple
outputs, latest results replace the earlier ones like explained in the previous
section. Also this merging strategy requires the top-level test suites to
be same in all outputs.

## JSON output files

Rebot can create and process output files also in the [JSON](../creating-test-data/test-data-syntax.md#json-structure) format.
Creating JSON output files is done using the normal `--output` option
so that the specified file has a *.json* extension:

```
rebot --output output.json output.xml
```

When reading output files, JSON files are automatically recognized by
the extension:

```
rebot output.json
rebot output1.json output2.json
```

When combining or merging results, it is possible to mix JSON and XML output files:

```
rebot output1.xml output2.json
rebot --merge original.xml rerun.json
```

The JSON output file structure is documented in the *result.json* [schema file](https://github.com/robotframework/robotframework/tree/master/doc/schema#readme).

!!! note
    Support for JSON output files is new in Robot Framework 7.0.
    Prior to Robot Framework 7.2 JSON output files contained only
    information about the executed suite, but nowadays they contain
    the same result data as [XML output files](output-files.md#xml-output-files).

