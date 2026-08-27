# CrossPortability

CrossPortability is an open-source Python library for detecting potentially platform-specific code in Python projects.

It helps developers identify code that may behave differently across operating systems, making cross-platform compatibility issues easier to find and review.

## Features

CrossPortability currently detects:

- OS-specific paths
- Platform-specific usage
- System commands
- Platform-specific imports
- Environment variables

## Installation

Install CrossPortability directly from PyPI:

~~~bash
pip install crossportability
~~~

## How to Use

Import CrossPortability into your Python project:

~~~python
from crossportability import detect, report
~~~

### Detection

CrossPortability analyzes Python source files and identifies potentially platform-specific code.

For example, consider the following Python code:

~~~python
import os
import subprocess

path = "C:\\Users\\example\\project"

if os.name == "nt":
    subprocess.run("dir", shell=True)
~~~

CrossPortability can identify potentially platform-specific patterns such as:

- Windows-specific paths
- Platform checks
- System commands

Detection results are organized into the following categories:

~~~text
os_paths
platform_usage
system_commands
imports
environment_variables
~~~

### Reporting

The `report` module presents detection results in a readable format.

Example report:

~~~text
OS-SPECIFIC PATHS

FILE: example.py
  Potential platform-specific path detected

PLATFORM DETECTION

FILE: example.py
  Platform-specific usage detected

SYSTEM COMMANDS

FILE: example.py
  System command detected

PLATFORM-SPECIFIC IMPORTS

FILE: example.py
  No findings

ENVIRONMENT VARIABLES

FILE: example.py
  No findings
~~~

> **Note:** CrossPortability identifies potentially platform-specific code. A finding does not necessarily mean that the code is incompatible with another operating system.

## How It Works

CrossPortability uses Python's built-in `ast` module to analyze Python source code.

Instead of simply searching for specific strings, it examines the structure of Python code to identify platform-related patterns.

The detected patterns are organized into five categories:

- OS-specific paths
- Platform-specific usage
- System commands
- Platform-specific imports
- Environment variables

## Development

Clone the repository:

~~~bash
git clone <repository-url>
cd CrossPortability
~~~

Install the package in editable mode:

~~~bash
pip install -e .
~~~

Editable installation allows changes to the source code to be tested without reinstalling the package after every modification.

## Contributing

Contributions, suggestions, and bug reports are welcome.

If you find a platform-specific pattern that CrossPortability does not currently detect, feel free to open an issue or submit a pull request.

## License

See the `LICENSE` file for information about the project's license.

## PyPI

CrossPortability is available on PyPI:

https://pypi.org/project/crossportability/

## Version

**0.1.0**