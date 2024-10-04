#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""The root of the Robot Framework package.

The command line entry points provided by the framework are exposed for
programmatic usage as follows:

  * [run][robot.run.run]: Function to run tests.
  * [run_cli][robot.run.run_cli]: Function to run tests
    with command line argument processing.
  * [rebot][robot.rebot.rebot]: Function to post-process outputs.
  * [rebot_cli][robot.rebot.rebot_cli]: Function to post-process outputs
    with command line argument processing.
  * [libdoc][robot.libdoc]: Module for library documentation generation.
  * [testdoc][robot.testdoc]: Module for test case documentation generation.

All the functions above can be imported directly from the `robot` root module
like `#!py from robot import run`. Functions and classes provided by the modules
need to be imported like `#!py from robot.libdoc import libdoc_cli`.

The functions and modules listed above are considered stable. Other modules in
this package are for internal usage and may change without a prior notice.

!!! tip

    The stable public API is otherwise exposed via the [robot.api][] module.
"""

import sys
import warnings

from robot.rebot import rebot, rebot_cli
from robot.run import run, run_cli
from robot.version import get_version


# Avoid warnings when using `python -m robot.run`.
# https://github.com/robotframework/robotframework/issues/2552
if not sys.warnoptions:
    warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')


__all__ = ['run', 'run_cli', 'rebot', 'rebot_cli']
__version__ = get_version()
