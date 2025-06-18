"""
Cursor Kernel Reset Package

A package to reinitialize the Jupyter kernel in Cursor environments.
"""

from .kernel_reset import (
    verify_environment,
    install_missing_packages,
    reset_kernel,
    verify_cursor_version,
    KernelResetError
)

__version__ = "0.1.0"
__all__ = [
    "verify_environment",
    "install_missing_packages",
    "reset_kernel",
    "verify_cursor_version",
    "KernelResetError"
] 