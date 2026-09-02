# Registrations

This appendix lists file extensions, media types, and so on, that are
associated with Robot Framework.

## Suite file extensions

[Suite files](../syntax/suites.md#suite-files) with the following extensions are parsed automatically:

*.robot*
    Suite file using the [plain text format](../syntax/data.md#plain-text-format).

*.robot.rst*
    Suite file using the [reStructuredText format](../syntax/data.md#restructuredtext-format).

*.robot.md*
    Suite file using the [Markdown format](../syntax/data.md#markdown-format).

*.rbt*
    Suite file using the [JSON format](../syntax/data.md#json-format).

Using other extensions is possible, but it requires [separate configuration](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=8270).

## Resource file extensions

[Resource files](../syntax/resource-files.md#resource-files) can use the following extensions:

*.resource*
    Recommended when using the plain text format.

*.robot*, *.txt* and *.tsv*
    Supported with the plain text format for backwards compatibility reasons.
    *.resource* is recommended and may be mandated in the future.

*.rst* and *.rest*
    Resource file using the [reStructuredText format](../syntax/data.md#restructuredtext-format).

*.md* and *.markdown*
    Resource file using the [Markdown format](../syntax/data.md#markdown-format).

*.rsrc* and *.json*
    Resource file using the [JSON format](../syntax/data.md#json-format).

## Media type

The media type to use with Robot Framework data is `text/robotframework`.

## Remote server port

The default [remote server](../extend/remote.md#remote-library-interface) port is 8270. The port has been [registered by IANA](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=8270).

