from pathlib import Path
import ast


def _validate_path(path: str | Path) -> Path:
    """
    Validate that the supplied path exists.

    Args:
        path: A file or directory path.

    Returns:
        A Path object representing the supplied path.

    Raises:
        ValueError: If the path does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise ValueError("Path does not exist")
    return path


def _get_python_files(path: str | Path) -> list[Path]:
    """
    Find Python files from a file or directory path.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A list of Python file paths.

    Raises:
        ValueError: If the path is invalid or is not a Python file.
    """
    path = _validate_path(path)
    if path.is_file():
        if path.suffix == ".py":
            return [path]
        raise ValueError("File is not a Python file")
    if path.is_dir():
        return list(path.rglob("*.py"))
    raise ValueError("Invalid path")


def imports(path: str | Path) -> dict[str, list[tuple[str, str]]]:
    """
    Detect OS-specific Python imports.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary mapping file paths to detected imports.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    files = _get_python_files(path)
    results = {}
    for file in files:
        code = file.read_text()
        tree = ast.parse(code)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name
                    if module in ["winsound", "winreg", "msvcrt"]:
                        findings.append(("Windows", module))
                    elif module in ["pwd", "grp", "termios", "fcntl"]:
                        findings.append(("Unix", module))
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                if module in ["winsound", "winreg", "msvcrt"]:
                    findings.append(("Windows", module))
                elif module in ["pwd", "grp", "termios", "fcntl"]:
                    findings.append(("Unix", module))
        results[str(file)] = findings
    return results


def ospath(path: str | Path) -> dict[str, list[tuple[str, str]]]:
    """
    Detect hard-coded operating-system-specific paths.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary mapping file paths to detected
        Windows- or Unix-style paths.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    files = _get_python_files(path)
    results = {}
    for file in files:
        code = file.read_text()
        tree = ast.parse(code)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    if ":" in node.value and "\\" in node.value:
                        findings.append(("Windows", node.value))
                    elif node.value.startswith("/"):
                        findings.append(("Unix", node.value))
        results[str(file)] = findings
    return results


def platform_usage(path: str | Path) -> dict[str, list[str]]:
    """
    Detect platform-specific checks using os.name or sys.platform.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary mapping file paths to detected platform checks.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    files = _get_python_files(path)
    results = {}
    for file in files:
        code = file.read_text()
        tree = ast.parse(code)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    if node.value.id == "os" and node.attr == "name":
                        findings.append("os.name")
                    elif node.value.id == "sys" and node.attr == "platform":
                        findings.append("sys.platform")
        results[str(file)] = findings
    return results


def commands(path: str | Path) -> dict[str, list[str]]:
    """
    Detect potentially platform-dependent system commands.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary mapping file paths to detected system commands.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    files = _get_python_files(path)
    results = {}
    for file in files:
        code = file.read_text()
        tree = ast.parse(code)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id == "os" and node.func.attr == "system":
                            findings.append("os.system")
                        elif node.func.value.id == "subprocess" and node.func.attr == "run":
                            findings.append("subprocess.run")
        results[str(file)] = findings
    return results


def environment(path: str | Path) -> dict[str, list[tuple[str, str]]]:
    """
    Detect platform-specific environment variables.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary mapping file paths to detected
        Unix- or Windows-specific environment variables.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    files = _get_python_files(path)
    results = {}
    windows_variables = ["USERPROFILE", "APPDATA", "PROGRAMFILES"]
    unix_variables = ["HOME", "PATH", "SHELL"]
    for file in files:
        code = file.read_text()
        tree = ast.parse(code)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Attribute):
                    if isinstance(node.value.value, ast.Name):
                        if node.value.value.id == "os" and node.value.attr == "environ":
                            if isinstance(node.slice, ast.Constant):
                                if isinstance(node.slice.value, str):
                                    if node.slice.value in unix_variables:
                                        findings.append(("Unix", node.slice.value))
                                    elif node.slice.value in windows_variables:
                                        findings.append(("Windows", node.slice.value))
        results[str(file)] = findings
    return results


def scan(path: str | Path) -> dict:
    """
    Run all portability detection checks on a Python file or directory.

    Args:
        path: A Python file or directory to scan.

    Returns:
        A dictionary containing the results from all detection categories.

    Raises:
        ValueError: If the supplied path does not exist or is invalid.
    """
    return {
        "os_paths": ospath(path),
        "platform_usage": platform_usage(path),
        "system_commands": commands(path),
        "imports": imports(path),
        "environment_variables": environment(path)
            }
