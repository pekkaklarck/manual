
<a id="settings"></a>
# Available settings

This appendix lists all settings that can be used in different sections.

!!! note
    Settings can be [localized](../creating-test-data/test-data-syntax.md#localized). See the [Translations](translations.md#translations) appendix for
    supported translations.

## Setting section

The Setting section is used to import libraries, resource files and
variable files and to define metadata for test suites and test
cases. It can be included in test case files and resource files. Note
that in a resource file, a Setting section can only include settings for
importing libraries, resources, and variables.

| Name | Description |
| --- | --- |
| Library | Used for [importing libraries](../creating-test-data/using-test-libraries.md#importing-libraries). |
| Resource | Used for [taking resource files into use](../creating-test-data/resource-files.md#taking-resource-files-into-use). |
| Variables | Used for [taking variable files into use](../creating-test-data/variable-files.md#taking-variable-files-into-use). |
| Name | Used for setting a custom [suite name](../creating-test-data/creating-test-suites.md#suite-name). |
| Documentation | Used for specifying a [suite](../creating-test-data/creating-test-suites.md#suite-documentation) or [resource file](../creating-test-data/resource-files.md#resource-files) documentation. |
| Metadata | Used for setting [free suite metadata](../creating-test-data/creating-test-suites.md#free-suite-metadata). |
| Suite Setup | Used for specifying the [suite setup](../executing-tests/test-execution.md#suite-setup). |
| Suite Teardown | Used for specifying the [suite teardown](../executing-tests/test-execution.md#suite-teardown). |
| Test  Tags | Used for specifying [test case tags](../creating-test-data/creating-test-cases.md#test-case-tags) for all tests in a suite. |
| Force Tags, Default Tags | [Deprecated settings](../creating-test-data/creating-test-cases.md#deprecation-of-force-tags-and-default-tags) for specifying test case tags. |
| Keyword Tags | Used for specifying [user keyword tags](../creating-test-data/creating-user-keywords.md#user-keyword-tags) for all keywords in a certain file. |
| Test Setup | Used for specifying a default [test setup](../executing-tests/test-execution.md#test-setup). |
| Test Teardown | Used for specifying a default [test teardown](../executing-tests/test-execution.md#test-teardown). |
| Test Template | Used for specifying a default [template keyword](../creating-test-data/creating-test-cases.md#template-keyword) for test cases. |
| Test Timeout | Used for specifying a default [test case timeout](../creating-test-data/advanced-features.md#test-case-timeout). |
| Task Setup, Task Teardown, Task Template, Task Timeout | Aliases for Test Setup, Test Teardown, Test Template and Test Timeout, respectively, that can be used when [creating tasks](../creating-test-data/creating-tasks.md#creating-tasks). |

## Test Case section

The settings in the Test Case section are always specific to the test
case for which they are defined. Some of these settings override the
default values defined in the Settings section.

Exactly same settings are available when [creating tasks](../creating-test-data/creating-tasks.md#creating-tasks) in the Task section.

| Name | Description |
| --- | --- |
| [Documentation] | Used for specifying a [test case documentation](../creating-test-data/creating-test-cases.md#test-case-documentation). |
| [Tags] | Used for [tagging test cases](../creating-test-data/creating-test-cases.md#tagging-test-cases). |
| [Setup] | Used for specifying a [test setup](../executing-tests/test-execution.md#test-setup). |
| [Teardown] | Used for specifying a [test teardown](../executing-tests/test-execution.md#test-teardown). |
| [Template] | Used for specifying a [template keyword](../creating-test-data/creating-test-cases.md#template-keyword). |
| [Timeout] | Used for specifying a [test case timeout](../creating-test-data/advanced-features.md#test-case-timeout). |

## Keyword section

Settings in the Keyword section are specific to the user keyword for
which they are defined.

| Name | Description |
| --- | --- |
| [Documentation] | Used for specifying a [user keyword documentation](../creating-test-data/creating-user-keywords.md#user-keyword-documentation). |
| [Tags] | Used for specifying [user keyword tags](../creating-test-data/creating-user-keywords.md#user-keyword-tags). |
| [Arguments] | Used for specifying [user keyword arguments](../creating-test-data/creating-user-keywords.md#user-keyword-arguments). |
| [Setup] | Used for specifying a [user keyword setup](../executing-tests/test-execution.md#user-keyword-setup). New in Robot Framework 7.0. |
| [Teardown] | Used for specifying [user keyword teardown](../executing-tests/test-execution.md#user-keyword-teardown). |
| [Timeout] | Used for specifying a [user keyword timeout](../creating-test-data/advanced-features.md#user-keyword-timeout). |
| [Return] | Used for specifying [user keyword return values](../creating-test-data/creating-user-keywords.md#user-keyword-return-values). Deprecated in Robot Framework 7.0. Use the [RETURN](../creating-test-data/creating-user-keywords.md#return) statement instead. |
