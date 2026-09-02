# Robot Framework Manual

Robot Framework is an open source automation framework for software testing, robotic process automation (RPA), and other automation tasks. Its readable syntax supports keyword-driven and data-driven approaches, as well as behaviour-driven development (BDD). It can be extended with libraries and used with supporting tools.

This Manual is the **technical reference** for installing, using, and extending Robot Framework. It covers the framework itself and the standard libraries distributed with it. External libraries and tools have their own documentation.

Robot Framework automation is organised into test cases or tasks. This example shows a simple task:

```robotframework
*** Tasks ***
Create the monthly report
    Collect report data
    Generate report    format=PDF
    Send report    recipient=finance@example.com
```

The task name and keywords describe the workflow. Named arguments such as `format=PDF` add details while keeping the workflow readable. Keywords can come from standard or external libraries, or you can create user keywords for your project.

## What the Manual covers

- **Installation**: Set up Python, [install Robot Framework](install/index.md), and verify the installation. We recommend using a virtual environment to keep project dependencies isolated.
- **Write and run automation**: [Syntax](syntax/index.md) covers automation file structure, variables, keywords, and control structures. [Execution](execution/index.md) covers running and configuring automation and generated execution artifacts such as logs and reports. [Libraries](libraries/index.md) provides reference documentation for the standard libraries.
- **Create extensions**: [Extend](extend/index.md) explains how to create libraries and use extension interfaces such as listeners and parsers. Use the Python [API reference](api/index.md) when working with Robot Framework programmatically.
- **Find settings and terminology**: Look in the [Appendix](appendix/index.md) for settings, command-line options, and supported file formats. If a term is unfamiliar, check the [Glossary](glossary.md) for its definition.

## Guides, libraries, and tools

The Manual explains Robot Framework features and behaviour in detail. If you want to learn through examples or complete a specific task, the community-maintained [Robot Framework Guides](https://docs.robotframework.org/) offer tutorials and step-by-step instructions.

The wider Robot Framework ecosystem also includes libraries and tools developed and maintained separately from the framework. **Libraries** can connect the framework to browsers, APIs, databases, and other technologies. **Tools** help with writing, running, and maintaining automation. You can find an overview of available external libraries and tools on the [Robot Framework website](https://robotframework.org/#resources).

## Community and contributions

The Robot Framework community is a place to ask questions, share knowledge, and work with others who use and develop the framework. You can contribute by helping another user or improving the project.

Here are three places to start:

- [**Community forum**](https://forum.robotframework.org/): Ask questions, find previous answers, and take part in longer discussions.

- [**Slack**](https://slack.robotframework.org/): Chat with other community members in real time.

- [**GitHub**](https://github.com/robotframework): Follow development, report project issues, and contribute documentation or code.

## Robot Framework Foundation

Robot Framework is open source software released under the Apache License 2.0. The Robot Framework Foundation, a non-profit association, supports the project’s continued development and infrastructure.

The Foundation stewards the project and funds core development and maintenance. It also supports the wider ecosystem and community activities.

Learn more about the [Robot Framework Foundation](https://robotframework.org/foundation/).

## Reporting security issues

If you discover a potential security issue, **do not** disclose it through a public issue or community channel.

For independently maintained libraries and tools, contact the maintainers of the affected project privately.

For Robot Framework or another Foundation-managed project, report the issue confidentially to [security@robotframework.org](mailto:security@robotframework.org).
