#!/usr/bin/env python3
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

import os
import re
from pathlib import Path

LICENSE_HEADER = '''# Copyright 2024 SpliceWeb
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

'''

def should_skip_file(file_path):
    """Check if file should be skipped."""
    skip_patterns = [
        r'__pycache__',
        r'\.git',
        r'\.venv',
        r'\.env',
        r'\.pytest_cache',
        r'\.coverage',
        r'\.tox',
        r'\.mypy_cache',
        r'\.ruff_cache',
        r'\.eggs',
        r'\.idea',
        r'\.vscode',
        r'\.DS_Store',
        r'\.pyc$',
        r'\.pyo$',
        r'\.pyd$',
        r'\.so$',
        r'\.dylib$',
        r'\.dll$',
        r'\.exe$',
        r'\.egg$',
        r'\.egg-info$',
        r'\.dist-info$',
        r'\.whl$',
        r'\.tar\.gz$',
        r'\.zip$',
        r'\.rar$',
        r'\.7z$',
        r'\.bz2$',
        r'\.xz$',
        r'\.tar$',
        r'\.tgz$',
        r'\.tbz2$',
        r'\.txz$',
        r'\.tar\.bz2$',
        r'\.tar\.xz$',
        r'\.tar\.lzma$',
        r'\.tar\.lz$',
        r'\.tar\.lzo$',
        r'\.tar\.lzop$',
        r'\.tar\.lz4$',
        r'\.tar\.zst$',
        r'\.tar\.zstd$',
        r'\.tar\.lz$',
        r'\.tar\.lzo$',
        r'\.tar\.lzop$',
        r'\.tar\.lz4$',
        r'\.tar\.zst$',
        r'\.tar\.zstd$',
    ]
    return any(re.search(pattern, str(file_path)) for pattern in skip_patterns)

def has_license_header(content):
    """Check if file already has Apache 2.0 license header."""
    return "Licensed under the Apache License, Version 2.0" in content

def add_license_header(file_path):
    """Add license header to file if it doesn't have one."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if has_license_header(content):
            print(f"Skipping {file_path} - already has license header")
            return

        # Add license header
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(LICENSE_HEADER + content)
        print(f"Added license header to {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    """Main function to add license headers to all Python files."""
    # Get the project root directory
    project_root = Path(__file__).parent

    # Walk through all Python files
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                if not should_skip_file(file_path):
                    add_license_header(file_path)

if __name__ == '__main__':
    main() 