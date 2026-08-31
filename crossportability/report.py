from . import detect


def imports(path: str) -> str:
    """
    Generate a text report of platform-specific imports.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing the detected imports.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect.imports(path)
    report = []
    for file, findings in results.items():
        report.append(f"FILE: {file}")
        if findings:
            for finding in findings:
                report.append(f"  {finding[0]} → {finding[1]}")
        else:
            report.append("  No findings")
        report.append("")
    return "\n".join(report)


def ospath(path: str) -> str:
    """
    Generate a report of operating-system-specific paths.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing the detected OS-specific paths.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect.ospath(path)
    report = []
    for file, findings in results.items():
        report.append(f"FILE: {file}")
        if findings:
            for finding in findings:
                report.append(f"  {finding[0]} → {finding[1]}")
        else:
            report.append("  No findings")
        report.append("")
    return "\n".join(report)


def platform_usage(path: str) -> str:
    """
    Generate a report of platform-specific checks in Python code.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing detected uses of os.name
        and sys.platform.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect.platform_usage(path)
    report = []
    for file, findings in results.items():
        report.append(f"FILE: {file}")
        if findings:
            for finding in findings:
                report.append(f"  {finding}")
        else:
            report.append("  No findings")
        report.append("")
    return "\n".join(report)


def commands(path: str) -> str:
    """
    Generate a report of potentially platform-dependent system commands.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing detected uses of os.system
        and subprocess.run.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect.commands(path)
    report = []
    for file, findings in results.items():
        report.append(f"FILE: {file}")
        if findings:
            for finding in findings:
                report.append(f"  {finding}")
        else:
            report.append("  No findings")
        report.append("")
    return "\n".join(report)


def environment(path: str) -> str:
    """
    Generate a report of platform-specific environment variables.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing the detected environment variables.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect.environment(path)
    report = []
    for file, findings in results.items():
        report.append(f"FILE: {file}")
        if findings:
            for finding in findings:
                report.append(f"  {finding[0]} → {finding[1]}")
        else:
            report.append("  No findings")
        report.append("")
    return "\n".join(report)


def scan(path: str) -> str: #generates a report which contains all findings from a directory/file
    """
    Generate a complete portability report.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing all portability detection results.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    sections = []
#for adding each detection category as a separate section
    sections.append("OS-SPECIFIC PATHS") 
    sections.append(ospath(path))
    sections.append("PLATFORM DETECTION")
    sections.append(platform_usage(path))
    sections.append("SYSTEM COMMANDS")
    sections.append(commands(path))
    sections.append("PLATFORM-SPECIFIC IMPORTS")
    sections.append(imports(path))
    sections.append("ENVIRONMENT VARIABLES")
    sections.append(environment(path))
    return "\n\n".join(sections)


def files(path: str) -> str:
    """
    Generate a formatted table of Python files found at the given path.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A formatted string containing the discovered Python files.

    Raises:
        ValueError: If the path does not exist or is invalid.
    """
    results = detect._get_python_files(path)
    if not results:
        return "PYTHON FILES\n\nNo Python files found."
    rows = []
    rows.append("PYTHON FILES")
    rows.append("-" * 60)
    rows.append(f"{'#':<5} {'FILE'}")
    rows.append("-" * 60)
    for number, file in enumerate(results, start=1):
        rows.append(f"{number:<5} {file}")
    rows.append("-" * 60)
    return "\n".join(rows)
