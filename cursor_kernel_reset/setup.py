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
Setup configuration for cursor_kernel_reset package.
"""

from setuptools import setup, find_packages

setup(
    name="cursor_kernel_reset",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ipython>=8.0.0",
        "ipykernel>=6.0.0",
        "jupyter-client>=7.0.0",
        "pyzmq>=23.0",
    ],
    author="Purveyor Sovereign",
    description="A package to reinitialize Jupyter kernel in Cursor environment",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/purveyor-sovereign/cursor_kernel_reset",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "cursor-kernel-reset=cursor_kernel_reset.kernel_reset:main",
        ],
    },
) 