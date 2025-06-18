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