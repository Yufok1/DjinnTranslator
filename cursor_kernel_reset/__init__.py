# Copyright 2024 SpliceWeb
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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