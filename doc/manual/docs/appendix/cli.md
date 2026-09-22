# Command line options

This appendix lists all the command line options that are available
when [executing test cases](../execution/basics.md#executing-test-cases)  and when [post-processing outputs](../execution/post-processing.md#post-processing-outputs).
Also environment variables affecting execution and post-processing
are listed.

## Command line options for test execution

`--rpa`{.option}
:   Turn on [generic automation](../execution/tasks.md#task-execution) mode.

`--language <lang>`{.option}
:   Activate [localization](../syntax/data.md#localization). `lang` can be a name or a code of a [built-in language](translations.md#translations), or a path or a module name of a custom language file.

`-F, --extension <value>`{.option}
:   [Parse only these files](../execution/configuration.md#selecting-files-to-parse) when executing a directory.

`-I, --parseinclude <pattern>`{.option}
:   [Parse only matching files](../execution/configuration.md#selecting-files-to-parse) when executing a directory.

`-N, --name <name>`{.option}
:   [Sets the name](../execution/configuration.md#setting-suite-name) of the top-level test suite.

`-D, --doc <document>`{.option}
:   [Sets the documentation](../execution/configuration.md#setting-suite-documentation) of the top-level test suite.

`-M, --metadata <name:value>`{.option}
:   [Sets free metadata](../execution/configuration.md#setting-free-suite-metadata) for the top level test suite.

`-G, --settag <tag>`{.option}
:   [Sets the tag(s)](../execution/configuration.md#setting-test-tags) to all executed test cases.

`-t, --test <name>`{.option}
:   [Selects the test cases by name](../execution/configuration.md#by-test-names).

`--task <name>`{.option}
:   Alias for `--test`{.option} that can be used when [executing tasks](../execution/tasks.md#executing-tasks).

`-s, --suite <name>`{.option}
:   [Selects the test suites](../execution/configuration.md#by-suite-names) by name.

`-R, --rerunfailed <file>`{.option}
:   [Selects failed tests](../execution/configuration.md#re-executing-failed-test-cases) from an earlier [output file](../execution/results.md#output-file) to be re-executed.

`-S, --rerunfailedsuites <file>`{.option}
:   [Selects failed test suites](../execution/configuration.md#re-executing-failed-test-suites) from an earlier [output file](../execution/results.md#output-file) to be re-executed.

`-i, --include <tag>`{.option}
:   [Selects the test cases](../execution/configuration.md#by-tag-names) by tag.

`-e, --exclude <tag>`{.option}
:   [Selects the test cases](../execution/configuration.md#by-tag-names) by tag.

`--skip <tag>`{.option}
:   Tests having given tag will be [skipped](../execution/tests.md#skipped). Tag can be a pattern.

`--skiponfailure <tag>`{.option}
:   Tests having given tag will be [skipped](../execution/tests.md#skipped) if they fail.

`-v, --variable <name:value>`{.option}
:   Sets [individual variables](../syntax/variables.md#command-line-variables).

`-V, --variablefile <path:args>`{.option}
:   Sets variables using [variable files](../syntax/variable-files.md#variable-files).

`-d, --outputdir <dir>`{.option}
:   Defines where to [create result files](../execution/results.md#output-directory).

`-o, --output <file>`{.option}
:   Sets the path to the generated [output file](../execution/results.md#output-file).

`--legacyoutput`{.option}
:   Creates output file in [Robot Framework 6.x compatible format](../execution/results.md#legacy-xml-format).

`-l, --log <file>`{.option}
:   Sets the path to the generated [log file](../execution/results.md#log-file).

`-r, --report <file>`{.option}
:   Sets the path to the generated [report file](../execution/results.md#report-file).

`-x, --xunit <file>`{.option}
:   Sets the path to the generated [xUnit compatible result file](../execution/results.md#xunit-compatible-result-file).

`-b, --debugfile <file>`{.option}
:   A [debug file](../execution/results.md#debug-file) that is written during execution.

`-T, --timestampoutputs`{.option}
:   [Adds a timestamp](../execution/results.md#timestamping-result-files) to [result files](../execution/results.md#result-files) listed above.

`--splitlog`{.option}
:   [Split log file](../execution/results.md#splitting-logs) into smaller pieces that open in browser transparently.

`--logtitle <title>`{.option}
:   [Sets a title](../execution/results.md#setting-titles) for the generated test log.

`--reporttitle <title>`{.option}
:   [Sets a title](../execution/results.md#setting-titles) for the generated test report.

`--reportbackground <colors>`{.option}
:   [Sets background colors](../execution/results.md#setting-background-colors) of the generated report.

`--maxerrorlines <lines>`{.option}
:   Sets the number of [error lines](../execution/results.md#limiting-error-message-length-in-reports) shown in report when tests fail.

`--maxassignlength <characters>`{.option}
:   Sets the number of characters shown in log when [variables are assigned](../syntax/variables.md#automatically-logging-assigned-variable-value).

`-L, --loglevel <level>`{.option}
:   [Sets the threshold level](../execution/results.md#setting-log-level) for logging. Optionally the default [visible log level](../execution/results.md#visible-log-level) can be given separated with a colon (:).

`--suitestatlevel <level>`{.option}
:   Defines how many [levels to show](../execution/results.md#configuring-displayed-suite-statistics) in the *Statistics by Suite* table in outputs.

`--tagstatinclude <tag>`{.option}
:   [Includes only these tags](../execution/results.md#including-and-excluding-tag-statistics) in the *Statistics by Tag* table.

`--tagstatexclude <tag>`{.option}
:   [Excludes these tags](../execution/results.md#including-and-excluding-tag-statistics) from the *Statistics by Tag* table.

`--tagstatcombine <tags:title>`{.option}
:   Creates [combined statistics based on tags](../execution/results.md#generating-combined-tag-statistics).

`--tagdoc <pattern:doc>`{.option}
:   Adds [documentation to the specified tags](../execution/results.md#adding-documentation-to-tags).

`--tagstatlink <pattern:link:title>`{.option}
:   Adds [external links](../execution/results.md#creating-links-from-tag-names) to the *Statistics by Tag* table.

`--expandkeywords <name:pattern|tag:pattern>`{.option}
:   Automatically [expand keywords](../execution/results.md#automatically-expanding-keywords) in the generated log file.

`--removekeywords <all|passed|name:pattern|tag:pattern|for|while|wuks>`{.option}
:   [Removes keyword data](../execution/results.md#removing-and-flattening-keywords) from the generated log file.

`--flattenkeywords <for|while|iteration|name:pattern|tag:pattern>`{.option}
:   [Flattens keywords](../execution/results.md#removing-and-flattening-keywords) in the generated log file.

`--listener <name:args>`{.option}
:   [Sets a listener](../execution/configuration.md#setting-listeners) for monitoring test execution.

`--nostatusrc`{.option}
:   Sets the [return code](../execution/basics.md#return-codes) to zero regardless of failures in test cases. Error codes are returned normally.

`--runemptysuite`{.option}
:   Executes tests also if the selected [test suites are empty](../execution/configuration.md#when-no-tests-match-selection).

`--dryrun`{.option}
:   In the [dry run](../execution/configuration.md#dry-run) mode tests are run without executing keywords originating from test libraries. Useful for validating test data syntax.

`-X, --exitonfailure`{.option}
:   [Stops test execution](../execution/tests.md#stopping-when-first-test-case-fails) if any test fails.

`--exitonerror`{.option}
:   [Stops test execution](../execution/tests.md#stopping-on-parsing-or-execution-error) if any error occurs when parsing test data, importing libraries, and so on.

`--skipteardownonexit`{.option}
:   [Skips teardowns](../execution/tests.md#handling-teardowns) if test execution is prematurely stopped.

`--prerunmodifier <name:args>`{.option}
:   Activate [programmatic modification of test data](../execution/configuration.md#programmatic-modification-of-test-data).

`--prerebotmodifier <name:args>`{.option}
:   Activate [programmatic modification of results](../execution/results.md#programmatic-modification-of-results).

`--randomize <all|suites|tests|none>`{.option}
:   [Randomizes](../execution/configuration.md#randomizing-execution-order) test execution order.

`--console <verbose|dotted|quiet|none|custom>`{.option}
:   [Console output type](../execution/configuration.md#built-in-console-loggers). Also accepts [custom console loggers](../execution/configuration.md#custom-console-loggers).

`--dotted`{.option}
:   Shortcut for `--console dotted`.

`--quiet`{.option}
:   Shortcut for `--console quiet`.

`-W, --consolewidth <width>`{.option}
:   [Sets the width](../execution/configuration.md#console-width) of the console output.

`-C, --consolecolors <auto|on|ansi|off>`{.option}
:   [Specifies are colors](../execution/configuration.md#console-colors) used on the console.

`--consolelinks <auto|off>`{.option}
:   Controls [making paths to results files hyperlinks](../execution/configuration.md#console-links).

`-K, --consolemarkers <auto|on|off>`{.option}
:   Show [markers on the console](../execution/configuration.md#console-markers) when top level keywords in a test case end.

`-P, --pythonpath <path>`{.option}
:   Additional locations to add to the [module search path](../execution/configuration.md#module-search-path).

`-A, --argumentfile <path>`{.option}
:   A text file to [read more arguments](../execution/basics.md#argument-files) from.

`-h, --help`{.option}
:   Prints [usage instructions](../execution/basics.md#getting-help-and-version-information).

`--version`{.option}
:   Prints the [version information](../execution/basics.md#getting-help-and-version-information).

## Command line options for post-processing outputs

`--rpa`{.option}
:   Turn on [generic automation](../execution/tasks.md#task-execution) mode.

`-R, --merge`{.option}
:   Changes result combining behavior to [merging](../execution/post-processing.md#merging-results).

`-N, --name <name>`{.option}
:   [Sets the name](../execution/configuration.md#setting-suite-name) of the top level test suite.

`-D, --doc <document>`{.option}
:   [Sets the documentation](../execution/configuration.md#setting-suite-documentation) of the top-level test suite.

`-M, --metadata <name:value>`{.option}
:   [Sets free metadata](../execution/configuration.md#setting-free-suite-metadata) for the top-level test suite.

`-G, --settag <tag>`{.option}
:   [Sets the tag(s)](../execution/configuration.md#setting-test-tags) to all processed test cases.

`-t, --test <name>`{.option}
:   [Selects the test cases by name](../execution/configuration.md#by-test-names).

`--task <name>`{.option}
:   Alias for `--test`{.option}.

`-s, --suite <name>`{.option}
:   [Selects the test suites](../execution/configuration.md#by-suite-names) by name.

`-i, --include <tag>`{.option}
:   [Selects the test cases](../execution/configuration.md#by-tag-names) by tag.

`-e, --exclude <tag>`{.option}
:   [Selects the test cases](../execution/configuration.md#by-tag-names) by tag.

`-d, --outputdir <dir>`{.option}
:   Defines where to [create result files](../execution/results.md#output-directory).

`-o, --output <file>`{.option}
:   Sets the path to the generated [output file](../execution/results.md#output-file).

`--legacyoutput`{.option}
:   Creates output file in [Robot Framework 6.x compatible format](../execution/results.md#legacy-xml-format).

`-l, --log <file>`{.option}
:   Sets the path to the generated [log file](../execution/results.md#log-file).

`-r, --report <file>`{.option}
:   Sets the path to the generated [report file](../execution/results.md#report-file).

`-x, --xunit <file>`{.option}
:   Sets the path to the generated [xUnit compatible result file](../execution/results.md#xunit-compatible-result-file).

`-T, --timestampoutputs`{.option}
:   [Adds a timestamp](../execution/results.md#timestamping-result-files) to [result files](../execution/results.md#result-files) listed above.

`--splitlog`{.option}
:   [Split log file](../execution/results.md#splitting-logs) into smaller pieces that open in browser transparently.

`--logtitle <title>`{.option}
:   [Sets a title](../execution/results.md#setting-titles) for the generated test log.

`--reporttitle <title>`{.option}
:   [Sets a title](../execution/results.md#setting-titles) for the generated test report.

`--reportbackground <colors>`{.option}
:   [Sets background colors](../execution/results.md#setting-background-colors) of the generated report.

`-L, --loglevel <level>`{.option}
:   [Sets the threshold level](../execution/results.md#setting-log-level) to select log messages. Optionally the default [visible log level](../execution/results.md#visible-log-level) can be given separated with a colon (:).

`--suitestatlevel <level>`{.option}
:   Defines how many [levels to show](../execution/results.md#configuring-displayed-suite-statistics) in the *Statistics by Suite* table in outputs.

`--tagstatinclude <tag>`{.option}
:   [Includes only these tags](../execution/results.md#including-and-excluding-tag-statistics) in the *Statistics by Tag* table.

`--tagstatexclude <tag>`{.option}
:   [Excludes these tags](../execution/results.md#including-and-excluding-tag-statistics) from the *Statistics by Tag* table.

`--tagstatcombine <tags:title>`{.option}
:   Creates [combined statistics based on tags](../execution/results.md#generating-combined-tag-statistics).

`--tagdoc <pattern:doc>`{.option}
:   Adds [documentation to the specified tags](../execution/results.md#adding-documentation-to-tags).

`--tagstatlink <pattern:link:title>`{.option}
:   Adds [external links](../execution/results.md#creating-links-from-tag-names) to the *Statistics by Tag* table.

`--expandkeywords <name:pattern|tag:pattern>`{.option}
:   Automatically [expand keywords](../execution/results.md#automatically-expanding-keywords) in the generated log file.

`--removekeywords <all|passed|name:pattern|tag:pattern|for|wuks>`{.option}
:   [Removes keyword data](../execution/results.md#removing-and-flattening-keywords) from the generated outputs.

`--flattenkeywords <for|foritem|name:pattern|tag:pattern>`{.option}
:   [Flattens keywords](../execution/results.md#removing-and-flattening-keywords) in the generated outputs.

`--starttime <timestamp>`{.option}
:   Sets the [starting time](../execution/results.md#setting-start-and-end-time-of-execution) of test execution when creating reports.

`--endtime <timestamp>`{.option}
:   Sets the [ending time](../execution/results.md#setting-start-and-end-time-of-execution) of test execution when creating reports.

`--nostatusrc`{.option}
:   Sets the [return code](../execution/basics.md#return-codes) to zero regardless of failures in test cases. Error codes are returned normally.

`--processemptysuite`{.option}
:   Processes output files even if files contain [empty test suites](../execution/configuration.md#when-no-tests-match-selection).

`--prerebotmodifier <name:args>`{.option}
:   Activate [programmatic modification of results](../execution/results.md#programmatic-modification-of-results).

`--console <verbose|quiet|none|custom>`{.option}
:   [Controlling Rebot console output](../execution/post-processing.md#controlling-rebot-console-output). Also accepts [custom console loggers](../execution/configuration.md#custom-console-loggers).

`--quiet`{.option}
:   Shortcut for `--console quiet`.

`-C, --consolecolors <auto|on|ansi|off>`{.option}
:   [Specifies are colors](../execution/configuration.md#console-colors) used on the console.

`--consolelinks <auto|off>`{.option}
:   Controls [making paths to results files hyperlinks](../execution/configuration.md#console-links).

`-P, --pythonpath <path>`{.option}
:   Additional locations to add to the [module search path](../execution/configuration.md#module-search-path).

`-A, --argumentfile <path>`{.option}
:   A text file to [read more arguments](../execution/basics.md#argument-files) from.

`-h, --help`{.option}
:   Prints [usage instructions](../execution/basics.md#getting-help-and-version-information).

`--version`{.option}
:   Prints the [version information](../execution/basics.md#getting-help-and-version-information).

## Environment variables for execution and post-processing

`ROBOT_OPTIONS` and `REBOT_OPTIONS`
: Space separated list of default options to be placed
    [in front of any explicit options](../execution/basics.md#robot-options-and-rebot-options-environment-variables) on the command line.

`ROBOT_SYSLOG_FILE`
: Path to a [syslog](../execution/results.md#system-log) file where Robot Framework writes internal
    information about parsing test case files and running
    tests.

`ROBOT_SYSLOG_LEVEL`
: Log level to use when writing to the [syslog](../execution/results.md#system-log) file.

`ROBOT_INTERNAL_TRACES`
: When set to any non-empty value, Robot Framework's
    internal methods are included in [error tracebacks](../execution/basics.md#debugging-problems).

