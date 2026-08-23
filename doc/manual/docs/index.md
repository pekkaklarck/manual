# Robot Framework Manual

Robot Framework is an open source automation framework used for software testing, robotic process automation (RPA), and other automation tasks. It uses a readable syntax for keyword-driven and data-driven specification, as well as behaviour-driven development (BDD). The framework can be extended with libraries and tools.

This Manual is the **technical reference** for installing, using, and extending Robot Framework. It covers the framework itself and the standard libraries distributed with it. External libraries and tools have their own documentation.

Robot Framework automation is organised into test cases or tasks. This example shows a simple task:

```robotframework
*** Tasks ***
Create the monthly report
    Collect report data
    Generate report    format=PDF
    Send report    recipient=finance@example.com
```

The task name and keywords describe the workflow. Arguments such as `format=PDF` add details without hiding the intent. Keywords can come from standard or external libraries, or be created for the project.

## What the Manual covers

### Install Robot Framework

Set up Python, [install Robot Framework](install/index.md), check that the installation works, and use a virtual environment when needed.

### Write and run automation

Learn how automation files are structured in [Syntax](syntax/index.md), including how variables, keywords, and control structures work. [Execution](execution/index.md) covers running and configuring automation and working with generated execution artifacts such as logs and reports. Browse [Libraries](libraries/index.md) for reference documentation on the standard libraries distributed with Robot Framework.

### Create extensions

[Extend](extend/index.md) explains how to create libraries and use extension interfaces such as listeners and parsers. Use the Python [API reference](api/index.md) when working with Robot Framework programmatically.

### Find settings and terminology

Look in the [Appendix](appendix/index.md) for settings, command-line options, supported formats, and other reference information. If a term is unfamiliar, check the [Glossary](glossary.md) for its definition.

## Tutorials and how-to guides

The Manual explains Robot Framework features and behaviour in detail. If you want help putting that information into practice, the community-maintained [Robot Framework Guides](https://docs.robotframework.org/) offer tutorials, practical examples, and step-by-step instructions for specific tasks.

## External libraries and tools

External libraries and tools are developed and maintained separately from Robot Framework. **Libraries** can connect the framework to browsers, APIs, databases, and other technologies. **Tools** help with writing, running, and maintaining automation. You can find an overview of available external libraries and tools on the [Robot Framework website](https://robotframework.org/#resources).

## Community and contributions

The Robot Framework community is a place to ask questions, share knowledge, and work with others who use and develop the framework. You can contribute by helping another user or improving the project.

Here are three places to start:

- [**Community forum**](https://forum.robotframework.org/): Ask questions, find previous answers, and take part in longer discussions.

- [**Slack**](https://slack.robotframework.org/): Talk with other community members and join real-time discussions.

- [**GitHub**](https://github.com/robotframework): Follow development, report project issues, and contribute documentation or code.

## Robot Framework Foundation

Robot Framework is an open source project available under the Apache License 2.0 and stewarded by a non-profit association. The Foundation funds core development and maintenance. It also supports project infrastructure, the wider ecosystem, and community activities.

Learn more about the [Robot Framework Foundation](https://robotframework.org/foundation/).

## Reporting security issues

If you discover a potential security issue, **do not** disclose it through a public issue or community channel.

For independently maintained libraries and tools, contact the maintainers of the affected project privately.

For Robot Framework or another Foundation-managed project, report the issue confidentially to [security@robotframework.org](mailto:security@robotframework.org).
