# Registrations

This appendix lists file extensions, media types, and so on, that are
associated with Robot Framework.

## Suite file extensions

[Suite files](../syntax/suites.md#suite-files) with the following extensions are parsed automatically:

`.robot`{.file}
: Suite file using the [plain text data format](../syntax/data.md#plain-text-data-format).

`.robot.rst`{.file}
: Suite file using the [reStructuredText data format](../syntax/data.md#restructuredtext-data-format).

`.robot.md`{.file}
: Suite file using the [Markdown data format](../syntax/data.md#markdown-data-format).

`.rbt`{.file}
: Suite file using the [JSON data format](../syntax/data.md#json-data-format).

Using other extensions is possible, but it requires [separate configuration](../execution/configuration.md#selecting-files-to-parse).

## Resource file extensions

[Resource files](../syntax/resource-files.md#resource-files) can use the following extensions:

`.resource`{.file}
: Recommended when using the plain text format.

`.robot`{.file}, `.txt`{.file} and `.tsv`{.file}
: Supported with the plain text format for backwards compatibility reasons.
    `.resource`{.file} is recommended and may be mandated in the future.

`.rst`{.file} and `.rest`{.file}
: Resource file using the [reStructuredText format](../syntax/resource-files.md#resource-files-using-restructuredtext-format).

`.md`{.file} and `.markdown`{.file}
: Resource file using the [Markdown format](../syntax/resource-files.md#resource-files-using-markdown-format).

`.rsrc`{.file} and `.json`{.file}
: Resource file using the [JSON format](../syntax/resource-files.md#resource-files-using-json-format).

## Media type

The media type to use with Robot Framework data is `text/robotframework`.

## Remote server port

The default [remote server](../extend/remote.md#remote-library-interface) port is 8270. The port has been [registered by IANA](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=8270).

