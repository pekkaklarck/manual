# Command line options

This appendix lists all the command line options that are available
when [executing test cases](../executing-tests/basic-usage.md#executing-test-cases)  and when [post-processing outputs](../executing-tests/post-processing.md#post-processing-outputs).
Also environment variables affecting execution and post-processing
are listed.

## Command line options for test execution

  --rpa                   Turn on [generic automation](../executing-tests/task-execution.md#generic-automation-mode) mode.
  --language <lang>       Activate [localization](../creating-test-data/test-data-syntax.md#localization). `lang` can be a name or a code
                          of a [built-in language](translations.md#translations)_, or a path
                          or a module name of a custom language file.
  -F, --extension <value>  [Parse only these files](#parse-only-these-files) when executing a directory.
  -I, --parseinclude <pattern>  [Parse only matching files](#parse-only-matching-files) when executing a directory.
  -N, --name <name>       [Sets the name](#sets-the-name) of the top-level test suite.
  -D, --doc <document>    [Sets the documentation](#sets-the-documentation) of the top-level test suite.
  -M, --metadata <name:value>  [Sets free metadata](#sets-free-metadata) for the top level test suite.
  -G, --settag <tag>      [Sets the tag(s)](../creating-test-data/creating-test-cases.md#tag) to all executed test cases.
  -t, --test <name>       [Selects the test cases by name](../creating-test-data/creating-test-cases.md#test-case).
  --task <name>           Alias for `--test` that can be used when [executing tasks](../executing-tests/task-execution.md#executing-tasks).
  -s, --suite <name>      [Selects the test suites](../creating-test-data/creating-test-suites.md#test-suite) by name.
  -R, --rerunfailed <file>  [Selects failed tests](../executing-tests/test-execution.md#fail) from an earlier [output file](../executing-tests/result-files.md#output-file)
                          to be re-executed.
  -S, --rerunfailedsuites <file>  [Selects failed test suites](../executing-tests/test-execution.md#fail) from an earlier
                          [output file](../executing-tests/result-files.md#output-file) to be re-executed.
  -i, --include <tag>     [Selects the test cases](../creating-test-data/creating-test-cases.md#test-case) by tag.
  -e, --exclude <tag>     [Selects the test cases](../creating-test-data/creating-test-cases.md#test-case) by tag.
  --skip <tag>            Tests having given tag will be [skipped](../executing-tests/test-execution.md#skipped). Tag can be a pattern.
  --skiponfailure <tag>   Tests having given tag will be [skipped](../executing-tests/test-execution.md#skipped) if they fail.
  -v, --variable <name:value>   Sets [individual variables](../creating-test-data/variables.md#variable).
  -V, --variablefile <path:args>  Sets variables using [variable files](../creating-test-data/variable-files.md#variable-files).
  -d, --outputdir <dir>   Defines where to [create result files](../executing-tests/result-files.md#result-file).
  -o, --output <file>     Sets the path to the generated [output file](../executing-tests/result-files.md#output-file).
  --legacyoutput          Creates output file in [Robot Framework 6.x compatible format](../creating-test-data/control-structures.md#for).
  -l, --log <file>        Sets the path to the generated [log file](../executing-tests/result-files.md#log-file).
  -r, --report <file>     Sets the path to the generated [report file](../executing-tests/result-files.md#report-file).
  -x, --xunit <file>      Sets the path to the generated [xUnit compatible result file](../executing-tests/result-files.md#xunit-compatible-result-file).
  -b, --debugfile <file>  A [debug file](../executing-tests/result-files.md#debug-file) that is written during execution.
  -T, --timestampoutputs  [Adds a timestamp](#adds-a-timestamp) to [result files](../executing-tests/result-files.md#result-files) listed above.
  --splitlog              [Split log file](../executing-tests/result-files.md#log) into smaller pieces that open in
                          browser transparently.
  --logtitle <title>      [Sets a title](#sets-a-title) for the generated test log.
  --reporttitle <title>   [Sets a title](#sets-a-title) for the generated test report.
  --reportbackground <colors>  [Sets background colors](#sets-background-colors) of the generated report.
  --maxerrorlines <lines>  Sets the number of [error lines](#error-lines) shown in report when tests fail.
  --maxassignlength <characters>  Sets the number of characters shown in log when
                           [variables are assigned](../creating-test-data/variables.md#automatically-logging-assigned-variable-value)_.
  -L, --loglevel <level>  [Sets the threshold level](#sets-the-threshold-level) for logging. Optionally
                          the default [visible log level](../executing-tests/result-files.md#visible-log-level) can be given
                          separated with a colon (:).
  --suitestatlevel <level>  Defines how many [levels to show](#levels-to-show) in the
                           *Statistics by Suite* table in outputs.
  --tagstatinclude <tag>  [Includes only these tags](../creating-test-data/creating-test-cases.md#tag) in the *Statistics by Tag* table.
  --tagstatexclude <tag>  [Excludes these tags](../creating-test-data/creating-test-cases.md#tag) from the *Statistics by Tag* table.
  --tagstatcombine <tags:title>  Creates [combined statistics based on tags](../creating-test-data/creating-test-cases.md#tag).
  --tagdoc <pattern:doc>  Adds [documentation to the specified tags](../creating-test-data/control-structures.md#if).
  --tagstatlink <pattern:link:title>  Adds [external links](#external-links) to the *Statistics by Tag* table.
  --expandkeywords <name:pattern|tag:pattern>  Automatically [expand keywords](#expand-keywords)
                          in the generated log file.
  --removekeywords <all|passed|name:pattern|tag:pattern|for|while|wuks>  [Removes keyword data](#removes-keyword-data)
                          from the generated log file.
  --flattenkeywords <for|while|iteration|name:pattern|tag:pattern>  [Flattens keywords](../executing-tests/output-files.md#flattening-keywords)
                          in the generated log file.
  --listener <name:args>  [Sets a listener](../extending/listener-interface.md#listener) for monitoring test execution.
  --nostatusrc            Sets the [return code](../executing-tests/basic-usage.md#return-code) to zero regardless of failures
                          in test cases. Error codes are returned normally.
  --runemptysuite         Executes tests also if the selected [test suites are empty](../creating-test-data/creating-test-suites.md#test-suite).
  --dryrun                In the [dry run](../executing-tests/configuring-execution.md#dry-run) mode tests are run without executing
                          keywords originating from test libraries. Useful for
                          validating test data syntax.
  -X, --exitonfailure     [Stops test execution](../executing-tests/test-execution.md#stopping-when-first-test-case-fails)_
                          if any test fails.
  --exitonerror           [Stops test execution](../executing-tests/test-execution.md#stopping-on-parsing-or-execution-error)_
                          if any error occurs when parsing test data, importing libraries, and so on.
  --skipteardownonexit    [Skips teardowns](../executing-tests/test-execution.md#skip) if test execution is prematurely stopped.
  --prerunmodifier <name:args>    Activate [programmatic modification of test data](../executing-tests/configuring-execution.md#programmatic-modification-of-test-data).
  --prerebotmodifier <name:args>  Activate [programmatic modification of results](../executing-tests/result-files.md#programmatic-modification-of-results).
  --randomize <all|suites|tests|none>  [Randomizes](#randomizes) test execution order.
  --console <verbose|dotted|quiet|none>  [Console output type](../executing-tests/configuring-execution.md#console-output-type).
  --dotted                Shortcut for `--console dotted`.
  --quiet                 Shortcut for `--console quiet`.
  -W, --consolewidth <width>  [Sets the width](#sets-the-width) of the console output.
  -C, --consolecolors <auto|on|ansi|off>  [Specifies are colors](../creating-test-data/control-structures.md#if) used on the console.
  --consolelinks <auto|off>  Controls [making paths to results files hyperlinks](../executing-tests/configuring-execution.md#console-links).
  -K, --consolemarkers <auto|on|off>  Show [markers on the console](#markers-on-the-console) when top level
                                      keywords in a test case end.
  -P, --pythonpath <path>  Additional locations to add to the [module search path](../executing-tests/configuring-execution.md#module-search-path).
  -A, --argumentfile <path>   A text file to [read more arguments](#read-more-arguments) from.
  -h, --help              Prints [usage instructions](../index.md#usage-instructions).
  --version               Prints the [version information](../index.md#version-information).

## Command line options for post-processing outputs

  --rpa                   Turn on [generic automation](../executing-tests/task-execution.md#generic-automation-mode) mode.
  -R, --merge             Changes result combining behavior to [merging](../executing-tests/post-processing.md#merging-results)_.
  -N, --name <name>       [Sets the name](#sets-the-name) of the top level test suite.
  -D, --doc <document>    [Sets the documentation](#sets-the-documentation) of the top-level test suite.
  -M, --metadata <name:value>  [Sets free metadata](#sets-free-metadata) for the top-level test suite.
  -G, --settag <tag>      [Sets the tag(s)](../creating-test-data/creating-test-cases.md#tag) to all processed test cases.
  -t, --test <name>       [Selects the test cases by name](../creating-test-data/creating-test-cases.md#test-case).
  --task <name>           Alias for `--test`.
  -s, --suite <name>      [Selects the test suites](../creating-test-data/creating-test-suites.md#test-suite) by name.
  -i, --include <tag>     [Selects the test cases](../creating-test-data/creating-test-cases.md#test-case) by tag.
  -e, --exclude <tag>     [Selects the test cases](../creating-test-data/creating-test-cases.md#test-case) by tag.
  -d, --outputdir <dir>   Defines where to [create result files](../executing-tests/result-files.md#result-file).
  -o, --output <file>     Sets the path to the generated [output file](../executing-tests/result-files.md#output-file).
  --legacyoutput          Creates output file in [Robot Framework 6.x compatible format](../creating-test-data/control-structures.md#for).
  -l, --log <file>        Sets the path to the generated [log file](../executing-tests/result-files.md#log-file).
  -r, --report <file>     Sets the path to the generated [report file](../executing-tests/result-files.md#report-file).
  -x, --xunit <file>      Sets the path to the generated [xUnit compatible result file](../executing-tests/result-files.md#xunit-compatible-result-file).
  -T, --timestampoutputs  [Adds a timestamp](#adds-a-timestamp) to [result files](../executing-tests/result-files.md#result-files) listed above.
  --splitlog              [Split log file](../executing-tests/result-files.md#log) into smaller pieces that open in
                          browser transparently.
  --logtitle <title>      [Sets a title](#sets-a-title) for the generated test log.
  --reporttitle <title>   [Sets a title](#sets-a-title) for the generated test report.
  --reportbackground <colors>  [Sets background colors](#sets-background-colors) of the generated report.
  -L, --loglevel <level>  [Sets the threshold level](#sets-the-threshold-level) to select log messages.
                          Optionally the default [visible log level](../executing-tests/result-files.md#visible-log-level) can be given
                          separated with a colon (:).
  --suitestatlevel <level>  Defines how many [levels to show](#levels-to-show) in the
                           *Statistics by Suite* table in outputs.
  --tagstatinclude <tag>  [Includes only these tags](../creating-test-data/creating-test-cases.md#tag) in the *Statistics by Tag* table.
  --tagstatexclude <tag>  [Excludes these tags](../creating-test-data/creating-test-cases.md#tag) from the *Statistics by Tag* table.
  --tagstatcombine <tags:title>  Creates [combined statistics based on tags](../creating-test-data/creating-test-cases.md#tag).
  --tagdoc <pattern:doc>  Adds [documentation to the specified tags](../creating-test-data/control-structures.md#if).
  --tagstatlink <pattern:link:title>  Adds [external links](#external-links) to the *Statistics by Tag* table.
  --expandkeywords <name:pattern|tag:pattern>  Automatically [expand keywords](#expand-keywords)
                          in the generated log file.
  --removekeywords <all|passed|name:pattern|tag:pattern|for|wuks>  [Removes keyword data](#removes-keyword-data)
                          from the generated outputs.
  --flattenkeywords <for|foritem|name:pattern|tag:pattern>  [Flattens keywords](../executing-tests/output-files.md#flattening-keywords)
                          in the generated outputs.
  --starttime <timestamp>  Sets the [starting time](#starting-time) of test execution when creating
                          reports.
  --endtime <timestamp>   Sets the [ending time](#command-line-options) of test execution when creating reports.
  --nostatusrc            Sets the [return code](../executing-tests/basic-usage.md#return-code) to zero regardless of failures
                          in test cases. Error codes are returned normally.
  --processemptysuite     Processes output files even if files contain
                          [empty test suites](../creating-test-data/creating-test-suites.md#test-suite).
  --prerebotmodifier <name:args>  Activate [programmatic modification of results](../executing-tests/result-files.md#programmatic-modification-of-results).
  -C, --consolecolors <auto|on|ansi|off>  [Specifies are colors](../creating-test-data/control-structures.md#if) used on the console.
  --consolelinks <auto|off>  Controls [making paths to results files hyperlinks](../executing-tests/configuring-execution.md#console-links).
  -P, --pythonpath <path>   Additional locations to add to the [module search path](../executing-tests/configuring-execution.md#module-search-path).
  -A, --argumentfile <path>   A text file to [read more arguments](#read-more-arguments) from.
  -h, --help              Prints [usage instructions](../index.md#usage-instructions).
  --version               Prints the [version information](../index.md#version-information).






## Environment variables for execution and post-processing

`ROBOT_OPTIONS` and `REBOT_OPTIONS`
: Space separated list of default options to be placed
    [in front of any explicit options](../supporting-tools/libdoc.md#options) on the command line.

`ROBOT_SYSLOG_FILE`
: Path to a [syslog](../executing-tests/result-files.md#syslog) file where Robot Framework writes internal
    information about parsing test case files and running
    tests.

`ROBOT_SYSLOG_LEVEL`
: Log level to use when writing to the [syslog](../executing-tests/result-files.md#syslog) file.

`ROBOT_INTERNAL_TRACES`
: When set to any non-empty value, Robot Framework's
    internal methods are included in [error tracebacks](../extending/creating-test-libraries.md#tracebacks).

