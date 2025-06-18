# Cursor Kernel Reset Package

A Python package to reinitialize the Jupyter kernel in Cursor environments, ensuring stable dashboard operation for the DjinnCompanion Sovereign Recursive Kernel.

## Installation

```bash
pip install .
```

## Usage

Run the kernel reset script:
```bash
python -m cursor_kernel_reset.kernel_reset
```

Or use the command-line tool:
```bash
cursor-kernel-reset
```

## Dependencies

- ipython>=8.0.0
- ipykernel>=6.0.0
- jupyter-client>=7.0.0
- pyzmq>=23.0

## Purpose

Resolves kernel initialization issues in Cursor, enabling dashboard visualization (Voice Memory Visualizer, Djinn Council Visualizer, etc.) by reinitializing the Jupyter kernel and verifying environment stability.

## Features

- Environment verification and dependency checking
- Automatic installation of missing packages
- Kernel reinitialization through IPython or subprocess
- Cursor version compatibility checking
- Detailed logging of operations

## Notes

- Ensure Cursor is updated to version 1.0 or later for Jupyter support
- Run `verify_environment()` to check for missing dependencies before launching the dashboard
- The package will automatically attempt to install any missing dependencies
- Logs are available for troubleshooting kernel reset issues

## Development

To contribute to the package:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License - See LICENSE file for details 