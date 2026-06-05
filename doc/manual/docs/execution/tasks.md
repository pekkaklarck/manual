<a id="executing-tasks"></a>
# Task execution

Robot Framework can be used also for other automation purposes than test
automation, and starting from Robot Framework 3.1 it is possible to
explicitly [create](#create) and execute tasks. For most parts task execution
and test execution work the same way, and this section explains the
differences.

## Generic automation mode

When Robot Framework is used execute a file and it notices that the file
has tasks, not tests, it automatically sets itself into the generic automation
mode. This mode does not change the actual execution at all, but when
logs and reports are created, they use term *task*, not *test*. They have,
for example, headers like `Task Log` and `Task Statistics` instead of
`Test Log` and `Test Statistics`.

The generic automation mode can also be enabled by using the `--rpa`
option. In that case the executed files can have either tests or tasks.
Alternatively `--norpa` can be used to force the test automation
mode even if executed files contain tasks. If neither of these options are
used, it is an error to execute multiple files so that some have tests and
others have tasks.

The execution mode is stored in the generated [output file](result-files.md#output-file) and read by
[Rebot](post-processing.md#rebot) if outputs are post-processed. The mode can also [be set when
using Rebot](../creating-test-data/creating-tasks.md#creating-tasks) if necessary.

## Task related command line options

All normal command line options can be used when executing tasks. If there
is a need to [select only certain tasks for execution](post-processing.md#controlling-execution-mode), `--task`
can be used instead of `--test`. Additionally the aforementioned
`--rpa` can be used to control the execution mode.

