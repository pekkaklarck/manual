
<a id="settings"></a>
# Available settings

This appendix lists all settings that can be used in different sections.

!!! note
    Settings can be [localized](../syntax/data.md#localized). See the [Translations](translations.md#translations) appendix for
    supported translations.

## Setting section

The Setting section is used to import libraries, resource files and
variable files and to define metadata for test suites and test
cases. It can be included in test case files and resource files. Note
that in a resource file, a Setting section can only include settings for
importing libraries, resources, and variables.

| Name | Description |
| --- | --- |
| Library | Used for [importing libraries](../syntax/libraries.md#importing-libraries). |
| Resource | Used for [taking resource files into use](../syntax/resource-files.md#taking-resource-files-into-use). |
| Variables | Used for [taking variable files into use](../syntax/variable-files.md#taking-variable-files-into-use). |
| Name | Used for setting a custom [suite name](../syntax/suites.md#suite-name). |
| Documentation | Used for specifying a [suite](../syntax/suites.md#suite-documentation) or [resource file](../syntax/resource-files.md#resource-files) documentation. |
| Metadata | Used for setting [free suite metadata](../syntax/suites.md#free-suite-metadata). |
| Suite Setup | Used for specifying the [suite setup](../execution/tests.md#suite-setup). |
| Suite Teardown | Used for specifying the [suite teardown](../execution/tests.md#suite-teardown). |
| Test  Tags | Used for specifying [test case tags](../syntax/tests.md#test-case-tags) for all tests in a suite. |
| Force Tags, Default Tags | [Deprecated settings](../syntax/tests.md#deprecation-of-force-tags-and-default-tags) for specifying test case tags. |
| Keyword Tags | Used for specifying [user keyword tags](../syntax/user-keywords.md#user-keyword-tags) for all keywords in a certain file. |
| Test Setup | Used for specifying a default [test setup](../execution/tests.md#test-setup). |
| Test Teardown | Used for specifying a default [test teardown](../execution/tests.md#test-teardown). |
| Test Template | Used for specifying a default [template keyword](../syntax/tests.md#template-keyword) for test cases. |
| Test Timeout | Used for specifying a default [test case timeout](../syntax/advanced.md#test-case-timeout). |
| Task Setup, Task Teardown, Task Template, Task Timeout | Aliases for Test Setup, Test Teardown, Test Template and Test Timeout, respectively, that can be used when [creating tasks](../syntax/tasks.md#creating-tasks). |

## Test Case section

The settings in the Test Case section are always specific to the test
case for which they are defined. Some of these settings override the
default values defined in the Settings section.

Exactly same settings are available when [creating tasks](../syntax/tasks.md#creating-tasks) in the Task section.

| Name | Description |
| --- | --- |
| [Documentation] | Used for specifying a [test case documentation](../syntax/tests.md#test-case-documentation). |
| [Tags] | Used for [tagging test cases](../syntax/tests.md#tagging-test-cases). |
| [Setup] | Used for specifying a [test setup](../execution/tests.md#test-setup). |
| [Teardown] | Used for specifying a [test teardown](../execution/tests.md#test-teardown). |
| [Template] | Used for specifying a [template keyword](../syntax/tests.md#template-keyword). |
| [Timeout] | Used for specifying a [test case timeout](../syntax/advanced.md#test-case-timeout). |

## Keyword section

Settings in the Keyword section are specific to the user keyword for
which they are defined.

| Name | Description |
| --- | --- |
| [Documentation] | Used for specifying a [user keyword documentation](../syntax/user-keywords.md#user-keyword-documentation). |
| [Tags] | Used for specifying [user keyword tags](../syntax/user-keywords.md#user-keyword-tags). |
| [Arguments] | Used for specifying [user keyword arguments](../syntax/user-keywords.md#user-keyword-arguments). |
| [Setup] | Used for specifying a [user keyword setup](../execution/tests.md#user-keyword-setup). New in Robot Framework 7.0. |
| [Teardown] | Used for specifying [user keyword teardown](../execution/tests.md#user-keyword-teardown). |
| [Timeout] | Used for specifying a [user keyword timeout](../syntax/advanced.md#user-keyword-timeout). |
| [Return] | Used for specifying [user keyword return values](../syntax/user-keywords.md#user-keyword-return-values). Deprecated in Robot Framework 7.0. Use the [RETURN](../syntax/user-keywords.md#return) statement instead. |
