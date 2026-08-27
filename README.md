CrossPortability

A Python library for detecting potentially platform-specific code and improving cross-platform compatibility.

CrossPortability analyzes Python source files and identifies patterns that may behave differently across operating systems.

Features

CrossPortability currently detects:

- OS-specific paths
- Platform-specific usage
- System commands
- Platform-specific imports
- Environment variables

The results are organized by detection category, making potential portability issues easier to review.

Installation

Install CrossPortability from PyPI:

python -m pip install crossportability

Quick Start

Import the library:

from crossportability import detect, report

Detect platform-specific code

from crossportability import detect

results = detect("example.py")

print(results)

The detector returns results grouped by category.

Example:

{
    'os_paths': {
        'example.py': []
    },
    'platform_usage': {
        'example.py': []
    },
    'system_commands': {
        'example.py': []
    },
    'imports': {
        'example.py': []
    },
    'environment_variables': {
        'example.py': []
    }
}

Generate a Report

The "report" module can be used to present detection results in a readable format.

from crossportability import detect, report

results = detect("example.py")

print(report(results))

Example output:

=== CROSSPORTABILITY REPORT ===

OS-SPECIFIC PATHS

FILE: example.py
  No findings


PLATFORM DETECTION

FILE: example.py
  No findings


SYSTEM COMMANDS

FILE: example.py
  No findings


PLATFORM-SPECIFIC IMPORTS

FILE: example.py
  No findings


ENVIRONMENT VARIABLES

FILE: example.py
  No findings

«Note: CrossPortability reports potentially platform-specific code. A finding does not necessarily mean that the code will fail on another operating system.»

Example

Consider the following Python code:

import os
import subprocess

path = "C:\\Users\\example\\project"

if os.name == "nt":
    subprocess.run("dir", shell=True)

CrossPortability can identify potentially platform-specific constructs such as:

- Windows-specific paths
- Platform checks
- System commands

This allows developers to review these areas before moving their project to another operating system.

How It Works

CrossPortability uses Python's built-in "ast" module to analyze Python source code.

Rather than relying solely on text matching, it examines the structure of the code to identify platform-related patterns.

The detection system is organized into separate categories so additional checks can be added as the project develops.

Project Structure

CrossPortability/
│
├── crossportability/
│   ├── __init__.py
│   ├── detect.py
│   └── report.py
│
├── LICENSE
├── README.md
└── pyproject.toml

Development

Clone the repository:

git clone <repository-url>
cd CrossPortability

Install the package in editable mode:

python -m pip install -e .

This allows changes to the source code to be tested without reinstalling the package after every modification.

Contributing

Contributions and suggestions are welcome.

If you find a platform-specific pattern that CrossPortability does not currently detect, you can open an issue describing the pattern or submit a pull request with an improvement.

License

See the "LICENSE" file for the project's license.

PyPI

CrossPortability is available on PyPI:

https://pypi.org/project/crossportability/

Version

0.1.0